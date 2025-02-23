# 本リポジトリについて
このリポジトリでは、スキルを示すポートフォリオ用のサンプルコードを公開しています。  
商用利用や実運用を目的としたものではございません。  
また、スクリプトの流用や改造による再配布はお控えください。
## 各フォルダの説明  
### cosmetics
#### 概要
化粧品のランディングページ（LP）です。  
デザインをFigmaで作成し、HTML・CSS・JavaScriptを使用して忠実にコーディングしました。

#### 特徴
- **レスポンシブ対応**: スマートフォン、デスクトップに対応。  
- **ハンバーガーメニュー**: スマートフォン用の画面で、メニュー切り替え機能を実装。

#### 動作環境
- 現在、以下のリンクからアクセス可能です：  
- *https://cosmetics.shimoza.site/* 

### Laravel-Basic

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
- Webサーバー: XAMPP  

### portfolio-web-scraping

#### 概要
Webスクレイピングしたデータを一覧化し、CSVやGoogleスプレッドシートに保存するツールです。このリポジトリには、スクレイピングアプリケーションに関連するコードやリソースをまとめています。
- **`webscraper.py`**: スクレイピングスクリプト。  
- **`urls.csv`**: スクレイピング対象のURLリスト。

**注意:**  
Googleスプレッドシートとの連携や.iniファイルの読み込み処理を実装していますが、認証情報ファイルおよび.iniファイルはこのリポジトリには含まれていません。

#### 特徴
- スクレイピングスクリプトを使用して指定されたURLからデータを収集。
- 収集データをCSV形式で保存可能。
- Googleスプレッドシートとの連携機能を実装。
- `.ini`ファイルを用いた柔軟な設定管理。

#### 動作環境
以下の環境で動作確認を行っています：  
- Python:3.12.4
- Spyder:5.5.1

### payroll_system

#### 概要
Djangoを使用して開発した簡易的な給与明細管理システムです。
従業員の給与データを管理し、動的に一覧表示できる機能を実装しています。

#### 特徴
・従業員名、給与、発行日を管理
・日本語の日付表記対応
・給与金額の小数点非表示
・Djangoの管理画面からデータの追加・編集・削除が可能
・SQLiteデータベースを使用

#### 動作環境
以下の環境で動作確認を行っています。
・Python: 3.12.4
・Django: 5.1.6
・データベース: SQLite
・OS: Windows 10

