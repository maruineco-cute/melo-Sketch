"""Optional Melosketch preview server and H.264/AAC MP4 converter.

Requirements: Python 3 and ffmpeg on PATH. No third-party Python packages.
For local/prototype use. Add authentication, rate limits and HTTPS for public hosting.
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit
import os
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", "8080"))
MAX_VIDEO_SIZE = 40 * 1024 * 1024


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        super().end_headers()

    def do_GET(self):
        path = urlsplit(self.path).path
        if path in ("/", "/index.html"):
            data = (ROOT / "index.html").read_bytes()
            # Only this optional server enables video uploads/conversion.
            # The unchanged file on GitHub Pages remains entirely browser-side.
            flag = b"<head><script>window.MELOSKETCH_CONVERTER=true;</script>"
            data = data.replace(b"<head>", flag, 1)
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if path == "/api/convert":
            self.send_error(405, "Use POST")
            return
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/api/convert":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_VIDEO_SIZE:
                self.send_error(413, "Video is empty or larger than 40 MB")
                return
            if shutil.which("ffmpeg") is None:
                self.send_error(503, "Install ffmpeg to enable MP4 conversion")
                return
            self.connection.settimeout(60)
            body = self.rfile.read(size)
            if len(body) != size:
                self.send_error(400, "Incomplete upload")
                return
            with tempfile.TemporaryDirectory(prefix="melosketch-video-") as folder:
                src = Path(folder) / "input.video"
                dst = Path(folder) / "output.mp4"
                src.write_bytes(body)
                result = subprocess.run(
                    [
                        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                        "-i", str(src), "-map", "0:v:0", "-map", "0:a:0",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac",
                        "-b:a", "160k", "-movflags", "+faststart", str(dst),
                    ],
                    capture_output=True,
                    timeout=90,
                    check=False,
                )
                if result.returncode:
                    print(result.stderr.decode(errors="replace"), flush=True)
                    self.send_error(422, "Video could not be converted")
                    return
                data = dst.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
        except (ValueError, subprocess.TimeoutExpired, OSError) as exc:
            print(str(exc), flush=True)
            try:
                self.send_error(500, "Conversion failed")
            except OSError:
                pass


if __name__ == "__main__":
    if not (ROOT / "index.html").is_file():
        raise SystemExit("Place index.html next to server.py.")
    if shutil.which("ffmpeg") is None:
        print("Warning: ffmpeg is missing; native browser video export remains available.")
    print(f"Melosketch: http://localhost:{PORT}/", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
