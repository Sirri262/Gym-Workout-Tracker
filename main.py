import psycopg2
from datetime import datetime
import math
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

def add_workout(cur,conn):

    while True:
            exercise_name = input("Enter your exercise name: ").strip()
            if exercise_name:
                break
            else:
                print("Exercise name cannot be empty!")
                

    while True:

        try:
            sets = int(input("Enter your set: "))
            if sets <= 0:
                print("Sets must be greater than 0")
            else:
                break
        except ValueError:
            print("Invalid input! Enter a number")
    
    while True:
        try:
            reps = int(input("Enter your reps: "))
            if reps <= 0:
                print("Reps must be greater than 0")
            else:
                break
        except ValueError:
            print("Invalid input! Enter a number")

    while True:
        try:
            weight = float(input("Enter your weight: "))
            if weight <= 0 or not math.isfinite(weight):
                print("Weight must be a positive, finite number")
            else:
                break
        except ValueError:
            print("Invalid input! Enter a number")

    while True:
        try:
            date = input("Enter your date (YYYY-MM-DD): ")
            datetime.strptime(date, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date! Use YYYY-MM-DD.")
                 
    try:
        sql = ("INSERT INTO workouts(exercise_name,sets,reps,weight,work_date) VALUES (%s, %s, %s, %s, %s)")
        cur.execute(sql,(exercise_name,sets,reps,weight,date))
        conn.commit()
        print("Exercise added successfully!")
    except psycopg2.Error:
        conn.rollback()
        print("Database error!")

    
def view_workout(cur,conn):
    try:
        cur.execute("SELECT * FROM workouts ORDER BY workout_id")
        view = cur.fetchall()

        if not view:
            print("No Result!")
        else:
            for exercise in view:
                print(f"{exercise[0]}) {exercise[1]} {exercise[2]}x{exercise[3]} KG:{exercise[4]} {exercise[5]}")
    except psycopg2.Error:
        conn.rollback()
        print("Database error!")

def exercise_search(cur,conn):
    while True:
        exercise_name = input("Search: ").strip()
        if exercise_name:
            break
        else:
            print("Exercise name cannot be empty!")

    search_term = (f"%{exercise_name}%")
    try:
        search= ("SELECT * FROM workouts WHERE exercise_name ILIKE %s")
        cur.execute(search,(search_term,))
        name = cur.fetchall()
        if not name:
            print("No Result")
        else:
            for i in name:
                print(f"{i[0]}) {i[1]} {i[2]}x{i[3]} {i[4]} {i[5]}")
    except psycopg2.Error:
        conn.rollback()
        print("Database error!")




def update_workout(cur, conn):

    while True:
        try:
            workout_id = int(input("Enter workout ID: "))
            if workout_id <= 0:
                print("ID must be greater than 0")
            else:
                try:
                    sql = "SELECT * FROM workouts WHERE workout_id = %s"
                    cur.execute(sql,(workout_id,))
                    result = cur.fetchone()
                    if result is None:
                        print("No workout found!")
                    else:
                        break
                except psycopg2.Error:
                    conn.rollback()
                    print("Database error!")
                    return
        except ValueError:
            print("Invalid ID! Enter a number")

    while True:
        try:
            new_weight = float(input("Enter new weight: "))
            if new_weight <= 0 or not math.isfinite(new_weight):
                print("Weight must be a positive, finite number")
            else:
                break
        except ValueError:
            print("Invalid weight! Enter a number")

    try:
        sql = "UPDATE workouts SET weight = %s WHERE workout_id = %s"
        cur.execute(sql, (new_weight, workout_id))
        affected_rows = cur.rowcount
        conn.commit()
        if affected_rows == 0:
            print("No workout found!")
        else:
            print("Workout updated successfully!")
    except psycopg2.Error:
        conn.rollback()
        print("Database error!")


def delete_workout(cur,conn):
    while True:
        try:
            workout_id = int(input("Enter workout ID to delete: "))
            if workout_id <= 0:
                print("ID must be greater than 0")
            else:
                break
        except ValueError:
            print("Invalid ID! Enter a number")
        
    try:
        sql = "DELETE FROM workouts WHERE workout_id = %s"
        cur.execute(sql,(workout_id,))
        affected_rows = cur.rowcount
        conn.commit()
        if affected_rows == 0:
            print("No workout found!")
        else:
            print("Workout deleted successfully!")
    except psycopg2.Error:
        conn.rollback()
        print("Database error!")

try:
    while True:

        try:
            choice = int(input("""
    --------- GYM WORKOUT TRACKER ---------
    1. Add Workout
    2. View Workouts
    3. Search Exercise
    4. Update Workout
    5. Delete Workout
    6. Exit
    --------------------------
Choose an option: """))
        except ValueError:
            print("Invalid choice!")
            continue

        if choice == 1:
            add_workout(cur,conn)
        elif choice == 2:
            view_workout(cur,conn)
        elif choice == 3:
            exercise_search(cur,conn)
        elif choice == 4:
            update_workout(cur,conn)
        elif choice == 5:
            delete_workout(cur,conn)
        elif choice == 6:
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")
finally:
    cur.close()
    conn.close()