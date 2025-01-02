# -*- coding: utf-8 -*-
# 標準ライブラリ
import os
import sys
import logging
import configparser

# 外部ライブラリ
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# GUI関連ライブラリ
from tkinter import Tk, messagebox

# Google API関連ライブラリ
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class WebScraper:
    # リトライ回数
    MAX_RETRIES = 3
    
    """ WebScraperの初期化 """        
    def __init__(self, config, logger):
        # ブラウザを用意
        self.driver = webdriver.Chrome()
        
        # スクレイピングするURL
        self.base_url = config['base_url']
        
        #　カレントディレクトリ
        self.current_dir = config['current_dir']
        
        # スプレッドシートid
        self.google_spreadsheet_id = config['google_spreadsheet_id']
        
        # 出力するcsvのパスの末尾
        self.csv_output_path = config['csv_output_path']
        
        # JSONファイル
        self.service_account_json = config['service_account_json']
        
        # ロギング
        self.logger = logger
        
        # データ用リスト
        self.location_weather_data = []
        
        # 取得したいid
        self.target_element_id = config['target_element_id']
    
    def main(self):
        success = False  # 通知表示の制御用フラグ
        """ 起点となる処理 """
        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                """ スクレイピング処理 """
                self.logger.info(f"[INFO] スクレイピングを開始します: {attempt}回目")
                
                self.scraping()
                
                """ csvに保存処理 """
                self.save_to_csv()
                
                """ スプレッドシートに出力処理 """
                self.upload_csv()
                
                """ 終了処理 """
                success = True
                self.logger.info("[INFO] スクレイピングが正常に完了しました。")
                
                break
            except TimeoutException:
                self.logger.warning(f"[WARNING] タイムアウトが発生しました（{attempt}回目）。リトライします...")
                if attempt == self.MAX_RETRIES:
                    self.logger.error("[ERROR] タイムアウトにより最大試行回数に到達しました。")
            except Exception as e:
                self.logger.error(f"[ERROR] 予期しないエラーが発生しました（{attempt}回目）：{e}")
                if attempt == self.MAX_RETRIES:
                    self.logger.error("[ERROR] 予期しないエラーにより最大試行回数に到達しました。")
        
        # 完了通知
        if success:
            self.show_message("スクレイピング完了", "データの取得と出力が完了しました。")
    
    def scraping(self):
        try:
            """　スクレイピング対象のWebサイトにアクセス """
            try:
                self.driver.get(self.base_url)
            except Exception as e:
                self.logger.error(f"[ERROR] {self.base_url} にアクセスできませんでした: {e}")
            
            
            """　ターゲットのidが見つかるまで待機 """
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, self.target_element_id)))    
            except Exception as e:
                self.logger.error(f"[ERROR] 取得対象:{self.target_id}が見つかりませんでした: {e}")
            
            """　データ抽出関数 """
            try:
                html = self.driver.page_source
                self.soup = BeautifulSoup(html, 'html.parser')
            except Exception as e:
                self.logger.error(f"[ERROR] BeautifulSoupによるHTML解析が失敗しました: {e}, HTML内容: {html[:100]}...")
        
            """　「場所」と「天気」を取り出す """
            try:
                for content in self.soup.find_all(class_='contents'):
                    location = content.find('h2').get_text(strip=True)
                    weather = content.find('p').get_text(strip=True)
                    self.location_weather_data.append({'場所': location, '天気': weather})
            except Exception as e:
                self.logger.error(f"[ERROR] 場所と天気の抽出ができませんでした: {e}")
        
        except Exception as e:
            print(f"スクレイピング中にエラーが発生しました: {e}")
            self.logger.error(f"[ERROR] スクレイピング中にエラーが発生しました: {e}")
    
    def save_to_csv(self):
        """　csvに保存処理 """
        try:
            df = pd.DataFrame(self.location_weather_data)
            
            # パス
            csv_output_path = os.path.join(self.current_dir, self.csv_output_path)
            
            # 保存messagebox.showinfo("スクレイピング完了", "データの取得と出力が完了しました。")
            if not os.path.exists(csv_output_path) or self.show_message("上書き確認", "csvを上書きしますがよろしいでしょうか", message_type="yesno"):
                df.to_csv(csv_output_path, encoding="shift-jis", index=False)
                self.logger.info("[INFO] CSVを保存しました。")
            else:
                self.logger.info("[INFO] CSVの保存をキャンセルしました。")

        except Exception as e:
            self.logger.error(f"[ERROR] CSVに保存できませんでした: {e}, 出力パス: {csv_output_path}")
    
    def upload_csv(self):
        """ スプレッドシートに保存処理 """
        try:
            """ 認証 """            
            # 実行環境に応じて認証設定を行う必要があります
            key_file = os.path.join(self.current_dir, self.service_account_json)
            credentials = Credentials.from_service_account_file(key_file)
            service = build('sheets', 'v4', credentials=credentials)
            
            # ヘッダー
            headers = ["場所", "天気"]

            # データを取得（辞書の値）
            rows = [list(d.values()) for d in self.location_weather_data]

            # ヘッダーとデータを結合
            formatted_data = [headers] + rows
            
            # シート名とセル範囲を確認
            range_name = "シート1!A1"  
            
            # データをそのままの形でスプレッドシートにデータを送信
            sheet_api = service.spreadsheets().values()
            request_body = {"values": formatted_data}  # スプレッドシートに送るデータ
            sheet_api.update(
                spreadsheetId=self.google_spreadsheet_id,
                range=range_name,
                valueInputOption="RAW",
                body=request_body
            ).execute()

            self.logger.info("[INFO] スプレッドシートにアップロードしました")
        except Exception as e:
            self.logger.error(f"[ERROR] スプレッドシートに保存できませんでした: {e}")
    
    # 完了通知を最前面に表示
    def show_message(self, title, message, message_type="info"):
        root = Tk()
        root.withdraw()
        root.wm_attributes("-topmost", 1)
        result = None
        if message_type == "info":
            messagebox.showinfo(title, message)
        elif message_type == "yesno":
            result = messagebox.askyesno(title, message)
        root.destroy()
        return result
    
    def close_browser(self):
        """ ブラウザを閉じる """
        try:
            self.driver.quit()
            self.logger.info("[INFO] ブラウザを正常に閉じました。")
        except Exception as e:
            self.logger.warning(f"[WARNING] ブラウザを閉じる際にエラーが発生しました: {e}")          
                
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
    
    # googleapiclient.discovery_cache のログレベルをエラーに設定
    logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
    
    """ スクレイピング準備 """
    # 設定ファイル
    config = configparser.ConfigParser()
    config_path = os.path.join(current_dir, "scraper_config.ini")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {config_path}")
    config.read(config_path)
    
    # csv,スプレッドシートid,JSONファイル。google_spreadsheet_id,service_account_json,target_element_idのfallbackはダミー
    csv_input_path = config.get("DEFAULT", "CsvInputPath", fallback="data/urls.csv")
    csv_output_path = config.get("DEFAULT", "CsvOutputPath", fallback="output/data.csv")
    google_spreadsheet_id = config.get("SPREADSHEET", "GoogleSpreadsheetId", fallback="default_spreadsheet_id")
    service_account_json = config.get("JSON", "ServiceAccountJson", fallback="credentials.json")
    target_element_id = config.get("TARGET", "TargetElementId", fallback="sample") # 取得したいid
    
    # CSVファイル(スクレイピングするURL)の読み込み(実行時には、URLリストを含むCSVファイルを準備してください)
    df = pd.read_csv(csv_input_path)
    
    # スクレイピング対象のURLを取り出す
    base_url = df.loc[df['URL_ID'] == 1, 'URL'].values[0]
    
    #　インスタンス生成
    config = {
        'base_url': base_url,
        'current_dir': current_dir,
        'target_id': target_element_id,
        'google_spreadsheet_id': google_spreadsheet_id,
        'csv_output_path': csv_output_path,
        'service_account_json': service_account_json,
        'target_element_id': target_element_id
    }
    
    scraper = WebScraper(config, logger)

    """ スクレイピング開始 """
    try:
        scraper.main()
    finally:
        scraper.close_browser()  # 必ずブラウザを閉じる
