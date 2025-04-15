import pandas as pd
import uuid

def parse_csv_input(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df.to_dict(orient="records")

def save_schedule_as_csv(schedule):
    df = pd.DataFrame(schedule)
    filename = f"jadwal_{uuid.uuid4().hex[:6]}.csv"
    df.to_csv(filename, index=False)
