import pandas as pd
import uuid

def parse_csv_input(uploaded_file):
    df = pd.read_csv(uploaded_file)
    tasks = df[["task", "teacher"]].to_dict(orient="records")  # ⬅️ Ini yang berubah
    teachers = df["teacher"].unique().tolist()
    rooms = df["room"].unique().tolist()
    timeslots = df["timeslot"].unique().tolist()
    return tasks, teachers, rooms, timeslots


def save_schedule_as_csv(schedule):
    df = pd.DataFrame(schedule)
    filename = f"jadwal_{uuid.uuid4().hex[:6]}.csv"
    df.to_csv(filename, index=False)
