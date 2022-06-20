import praw
import dotenv
import os

dotenv.load_dotenv()

REDDIT_API_ID = os.getenv("REDDIT_API_ID")
REDDIT_API_KEY = os.getenv("REDDIT_API_KEY")

reddit = praw.Reddit(
    client_id=REDDIT_API_ID,
    client_secret=REDDIT_API_KEY,
    user_agent="muj ulubiony bot",
)

for submission in reddit.subreddit("MadeMeSmile").hot(limit=10):
    print(submission.permalink)
