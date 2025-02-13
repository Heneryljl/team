import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 從環境變數中讀取 Channel Secret 和 Channel Access Token
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 Line 發送過來的簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求的正文內容
    body = request.get_data(as_text=True)

    try:
        # 驗證簽名
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 監聽文本消息事件
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回傳與收到的訊息相同的內容
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    # 使用 Vercel 預設端口
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
