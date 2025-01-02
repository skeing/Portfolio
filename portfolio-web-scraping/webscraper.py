# -*- coding: utf-8 -*-
# 標準ライブラリ
import os
import sys
import logging

# 外部ライブラリ
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# GUI関連ライブラリ
from tkinter import messagebox

# Google API関連ライブラリ
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class WebScraper:
    MAX_RETRIES = 3 # リトライ回数
    TARGET_ID = "parent" # 取得したいID
    
    """ WebScraperの初期化 """        
    def __init__(self, base_url, logger, current_dir):
        # ブラウザを用意
        self.driver = webdriver.Chrome()
        
        # スクレイピングするURL
        self.base_url = base_url
        
        # ロギング
        self.logger = logger
        
        #　カレントディレクトリ
        self.current_dir = current_dir
        
        # HTML
        self.soup = None
        
        # 天気と場所を入れるリスト
        self.data = []
    
    """ 起点となる処理 """
    def main(self):
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                """ スクレイピング処理 """
                self.logger.info(f"スクレイピングを実行します（{attempt}回目の試行）")
                
                self.scraping()
                
                """ csvに保存処理 """
                self.save_to_csv()
                
                """ スプレッドシートに出力処理 """
                self.upload_csv()
                
                """ 終了処理 """
                # スクレイピング完了通知
                messagebox.showinfo("スクレイピング完了", "データの取得と出力が完了しました。")
                
                self.logger.info("スクレイピングが正常に完了しました。")
                
                break
            except TimeoutException:
                self.logger.warning(f"タイムアウトが発生しました（{attempt}回目）。リトライします...")
                if attempt == self.MAX_RETRIES:
                    self.logger.error("タイムアウトにより最大試行回数に到達しました。")
            except Exception as e:
                self.logger.error(f"予期しないエラーが発生しました（{attempt}回目）：{e}")
                if attempt == self.MAX_RETRIES:
                    self.logger.error("予期しないエラーにより最大試行回数に到達しました。")
    
    """　ハンドラーの定義(関数実行用) """
    def handler(self, function):
        return function()

    """　csvに保存処理 """
    def save_to_csv(self):
        try:
            df = pd.DataFrame(self.data)
            
            # パス
            csv_filename = "data.csv"
            csv_path = os.path.join(self.current_dir, csv_filename)
            
            # 保存
            df.to_csv(csv_path, encoding="shift-jis", index=False)
        except Exception as e:
            self.logger.error(f"CSVに保存できませんでした: {e}")
    
    """ スプレッドシートに保存処理 """
    def upload_csv(self):
        try:
            """ 認証 """            
            # 実行環境に応じて認証設定を行う必要があります
            spreadsheet_id = "your_spreadsheet_id_here"
            key_file = os.path.join(self.current_dir, "json_file_name.json") # 認証が必要な場合は、json_file_name.jsonのパスを指定してください。
            credentials = Credentials.from_service_account_file(key_file)
            service = build('sheets', 'v4', credentials=credentials)
            
            # ヘッダー
            headers = ["場所", "天気"]

            # データを取得（辞書の値）
            rows = [list(d.values()) for d in self.data]

            # ヘッダーとデータを結合
            formatted_data = [headers] + rows
            
            # シート名とセル範囲を確認
            range_name = "シート1!A1"  
            
            # データをそのままの形でスプレッドシートにデータを送信
            sheet_api = service.spreadsheets().values()
            request_body = {"values": formatted_data}  # スプレッドシートに送るデータ
            sheet_api.update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=request_body
            ).execute()

            self.logger.info("スプレッドシートにアップロードしました")
        except Exception as e:
            self.logger.error(f"スプレッドシートに保存できませんでした: {e}")
            
    """　スクレイピング処理 """
    def scraping(self):
        self.access()
        self.web_driver_wait()
        self.html_parser()
        self.extract()
    
    """　場所と天気を抽出 """
    def extract(self):        
        for content in self.soup.find_all(class_='contents'):
            location = content.find('h2').get_text(strip=True)
            weather = content.find('p').get_text(strip=True)
            self.data.append({'場所': location, '天気': weather})

    """　スクレイピング対象のWebサイトにアクセス """
    def access(self):
        try:
            self.driver.get(self.base_url)
        except Exception as e:
            self.logger.error(f"{self.base_url}にアクセスできませんでした: {e}")
    
    """　ターゲットのidが見つかるまで待機 """
    def web_driver_wait(self):
        try:
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, self.TARGET_ID)))    
        except Exception as e:
            self.logger.error(f"取得対象:{self.TARGET_ID}が見つかりませんでした: {e}")
        
    """　データ抽出関数 """
    def html_parser(self):
        try:
            html = self.driver.page_source
            self.soup = BeautifulSoup(html, 'html.parser')
        except Exception as e:
            self.logger.error(f"BeautifulSoupによるデータ抽出ができませんでした: {e}")
    
    """　「場所」と「天気」を取り出す """
    def get_location_and_weather(self):
        pass        
    
    """ スクレイピング結果表示 """
    def print_result(self, result):
        print(f"スクレイピング結果:{result}")     
    
    """ ブラウザを閉じる """
    def close_browser(self):
        self.driver.quit()          
                
if __name__ == '__main__':
    """ タスクスケジューラ定義 """
    # 現在のスクリプトのディレクトリを取得
    if getattr(sys, 'frozen', False):
        # タスクスケジューラによって実行されている場合
        current_dir = os.path.dirname(sys.executable)
    else:
        # 通常のPython実行の場合
        current_dir = os.path.dirname(os.path.abspath(__file__))
    
    """ ログ定義 """
    # exeファイルと同じディレクトリにログファイルにする
    log_file_path = os.path.join(current_dir, 'scraping.log')
    
    # ログの設定
    logging.basicConfig(level=logging.INFO, 
                                  format='%(asctime)s - %(levelname)s - %(message)s',
                                  filename=log_file_path,
                                  filemode='a')
        
    # ロガーの設定・取得
    logger = logging.getLogger(__name__)
    
    """ スクレイピング準備 """
    # CSVファイル(スクレイピングするURL)の読み込み(実行時には、URLリストを含むCSVファイルを準備してください)
    df = pd.read_csv("data/urls.csv")
    
    # スクレイピング対象のURLを取り出す
    base_url = df.loc[df['URL_ID'] == 1, 'URL'].values[0]
    
    #　インスタンス生成
    scraper = WebScraper(base_url, logger, current_dir)
    
    """ スクレイピング開始 """
    try:
        scraper.main()
    finally:
        scraper.close_browser()  # 必ずブラウザを閉じる