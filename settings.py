# import dotenv
# import os

# def init():

# 	dotenv.load_dotenv()

# 	global BOT_API_KEY
# 	global BOT_NAME
# 	global URL
# 	global REDDIT_API_ID
# 	global REDDIT_API_KEY
# 	global DB_HOST
# 	global DB_USERNAME
# 	global DB_PASSWORD
# 	global DB_NAME
# 	global USER_AGENT
# 	global bot
# 	global reddit
# 	global connection
# 	global cursor

# 	BOT_API_KEY=os.getenv("BOT_API_KEY")
# 	BOT_NAME=os.getenv("BOT_NAME")
# 	URL=os.getenv("URL")
# 	REDDIT_API_ID=os.getenv("REDDIT_API_ID")
# 	REDDIT_API_KEY=os.getenv("REDDIT_API_KEY")
# 	DB_HOST=os.getenv("DB_HOST")
# 	DB_USERNAME=os.getenv("DB_USERNAME")
# 	DB_PASSWORD=os.getenv("DB_PASSWORD")
# 	DB_NAME=os.getenv("DB_NAME")

# 	bot = telegram.Bot(token=BOT_API_KEY)

# 	reddit = praw.Reddit(
#     client_id=REDDIT_API_ID,
#     client_secret=REDDIT_API_KEY,
#     user_agent=USER_AGENT,
# 	)

# 	connection = MySQLdb.connect(
# 	  host=DB_HOST,
# 	  user=DB_USERNAME,
# 	  passwd=DB_PASSWORD,
# 	  db=DB_NAME,
# 	  ssl={
# 	    "ca": "/etc/ssl/cert.pem"
# 	  }
# 	)

# 	cursor = connection.cursor()
