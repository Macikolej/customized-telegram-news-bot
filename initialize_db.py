from dotenv import load_dotenv
import os
import MySQLdb

load_dotenv()

connection = MySQLdb.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd=os.getenv("DB_PASSWORD"),
  db=os.getenv("DB_NAME"),
  ssl_mode="VERIFY_IDENTITY",
  ssl={
    "ca": "/etc/ssl/cert.pem"
  })

cursor = connection.cursor()

cursor.execute(f"""
  DROP TABLE IF EXISTS subscriptions;
  CREATE TABLE subscriptions (
  id int AUTO_INCREMENT PRIMARY KEY,
  chat_id varchar(255),
  subreddit_name varchar(255),
  date_of_subscription datetime,
  upvotes_threshold integer
);""")

cursor.execute("""
DROP TABLE IF EXISTS sent;
CREATE TABLE sent (
  chat_id varchar(255),
  post_url varchar(255),
  post_date datetime
);""")

cursor.close()
