import praw
import dotenv
import os
import MySQLdb
import time
import datetime
import telegram
from prawcore import NotFound

print("Starting scraping worker")

dotenv.load_dotenv()

BOT_API_KEY = os.getenv("BOT_API_KEY")
bot = telegram.Bot(token=BOT_API_KEY)

print(os.getenv("REDDIT_API_ID"), os.getenv("REDDIT_API_KEY"))
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_API_ID"),
    client_secret=os.getenv("REDDIT_API_KEY"),
    user_agent="muj ulubiony bot",
)

connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DB_NAME"),
    ssl={
    "ca": "/etc/ssl/cert.pem"
    }
)

c = connection.cursor()

c.execute(f"""
    SELECT * FROM subscriptions;
""")

subscriptions = c.fetchall()

subreddits = {}

for subscription in subscriptions:
    _, chat_id, subreddit_name, date_of_subscription, upvotes_threshold = subscription

    subscriber_tuple = (chat_id, date_of_subscription, upvotes_threshold)
    if (not subreddit_name in subreddits):
        subreddits[subreddit_name] = [subscriber_tuple]
    else:
        subreddits[subreddit_name].append(subscriber_tuple)

for subreddit_name in subreddits:
    subreddit_posts = list(reddit.subreddit(subreddit_name).top(time_filter="month"))
    subscribers = subreddits[subreddit_name]

    for subscriber_tuple in subscribers:
        for subreddit_post in subreddit_posts:
            chat_id, date_of_subscription, upvotes_threshold = subscriber_tuple
            creation_date = datetime.datetime.fromtimestamp(subreddit_post.created)
            temp = date_of_subscription - datetime.timedelta(days = 15)

            if (subreddit_post.score >= upvotes_threshold and creation_date >= temp):
                c.execute(f"""
                    SELECT * FROM sent WHERE chat_id="{chat_id}";
                """)
                sent_posts = c.fetchall()
                found = False
                for sent in sent_posts:
                    sent_chat_id, sent_post_url, _ = sent
                    if (sent_chat_id == chat_id and sent_post_url == subreddit_post.permalink):
                        found = True

                if (not found):
                    bot.sendMessage(chat_id=chat_id, text=f"reddit.com/{subreddit_post.permalink}")
                    c.execute(f"""
                        INSERT INTO sent (chat_id, post_url, post_date) VALUES("{chat_id}", "{subreddit_post.permalink}", "{creation_date.strftime('%Y-%m-%d %H:%M:%S')}");
                    """)

connection.commit()
