# メロスケッチ：音源の出典・利用条件

## 録音音源

マリンバ・ピアノ・ビブラフォンは、**University of Iowa Musical Instrument Samples（MIS）**の録音素材を利用しています。

- 制作・公開：Lawrence Fritts / University of Iowa Electronic Music Studios
- 公式案内・利用条件：<https://theremin.music.uiowa.edu/MIS.html>
- 公式の使用条件には、録音を **“downloaded and used for any projects, without restrictions”**（あらゆるプロジェクトに制限なく使用可能）と記載されています。
- 本ファイルは出典と案内です。素材に、こちらで独自のCC0やMITライセンスを付け直してはいません。

利用条件の最新の記載は、公式サイトで確認してください。

### ピアノ

- 楽器：Steinway & Sons Model B
- 出典：<https://theremin.music.uiowa.edu/MISpiano.html>
- 元ファイル：`Piano.mf.[NOTE].aiff` と `Piano.pp.[NOTE].aiff`
- 使用音：C4、D4、E4、G4、A4、C5、D5、E5、G5
- 各音2段階の強弱、計18サンプル。ステレオ録音です。
- 加工：発音前の無音除去、孤立したデジタルスパイクの低減、レベル調整、終端フェード、MP3への変換。
- 再生時に異なる音を大きな音程変更で代用するのではなく、各音の録音を使っています。

### マリンバ

- 出典：<https://theremin.music.uiowa.edu/Mismarimba.html>
- 元ファイル：`Marimba.yarn.mf.C4B4.aif`、`Marimba.yarn.mf.C5B5.aif`
- 毛糸巻きマレットを使った演奏です。
- 使用音：C4、D4、E4、G4、A4、C5、D5、E5、G5、計9サンプル。
- 加工：音ごとの切り出し、レベル調整、発音・終端フェード、MP3への変換。
- 元の録音のピッチを測定し、再生時に小さなチューニング補正を行います。

### ビブラフォン

- 出典：<https://theremin.music.uiowa.edu/Misvibraphone.html>
- 元ファイル：`Vibraphone.shortsustain.mf.C4B4.aif`、`Vibraphone.shortsustain.mf.C5B5.aif`
- 使用音：C4、D4、E4、G4、A4、C5、D5、E5、G5、計9サンプル。
- 加工：低域ノイズ除去、音ごとの切り出し、ノイズ低減、レベル調整、減衰と終端フェード、高域調整、MP3への変換。
- 元の録音のピッチを測定し、再生時に小さなチューニング補正を行います。
- 初期試作で使用した弱いロングサステイン録音は、この版には含めていません。

## 音響合成

### リズム

Web Audio APIでキック・スネア・ハイハットを合成しています。キックは低い基音に上の倍音を重ね、小さなスピーカーでも輪郭が聞き取りやすいようにしています。第三者の録音サンプルは使用していません。

### ピコピコ

Web Audio APIの矩形波、フィルター、音量エンベロープで作るゲーム風の電子音です。特定のゲームの音声データやメロディは使用していません。

## パッケージへの収録方法

加工済み録音サンプルは、`index.html` 内にBase64で含めています。別の音源フォルダ、外部CDN、アクセスキーは不要です。

アプリ本体のコードのライセンスについては、`README.md`を参照してください。
