
# 🏋️ Gym Workout Tracker

A command-line application built with Python and PostgreSQL to manage and track gym workouts.

## 🚀 Features
- Add new workouts
- View all workouts
- Search exercises by name
- Update workout weights
- Delete workouts
- Input validation and database error handling

## 🛠 Technologies
- Python
- PostgreSQL
- psycopg2
- python-dotenv

## 📁 Project Structure
```text
Gym-Workout-Tracker/
├── main.py
├── .gitignore
├── requirements.txt
└── README.md
```

## 🗄 Database Structure

**Database:** `gym_tracker`

**Table:** `workouts`

| Column | Data Type |
|---|---|
| workout_id | INTEGER (Primary Key) |
| exercise_name | VARCHAR |
| sets | INTEGER |
| reps | INTEGER |
| weight | NUMERIC |
| work_date | DATE |

## 💻 Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL database and `workouts` table, then configure a local `.env` file with your database credentials.

Run the application:

```bash
python main.py
```

## 📋 Example Console Menu

```text
--------- GYM WORKOUT TRACKER ---------
1. Add Workout
2. View Workouts
3. Search Exercise
4. Update Workout
5. Delete Workout
6. Exit
---------------------------------------
Choose an option:
```
