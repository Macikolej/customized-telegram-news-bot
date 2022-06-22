import dotenv
import os
import MySQLdb
import datetime
import settings

month_ago = datetime.datetime.strptime((datetime.datetime.now() - datetime.timedelta(days = 31)).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
settings.cursor.execute(f"""
  DELETE FROM sent WHERE
  post_date < "{month_ago}"
""")

settings.connection.commit()

