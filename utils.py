import pandas as pd
import uuid
from datetime import datetime, timedelta


# def parse_csv_input(uploaded_file):
#     df = pd.read_csv(uploaded_file)
#     # Pastikan tipe data 'sks' dan 'semester' diubah ke integer
#     df['sks'] = df['sks'].astype(int)
#     df['semester'] = df['semester'].astype(int)
#     courses = df.to_dict(orient="records")
    
#     teachers = df["teacher"].unique().tolist()
#     rooms = df["room"].unique().tolist()
    
#     # Buat list timeslot berupa angka. Misalnya, kita buat 12 slot per hari.
#     # Untuk contoh, kita gunakan angka 1 s.d. 12.
#     timeslots = list(df['timeslot'].unique())
    
#     # Semester juga diambil dari data (dalam hal ini, 1 sampai 7)
#     semesters = sorted(df["semester"].unique().tolist())
    
#     # Kelas di-set secara default (misalnya "A", "B", "C", "D")
#     classes = ['A', 'B', 'C', 'D']
    
#     return courses, teachers, rooms, timeslots, semesters, classes
def parse_csv_input(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['sks'] = df['sks'].astype(int)
    df['semester'] = df['semester'].astype(int)
    courses = df.to_dict(orient="records")
    teachers = df["teacher"].unique().tolist()
    rooms = df["room"].unique().tolist()
    timeslots = df['timeslot'].unique().tolist()
    semesters = sorted(df["semester"].unique().tolist())
    classes = df["class"].unique().tolist()
    return courses, teachers, rooms, timeslots, semesters, classes

def parse_time_range(timeslot):
    try:
        hari, jam = timeslot.split(", ")
        start, end = jam.split("-")
        fmt = "%H:%M"
        return hari.strip(), datetime.strptime(start.strip(), fmt), datetime.strptime(end.strip(), fmt)
    except Exception as e:
        print(f"Error parsing timeslot: {timeslot}", e)
        return None, None, None


def save_schedule_as_csv(schedule, filename_prefix="jadwal"):
    df = pd.DataFrame(schedule)
    filename = f"{filename_prefix}_{uuid.uuid4().hex[:6]}.csv"
    df.to_csv(filename, index=False)
    return filename
