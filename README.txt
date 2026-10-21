第三堂課：讓 Python 程式接上 AI 模型

本堂目標：輸入問題，呼叫一次模型 API，印出回答，處理金鑰、逾時與額度問題。
本堂尚未接公告資料、工具選擇、MCP 或 Skill。第四堂再處理自己的資料，第五堂才做模型選工具。
只使用 Python 標準函式庫，不需要 pip install。

一、自己的模型服務帳號
1. https://aistudio.google.com/api-keys 登入符合資格的 Google 帳號。
2. 看是否已有自己的專案／金鑰，沒有則 Create API key 選或建自己的專案。
3. 自行閱讀服務條款。查看專案可用模型與免費配額，課程不要求付費或綁卡。
4. config.json 預設 gemini-3.5-flash-lite，有免費層且回應較快；若專案不提供此模型，
   改成該專案支援 generateContent 且有免費層的文字模型完整 ID。
   不要盲目切到付費模型。配額與模型名可能調整，以自己的專案為準。

二、設定金鑰，金鑰不放原始碼或教材
Windows：搜尋「編輯帳戶的環境變數」，在「使用者變數」新增。
名稱：GEMINI_API_KEY；值：自己的金鑰。儲存後完整關閉 OpenCode 與 PowerShell 再重開。
Mac：在自己私下使用的終端機設定 export GEMINI_API_KEY="自己的金鑰"。
Mac 這個設定只在該終端機工作階段有效，在同一終端機執行 python3 ask_ai.py。
不要把真實金鑰貼給 Coding Agent、投影、寫入 Git 或作業、上傳共享雲端。
判斷是否設定只看有／沒有，不要印出金鑰。
設定畫面仍可能顯示完整金鑰。截圖時保留變數名稱、遮住值，問問題時只貼錯誤訊息。
新開 PowerShell 後，執行下列指令，只顯示 True／False：
python -c "import os; print(bool(os.environ.get('GEMINI_API_KEY')))"
True 只代表 Python 讀得到值，仍需完成下一節的真實 API 呼叫。

三、首次執行
1. 在 OpenCode 開啟包含 ask_ai.py、gemini_client.py、config.json 的資料夾。
2. 終端機 python --version（Mac 用 python3）。
3. python ask_ai.py（Mac 用 python3 ask_ai.py）。
4. 問「請用兩句話解釋變數，給資管大三學生看。」
5. 答案不必與老師一字不差，確認變數與例子是否正確。輸入 q 離開。
6. 修改 config.json 的 system_prompt，例如「先給一句定義，再給一個 Python 例子」。
7. 重開程式、問同一問題，比較回答。

四、無金鑰／額度不足時的替代練習（必須標明未完成真實 API 連線）
python ask_ai.py --demo
這是固定答案的離線流程示範，任何問題都用固定範例答案，不可當作模型真的回答。
python ask_ai.py --simulate timeout
python ask_ai.py --simulate quota
python ask_ai.py --simulate missing_key
以上只印教學用錯誤訊息，不會送出請求。之後需補做真實 API 成功測試。

五、交付
程式檔、config.json（不含金鑰）、自己的 README、填好的測試紀錄、
成功呼叫畫面及錯誤處理畫面。模擬結果要註記，不能代替真實串接成功紀錄。
檢查截圖沒有金鑰、信箱、私人資料。重點是能重跑，知道設定放哪、失敗怎麼判斷。

API 參考與查核日期：2026-10-03
https://ai.google.dev/api/generate-content
https://ai.google.dev/gemini-api/docs/api-key
https://ai.google.dev/gemini-api/docs/rate-limits
https://ai.google.dev/gemini-api/docs/pricing
https://ai.google.dev/gemini-api/docs/troubleshooting
