# 本リポジトリについて
このリポジトリでは、スキルを示すポートフォリオ用のサンプルコードを公開しています。  
商用利用や実運用を目的としたものではございません。  
また、スクリプトの流用や改造による再配布はお控えください。
## 各フォルダの説明  
### portfolio-web-scraping

#### 概要
Webスクレイピングしたデータを一覧化し、CSVやGoogleスプレッドシートに保存するツールです。このリポジトリには、スクレイピングアプリケーションに関連するコードやリソースをまとめています。
- **`webscraper.py`**: スクレイピングスクリプト。  
- **`urls.csv`**: スクレイピング対象のURLリスト。

※Googleスプレッドシートとの連携や.iniファイルの読み込み処理を実装していますが、認証情報ファイルおよび.iniファイルはこのリポジトリには含まれていません。

#### 特徴
- スクレイピングスクリプトを使用して指定されたURLからデータを収集。
- 収集データをCSV形式で保存可能。
- Googleスプレッドシートとの連携機能を実装。
- `.ini`ファイルを用いた柔軟な設定管理。

#### 動作環境
以下の環境で動作確認を行っています：  
- Python:3.12.4
- Spyder:5.5.1

### Laravel Basic

#### 概要
Laravelを使用した簡易的なプロジェクトです。現在は、静的なページを表示する機能のみを実装しています。

#### 特徴
- 静的ページのルーティング
- Laravelの基本構造を利用
- シンプルなコード

#### 動作環境
以下の環境で動作確認を行っています：
- PHP: 8.2.12
- Composer: 2.8.4
- Laravel Framework:10.48.25
- Webサーバー: Xampp
