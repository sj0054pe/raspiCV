中本真誉
====

## Project Title
RaspberryPiを用いた植物観測ツールの開発

## ソフトについて
RaspberryPiのカメラで撮影した植物の画像から、画像認識を利用して葉の面積を導出させるソフト。

## 機能
面積導出はOpenCVを利用しました。  
撮影された画像から、緑色部分の面積を導出しました。  
面積は/Rits-genome-engineering/RasPi/Assets/Assets_Outputのcsvファイルに保存されます。(今後データベースに変更予定。)  
撮影された画像はDropboxに保存されます。  

## 各プログラムの概要
モジュール化により複数のプログラムから構成されています。  
各プログラムの概要は以下の通りです。  

<Main_RasPi.py>  
・このプログラムを動かせばラズベリーパイでシャーレの撮影から葉の面積の保存を行う。  
・下記のdef_Take_the_picture.pyで任意の写真名を記述すればPCでも動作する。  

<def_datetime.py>  
時間を取得する。同時に写真の名前(fname)も作成する。  
ex) fname：MassObservation_S6_2019-09-26-07-00.png  

<def_Take_the_picture.py>  
撮影をする。  
撮影が失敗した場合(撮影せず特定の写真をPC上で読み込ませたい場合)はここを変更する。  

<def_Change_the_color.py>  
撮影したシャーレの写真から葉を検出する。  
葉を緑色とHSV色空間で定義した。  
定義した範囲：[20, 50, 50]〜[70, 255, 255]  

<def_Calculation_from_Contours.py>  
def_Change_the_colorで検出した葉から葉の輪郭を検出する。  
輪郭からは、①面積、②中心座標を導出する。  
ここで一度、面積のデータのみConventional_Record_SX_csvに保存する。  
輪郭はdef_Take_the_pictureで撮影した画像に貼り付けられる。→ Area_fname  

<def_Labeling_by_Coordinates.py>  
Area_fname(輪郭を添付した画像)に個体番号、面積、中心座標も添付する。個体番号は観察初日から最終日まで同一個体に対し同じ番号を付与しなければならない。そのために「前日の座標(ai , bi)に一番近い座標を持つ個体を個体番号iにする。」という条件文を作成した。初日は画像の下にある個体から個体番号を付与する。  
個体番号を前日と揃えたら面積と座標をcsvファイルに保存する。

<def_Identifying_RasPi.py>  
複数のラズベリーパイを識別するために各ラズベリーパイのCPU番号を取得する。  
ラズベリーパイ上で動かさない(PC上で動かす)場合は、予備のラズベリーパイのCPU番号を入力する。  

<def_Send_the_message.py>  
日付、CPU番号、面積を記載したテキストメッセージとArea_fname(情報を添付した画像)をLINEで送信する。  

<def_Save_the_picture.py>  
CPU番号に合わせてDropbox内で各フォルダにfnameとArea_fnameを保存する。  

<def_finish.py>  
ラズベリーパイ内のストレージを圧迫しないように使用した画像は全て削除する。  

## 必要条件
利用確認済みデバイス：RaspberryPi3B、RaspberryPi zero  
利用OS：RaspbianOS stretch

## 使い方
撮影された画像は以下のURL先(Dropboxファイル)で見ることができます。  
-Dropbox保存先 URL-  
https://www.dropbox.com/home/アプリ/ゼニゴケ観察_輪郭と番号/ゼニゴケ観察_輪郭%26番号  
※画像保存先(Dropboxファイル)を変更する場合は、以下のサイトを参考にDropboxに会員登録(無料)し、API(Application Programing Interface：DropboxやLINEなどの企業が自社のサービスをプログラマーが扱うことを可能にするために発行する番号)を発行し、適宜トークンを変更してください。  
-参照サイト： Dropboxファイルの作成・API発行-  
https://engrowth.me/tech/raspdrop/  

