import praw
import dotenv
import os
import MySQLdb
import time
import datetime
import telegram
from prawcore import NotFound

dotenv.load_dotenv()

BOT_API_KEY = os.getenv("BOT_API_KEY")
bot = telegram.Bot(token=BOT_API_KEY)

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
  })

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
  subreddit_posts = reddit.subreddit(subreddit_name).top(time_filter="month")
  subscribers = subreddits[subreddit_name]

  for subscriber_tuple in subscribers:
    for subreddit_post in subreddit_posts:
      chat_id, date_of_subscription, upvotes_threshold = subscriber_tuple

      creation_date = datetime.date.fromtimestamp(subreddit_post.created)
      if (subreddit_post.score >= upvotes_threshold and creation_date >= date_of_subscription):
        c.execute(f"""
          SELECT * FROM sent WHERE chat_id="{chat_id}";
        """)
        sent_posts = c.fetchall()
        #todo: clear sent when they are older than month
        found = False
        for sent in sent_posts:
          sent_chat_id, sent_post_url = sent
          if (sent_chat_id == chat_id and sent_post_url == subreddit_post.permalink):
            found = True

        if (not found):
          bot.sendMessage(chat_id=chat_id, text=subreddit_post.permalink)
          c.execute(f"""
            INSERT INTO sent (chat_id, post_url) VALUES("{chat_id}", "{subreddit_post.permalink}");
          """)

connection.commit()
