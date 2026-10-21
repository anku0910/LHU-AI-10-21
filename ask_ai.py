"""第三堂：問題進模型，文字答案回程式。--demo 與 --simulate 都不連線。"""
import argparse
import json
from pathlib import Path
from gemini_client import ClassroomError, ask_model, extract_text, http_message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="離線流程示範，不呼叫模型")
    parser.add_argument("--simulate", choices=["timeout", "quota", "missing_key"],
                        help="離線錯誤示範，不呼叫模型")
    args = parser.parse_args()
    try:
        config = json.loads(Path(__file__).with_name("config.json").read_text(encoding="utf-8"))
        for key in ("model", "timeout_seconds", "system_prompt"):
            if key not in config:
                raise ValueError(f"缺少 {key}")
        if float(config["timeout_seconds"]) <= 0:
            raise ValueError("timeout 必須大於 0")
    except (OSError, ValueError, TypeError):
        print("讀不到正確設定。請確認 config.json 的 model、timeout_seconds 與 system_prompt。")
        return

    if args.simulate:
        print("離線錯誤示範：未呼叫模型，未消耗 API 額度。")
        messages = {
            "timeout": f'等待超過 {config["timeout_seconds"]} 秒，這次沒有收到答案。請查看網路，稍後再試。',
            "quota": "HTTP 429：" + http_message(429),
            "missing_key": "尚未設定 GEMINI_API_KEY。請設定環境變數，再完整關閉並重開 OpenCode 與 PowerShell。",
        }
        print(messages[args.simulate])
        return

    print("離線流程示範：固定範例答案，未呼叫模型。" if args.demo
          else f'模型 API 問答（{config["model"]}，輸入 q 離開）')
    while True:
        question = input("你的問題：").strip()
        if question.lower() == "q":
            break
        if not question:
            print("請先輸入問題。")
            continue
        try:
            if args.demo:
                payload = {"candidates": [{"content": {"parts": [{"text":
                    "【固定範例，未呼叫模型】變數像貼了名稱的盒子，可以存放資料。\n例如 score = 80，score 就存著分數 80。"}]}}]}
                answer = extract_text(payload)
            else:
                answer = ask_model(question, config)
            print("AI 回答：\n" + answer)
        except (ClassroomError, KeyError, TypeError, ValueError) as error:
            if isinstance(error, ClassroomError):
                print("這次未取得答案：" + str(error))
            else:
                print("設定或回應格式有問題，請確認 config.json 與教材版本。")


if __name__ == "__main__":
    main()
