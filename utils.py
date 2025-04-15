import pandas as pd
import uuid

def parse_csv_input(uploaded_file):
    df = pd.read_csv(uploaded_file)
    courses = df[["course", "teacher", "sks", "room", "semester"]].to_dict(orient="records")
    teachers = df["teacher"].unique().tolist()
    rooms = df["room"].unique().tolist()
    timeslots = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00"]  # Contoh jadwal
    semesters = df["semester"].unique().tolist()
    classes = ['A', 'B', 'C', 'D']  # Kelas maksimal 4
    return courses, teachers, rooms, timeslots, semesters, classes

def save_schedule_as_csv(schedule):
    df = pd.DataFrame(schedule)
    filename = f"jadwal_{uuid.uuid4().hex[:6]}.csv"
    df.to_csv(filename, index=False)
