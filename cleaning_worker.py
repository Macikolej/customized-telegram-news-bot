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

c = connection.cursor()

# c.execute(f"""
#   DELETE FROM sent WHERE
#   STR_TO_DATE(post_date, '%Y-%m-%d %H:%M:%S') < {str(datetime.timedelta(days = 31))}
# """)

# connection.commit()

