from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Get Line Token & SQL Password
sql_password = os.environ.get("SQL_PASSWORD")
channel_acccess_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("LINE_CHANNEL_SECRET")

today = datetime.today().strftime(format="%Y%m%d")
stockSelectorDB = mysql.connector.connect(host = "us-cdbr-east-04.cleardb.com", user = "b8aabaa725cfb0", password = sql_password, database = "heroku_cec98989109bf67")
sql_select_Query = "select * from dailyselectresult where Date = " + today
mycursor = stockSelectorDB.cursor()
mycursor.execute(sql_select_Query)
# get all records
records = mycursor.fetchall()


# LINE聊天機器人基本資料
line_bot_api = LineBotApi(channel_acccess_token)
handler = WebhookHandler(channel_secret)

# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def echo(event):
    
    content = "⭐️⭐️⭐️本日財富自由精選股⭐️⭐️⭐️\n"
    for index in range(len(records)):
        content += records[index][1]+"\n"

    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )

if __name__ == "__main__":
    app.run()