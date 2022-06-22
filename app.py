from flask import Flask, request, jsonify
import telegram
import dotenv
import os
import datetime
from prawcore import NotFound
import settings

settings.init()

app = Flask(__name__)

@app.route('/api/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    response = settings.bot.setWebhook('{URL}{HOOK}'.format(URL=settings.URL, HOOK=settings.BOT_API_KEY))
    if response:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/api/deletewebhook', methods=['GET', 'POST'])
def delete_webhook():
    response = bot.deleteWebhook()
    if response:
        return "webhook deleted"
    else:
        return "webhook not deleted"

@app.route('/api/{}'.format(settings.BOT_API_KEY), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), settings.bot)

    if (update.message is None):
        return "ok"

    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()
    user_id = update.message.from_user.id

    if "/start" in text:
        settings.bot.sendMessage(chat_id=chat_id, text="Hello and welcome to your new news source! To subscribe to a subreddit type '/subscribe name_of_subreddit upvote_threshold'. To unsubscribe type '/unsubscribe name_of_subreddit upvote_threshold'.")
    if "/subscribe" in text:
        text_list = text.split()
        start_index = text_list.index("/subscribe")
        if len(text_list) > start_index + 2:
            subreddit = text_list[start_index + 1]
            try:
                int(text_list[start_index + 2])
            except ValueError:
                settings.bot.sendMessage(chat_id=chat_id, text=f"Second argument (Upvote threshold needs to be an integer!)", reply_to_message_id=msg_id)
                return "403"
            upvote_threshold = int(text_list[start_index + 2])
            if (upvote_threshold > 0):
                try:
                    if len(settings.reddit.subreddits.search_by_name(subreddit, exact=True)) == 0:
                        settings.bot.sendMessage(chat_id=chat_id, text=f"There is no subreddit named {subreddit}!", reply_to_message_id=msg_id)
                        return "404"
                    settings.cursor.execute(f"""
                        SELECT * FROM subscriptions
                        WHERE chat_id="{chat_id}" AND subreddit_name="{subreddit}"
                    """)
                    subscriptions = settings.cursor.fetchall()
                    if (len(subscriptions) == 0):
                        settings.cursor.execute(f"""
                            INSERT INTO subscriptions
                            (chat_id, subreddit_name, date_of_subscription, upvotes_threshold)
                            VALUES ("{chat_id}", "{subreddit}", "{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", {upvote_threshold})
                        """)
                        settings.connection.commit()
                        settings.bot.sendMessage(chat_id=chat_id, text=f"Subscribed to {subreddit}!", reply_to_message_id=msg_id)
                    else:
                        settings.bot.sendMessage(chat_id=chat_id, text=f"You are already subscribed to {subreddit}!", reply_to_message_id=msg_id)
                except NotFound:
                    settings.bot.sendMessage(chat_id=chat_id, text=f"Subreddit {subreddit} wasn't found!", reply_to_message_id=msg_id)
            else:
                settings.bot.sendMessage(chat_id=chat_id, text=f"Upvotes threshold needs to be higher than 0!", reply_to_message_id=msg_id)
        else:
            settings.bot.sendMessage(chat_id=chat_id, text="Your subscription command was missing one of the two arguments: subreddit name or upvote threshold!", reply_to_message_id=msg_id)

    if "/unsubscribe" in text:
        text_list = text.split()
        start_index = text_list.index("/unsubscribe")
        if len(text_list) > start_index + 1:
            subreddit = text_list[start_index + 1]
            try:
                settings.cursor.execute(f"""
                    DELETE FROM subscriptions
                    WHERE chat_id="{chat_id}" AND subreddit_name="{subreddit}"
                """)
                settings.connection.commit()
                settings.bot.sendMessage(chat_id=chat_id, text=f"Unsubscribed the {subreddit} subreddit!", reply_to_message_id=msg_id)
            except NotFound:
                settings.bot.sendMessage(chat_id=chat_id, text=f"Subreddit {subreddit} wasn't found!", reply_to_message_id=msg_id)
        else:
            settings.bot.sendMessage(chat_id=chat_id, text="Your subscription command was missing the subreddit name!", reply_to_message_id=msg_id)

    return "ok"

@app.route('/api/')
def index():
    return '.'

if __name__ == '__main__':
    app.run(threaded=True)
