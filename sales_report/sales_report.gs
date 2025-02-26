function collectSalesData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const dataSheet = ss.getSheetByName("売上データ");
  const summarySheet = ss.getSheetByName("集計表");

  if (!dataSheet || !summarySheet) {
    Logger.log("シートが見つかりません。");
    return;
  }

  // 売上データの取得
  const data = dataSheet.getDataRange().getValues();
  if (data.length <= 1) return; // データがない場合は終了（ヘッダー行を除く）

  const salesMap = new Map();

  for (let i = 1; i < data.length; i++) {
    let date = data[i][0]; // 日付
    let amount = data[i][4]; // 売上

    if (!date || !amount) continue; // 空の行をスキップ
    date = Utilities.formatDate(new Date(date), Session.getScriptTimeZone(), "yyyy/MM/dd");

    if (salesMap.has(date)) {
      salesMap.set(date, salesMap.get(date) + amount);
    } else {
      salesMap.set(date, amount);
    }
  }

  // 集計表のクリア＆ヘッダー追加
  summarySheet.clear();
  summarySheet.appendRow(["日付", "合計売上"]);

  // 集計データの書き込み
  salesMap.forEach((value, key) => {
    summarySheet.appendRow([key, value]);
  });

  Logger.log("集計が完了しました！");
}
