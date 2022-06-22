import dotenv
import os
import MySQLdb
import datetime

dotenv.load_dotenv()

connection = MySQLdb.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USERNAME"),
  passwd=os.getenv("DB_PASSWORD"),
  db=os.getenv("DB_NAME"),
  ssl={
    "ca": "/etc/ssl/cert.pem"
  })

cursor = connection.cursor()

month_ago = datetime.datetime.strptime((datetime.datetime.now() - datetime.timedelta(days = 31)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
cursor.execute(f"""
  DELETE FROM sent WHERE
  post_date < "{month_ago}"
""")

connection.commit()

