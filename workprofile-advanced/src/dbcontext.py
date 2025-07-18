from typing import List
import time
import mysql.connector
from mysql.connector import Error
from os import environ
from person import Person
from flask import Response

db_user = environ.get('DB_USER')
db_pass = environ.get('DB_PASS')
db_host = environ.get('DB_HOST')
db_name = environ.get('DB_NAME')

config = {
    "host": db_host,
    "user": db_user,
    "password": db_pass,
    "database": db_name,
    "port": 3306
}

def demo_data() -> List[Person]:
    person1 = Person(1, "John", "Doe", 30, "76 Ninth Avenue St, New York, NY 10011, USA", "Google")
    person2 = Person(2, "Jane", "Doe", 28, "15 Aabogade St, Aarhus, Denmark 8200", "Microsoft")
    person3 = Person(3, "Jack", "Doe", 25, "98 Yigal Alon St, Tel Aviv, Israel 6789141", "Amazon")
    return [person1, person2, person3]

def db_data() -> List[Person]:
    if not db_host:
        return demo_data()
    
    if not (db_user and db_pass):
        raise Exception("DB_USER and DB_PASS are not set")
    
    result = []
    try:
        cnx = mysql.connector.connect(**config)
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute("SELECT * FROM people")
            for item in cursor:
                result.append(Person(item[0], item[1], item[2], item[3], item[4], item[5]))
            cursor.close()
            cnx.close()
    except Error as e:
        print(f"Error fetching data from DB: {e}")
        # fallback ל-demo data או לשדרג טיפול שגיאות לפי צורך
        result = demo_data()
    return result

def db_delete(id: int) -> Response:
    if not db_host:
        return Response(status=200)
    status = 200
    try:
        cnx = mysql.connector.connect(**config)
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute(f"DELETE FROM people WHERE id = {id}")
            cnx.commit()
            cursor.close()
            cnx.close()
    except Error as e:
        print(f"Error deleting from DB: {e}")
        status = 404
    return Response(status=status)

def db_add(person: Person) -> Response:
    if not db_host:
        return Response(status=200)
    status = 200
    personId = 0
    try:
        cnx = mysql.connector.connect(**config)
        if cnx.is_connected():
            cursor = cnx.cursor()
            cursor.execute(
                "INSERT INTO people (firstName, lastName, age, address, workplace) VALUES (%s, %s, %s, %s, %s)",
                (person.first_name, person.last_name, person.age, person.address, person.workplace)
            )
            cnx.commit()
            personId = cursor.lastrowid
            cursor.close()
            cnx.close()
    except Error as e:
        print(f"Error adding to DB: {e}")
        status = 404
    return Response(status=status, response=str(personId))

def health_check() -> bool:
    if not db_host:
        return True
    
    retries = 5
    delay = 3  # שניות בין ניסיונות
    for attempt in range(retries):
        try:
            cnx = mysql.connector.connect(**config)
            if cnx.is_connected():
                cursor = cnx.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchall()
                cursor.close()
                cnx.close()
                return True
        except Error as e:
            print(f"DB connection failed on attempt {attempt+1}/{retries}: {e}")
            time.sleep(delay)
    return False

