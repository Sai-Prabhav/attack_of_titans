import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
   database="d1stpqngp1fuph", user='tawuenamkzawue', password=os.getenv("PASSWD"), host="ec2-52-214-125-106.eu-west-1.compute.amazonaws.com", port= '5432'
)
cursor = connection.cursor()
cursor.execute("SELECT * FROM test1")
print(cursor.fetchall())