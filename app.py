from flask import Flask, request
import telegram
import dotenv
import os
import MySQLdb
import datetime
import praw
from prawcore import NotFound

dotenv.load_dotenv()

global BOT_API_KEY
global bot

BOT_API_KEY = os.getenv("BOT_API_KEY")
BOT_NAME = os.getenv("BOT_NAME")
URL = os.getenv("URL")

bot = telegram.Bot(token=BOT_API_KEY)
app = Flask(__name__)
chat_id_g = 0

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_API_ID"),
    client_secret=os.getenv("REDDIT_API_KEY"),
    user_agent="muj ulubiony bot2",
)

connection = MySQLdb.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd=os.getenv("DB_PASSWORD"),
  db=os.getenv("DB_NAME"),
  ssl={
    "ca": "/etc/ssl/cert.pem"
  })

c = connection.cursor()

@app.route('/api/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=BOT_API_KEY))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/api/deletewebhook', methods=['GET', 'POST'])
def delete_webhook():
    s = bot.deleteWebhook()
    if s:
        return "webhook deleted"
    else:
        return "webhook not deleted"

@app.route('/api/{}'.format(BOT_API_KEY), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if (update.message is None):
        return "ok"

    chat_id = update.message.chat.id
    global chat_id_g
    chat_id_g = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    user_id = update.message.from_user.id

    if "/start" in text:
        bot.sendMessage(chat_id=chat_id, text="ok, instructions", reply_to_message_id=msg_id)
    if "/subscribe" in text:
        text_list = text.split()
        start_index = text_list.index("/subscribe")
        if len(text_list) > start_index + 2:
            subreddit = text_list[start_index + 1]
            try:
                int(text_list[start_index + 2])
            except ValueError:
                bot.sendMessage(chat_id=chat_id, text=f"Second argument (Upvote threshold needs to be an integer!)", reply_to_message_id=msg_id)
            upvote_threshold = int(text_list[start_index + 2])
            if (upvote_threshold > 0):
                try:
                    # reddit.subreddits.search_by_name("leagueoflegends", exact=True)
                    c.execute(f"""
                        INSERT INTO subscriptions
                        (id, chat_id, subreddit_name, date_of_subscription, upvotes_threshold)
                        VALUES (1, "{chat_id}", "{subreddit}", "{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", {upvote_threshold})
                    """)
                    bot.sendMessage(chat_id=chat_id, text=f"Subscribed to {subreddit}!", reply_to_message_id=msg_id)
                except NotFound:
                    bot.sendMessage(chat_id=chat_id, text=f"Subreddit {subreddit} wasn't found!", reply_to_message_id=msg_id)
            else:
                bot.sendMessage(chat_id=chat_id, text=f"Upvotes threshold needs to be higher than 0!", reply_to_message_id=msg_id)
        else:
            bot.sendMessage(chat_id=chat_id, text="Your subscription command was missing one of the two arguments: subreddit name or upvote threshold!", reply_to_message_id=msg_id)

    return "ok"

@app.route('/api/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
