from flask import Flask, request
import telegram
import dotenv
import os

dotenv.load_dotenv()

global BOT_API_KEY
global bot

BOT_API_KEY = os.getenv("BOT_API_KEY")
BOT_NAME = os.getenv("BOT_NAME")
URL = os.getenv("URL")

bot = telegram.Bot(token=BOT_API_KEY)
app = Flask(__name__)

@app.route('/api/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=BOT_API_KEY))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/api/{}'.format(BOT_API_KEY), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    bot.sendMessage(chat_id=chat_id, text="bla", reply_to_message_id=msg_id)
    return "ok"

@app.route('/api')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
