import psycopg2
import requests
import json
from datetime import datetime


response = requests.get('https://cph-flightinfo-prod.azurewebsites.net//api/v1/waiting/get?type=ventetid')
waitingtime = json.loads(response.text)
waitingtime_json = json.dumps(waitingtime)
t2WaitingTime = (waitingtime["t2WaitingTime"])
t2WaitingTimeInterval = (waitingtime["t2WaitingTimeInterval"])
deliveryId = (waitingtime["deliveryId"])
deliveryId = (deliveryId.replace("T", " ")) 


try:
    connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="cph_postgres_db",
                                  port="5432",
                                  database="postgres")
    cursor = connection.cursor()

    postgres_insert_query = """ INSERT INTO waitingtime (t2WaitingTime, t2WaitingTimeInterval, deliveryId) VALUES (%s,%s,%s)"""
    record_to_insert = (t2WaitingTime, t2WaitingTimeInterval, deliveryId)
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into CPH Waiting Time table")

except (Exception, psycopg2.Error) as error:
    print("Failed to insert record into CPH Waiting Time table", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