## 必要なパッケージのインストール
* OpenCV3.1のインストール 所要時間：３時間３０分
  * 依存ファイル(OpenCVのビルドと実行に必要な機能を持つパッケージ)のインストール
    1.	OpenCVのビルドに必要なパッケージをインストールします。  
      `$ sudo apt-get install build-essential cmake pkg-config`
    2.	JPEG, PNG, TIFなどの様々な画像ファイル形式をOpenCVで使用可能にするための画像I/O(Input/Output=入出力)パッケージをインストールします。  
      `$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev`
    3.	様々なビデオファイル形式を使用可能にするI/Oパッケージもインストールします。  
      `$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev`  
      `$ sudo apt-get install libxvidcore-dev libx264-dev`  
    4.	ライブラリ開発キットをインストールします。  
      `$ sudo apt-get install libgtk2.0-dev`  
    5.	OpenCVに必要な数値を扱う言語であるgfortranと行列計算ライブラリであるlibatlas-base-devをインストールします。  
      `$ sudo apt-get install libatlas-base-dev gfortran`
  * OpenCVソースコードのダウンロード
    1. OpenCVの3.1.0のアーカイブをGithubのOpenCVリポジトリからダウンロードします。  
       ```
       $ cd ~
       $ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
       $ unzip opencv.zip
       ```
    2. 拡張モジュールもインストールするため、 opencv_contribリポジトリも次に示すコマンドでインストールします。
       ```
       $ wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
       $ unzip opencv_contrib.zip
       ```
  * OpenCVのコンパイル／インストール
    1. CMakeを使用してビルドを設定します。
       ```
       $ cd ~/opencv-3.1.0/
       $ mkdir build
       $ cd build
       ```
       ```
       $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
       -D CMAKE_INSTALL_PREFIX=/usr/local \
       -D INSTALL_PYTHON_EXAMPLES=ON \
       -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules\
       -D ENABLE_PRECOMPILED_HEADERS=OFF \
       -D BUILD_EXAMPLES=ON ..
       ```
    2.	次のように、makeでビルドを開始します。約3時間半ビルドにかかります。※RaspberryPi3BのCPUの場合です。  
       `$ make`
       ※参照サイトには$make -j4 とするとCPUを４コア使用でき操作が約90分で終了できると書いてありますが、CPUのキャパオーバーでで途中でビルドが停止するので$makeに変更してあります。
    3.	最後に、ビルドしたOpenCVをRaspberry Pi 3に次のコマンドでインストールします。  
       `$ sudo make install`  
       `$ sudo ldconfig`  

       -参照サイト-  
       https://tomosoft.jp/design/?p=7476  

* その他に必要なパッケージのインストール 所要時間：10分
    葉の面積導出プログラム(Week3_OpenCV_Area.py)をRaspberryPiで実行するためには、OpenCVの他に３つのパッケージをインストールする必要があります。  
    dropboxパッケージ (撮影画像をクラウドストレージに保存するため)、matplotlib (図を扱うため)、scipy (画像を行列値としてpythonプログラム内で扱うため)をインストールします。  
  * dropboxパッケージのインストール  
     最初からRaspbianOSにインストールされているパッケージ管理ツールのapt-getには、Dropboxのパッケージが存在しません。そこでpipというパッケージ管理ツールをインストールする必要があります。  
    1.	pipはapt-getのパッケージとしてインストール可能なため、apt-getを使用してインストールします。  
      `$sudo apt-get install python-pip`
    2.	pipのアップグレードをします。(任意)  
      `$sudo pip install –-upgrade pip`
    3.	pipを使用してDropboxパッケージをインストールします。  
      `$pip3 install dropbox`
      ※sudoは記載せず、pipに3をつけてpip3とします。  
  * matplotlibとscipyのインストール
    1.	表をデスクトップ上で表示するために必要なmatplotlibという名前のパッケージをインストールします。    
    `$sudo apt-get install python3-matplotlib`  
      →定期観測する時はRaspberryPiをモニターに接続しないため、matplotlibをデフォルト設定のままにするとエラーが出ます。そこで、モニターに接続せずにコンパイルを完了するためにmatplotlibのデフォルト設定を変更します。  
      ※デフォルト設定に必要なファイル(matplotlibrc)は、「DISPLAYERROR(モニターに接続していないとmatplotlibは使えませんよ!というエラー)」が表示されてから作成されます。そこで、先に葉の面積導出プログラム(Week3_OpenCV_Area.py)を実行してエラーを出してから、デフォルト設定を編集してください。  
      編集コマンドnanoで、  
    `$sudo nano ~/.config/matplotlib/matplotlibrc`  
      と打つと、空白の編集画面が出てくるので、  
    `backend :Agg`  
      を記入します。(“d”と”:”の間にスペースがあります。)  
    2.	最後に画像を行列値としてpythonプログラム内で扱うために必要なscipyという名前のパッケージをインストールします。  
     `$sudo apt-get install python3-matplotlib`  
       →補足パッケージのインストール終了です。
