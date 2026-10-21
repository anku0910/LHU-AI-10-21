"""使用 Gemini generateContent REST API。只用 Python 標準函式庫。"""
import json
import os
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class ClassroomError(Exception):
    """可以直接給學生看的錯誤訊息。"""


def extract_text(payload):
    try:
        parts = payload.get("candidates", [])[0]["content"]["parts"]
        texts = [part["text"] for part in parts
                 if isinstance(part, dict) and isinstance(part.get("text"), str)
                 and not part.get("thought", False)]
    except (IndexError, KeyError, TypeError, AttributeError):
        texts = []
    answer = "\n".join(texts).strip()
    if not answer:
        raise ClassroomError("模型沒有回傳文字答案。可能受內容限制，或回應格式不同，請換一個簡單問題。")
    return answer


def http_message(status):
    if status in (401, 403):
        return "金鑰或專案權限有問題。請私下確認自己的金鑰與 API 存取資格。"
    if status == 400:
        return "請求格式或設定不正確。請確認金鑰、模型設定及程式送出的資料格式。"
    if status == 404:
        return "找不到模型或 API 路徑。請核對 config.json 的模型名稱與專案可用模型。"
    if status == 429:
        return "請求過多或額度不足。請查看 AI Studio 專案配額，稍後再試，不要連續重送。"
    if status >= 500:
        return "模型服務暫時有問題。請稍後再試。"
    return f"API 回傳 HTTP {status}。請把狀態碼與操作步驟記錄下來，勿貼出金鑰。"


def ask_model(question, config):
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ClassroomError("尚未設定 GEMINI_API_KEY。請設定環境變數，再完整關閉並重開 OpenCode 與 PowerShell。")
    model = str(config["model"]).strip()
    timeout = float(config["timeout_seconds"])
    if not model or timeout <= 0:
        raise ClassroomError("模型名稱不可空白，等待秒數必須大於 0。")
    endpoint = ("https://generativelanguage.googleapis.com/v1beta/models/"
                + quote(model, safe="") + ":generateContent")
    body = {
        "systemInstruction": {"parts": [{"text": config["system_prompt"]}]},
        "contents": [{"role": "user", "parts": [{"text": question}]}],
    }
    request = Request(endpoint, data=json.dumps(body).encode("utf-8"), method="POST",
                      headers={"Content-Type": "application/json", "x-goog-api-key": api_key})
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
        print(json.dumps(payload, ensure_ascii=False, indent=2))  # 取消註解可在終端機查看回傳 JSON
        return extract_text(payload)
    except HTTPError as error:
        # 不把 HTTP 原文或 request 印出，避免錯誤內容含有私人資料。
        raise ClassroomError(f"HTTP {error.code}：{http_message(error.code)}") from None
    except (TimeoutError, socket.timeout):
        raise ClassroomError(f"等待超過 {timeout:g} 秒，這次沒有收到答案。請查看網路，稍後再試。") from None
    except URLError as error:
        if isinstance(error.reason, (TimeoutError, socket.timeout)):
            raise ClassroomError(f"等待超過 {timeout:g} 秒，這次沒有收到答案。請查看網路，稍後再試。") from None
        raise ClassroomError("網路連線失敗。請確認可連上 Gemini API，或向老師說明教室網路限制。") from None
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ClassroomError("收到的資料不是預期的 JSON 回應，請稍後重試或記錄問題。") from None
