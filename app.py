import streamlit as st
import pandas as pd
from genetic_algorithm import GeneticScheduler

st.title("Optimasi Penjadwalan Tugas dengan Algoritma Genetika")

# Input jumlah tugas, guru, mata kuliah, ruangan, dan slot waktu
num_tasks = st.number_input("Jumlah Tugas", min_value=1, value=10)
num_teachers = st.number_input("Jumlah Guru", min_value=1, value=5)
num_subjects = st.number_input("Jumlah Mata Kuliah", min_value=1, value=5)
num_rooms = st.number_input("Jumlah Ruangan", min_value=1, value=3)
num_timeslots = st.number_input("Jumlah Slot Waktu", min_value=1, value=5)

if st.button("Jalankan Optimasi"):
    # Buat dataset
    tasks = [f"Tugas {i+1}" for i in range(num_tasks)]
    teachers = [f"Guru {i+1}" for i in range(num_teachers)]
    subjects = [f"Mata Kuliah {i+1}" for i in range(num_subjects)]
    rooms = [f"Ruangan {i+1}" for i in range(num_rooms)]
    timeslots = [f"Slot Waktu {i+1}" for i in range(num_timeslots)]

    # Jalankan Algoritma Genetika
    scheduler = GeneticScheduler(tasks, teachers, subjects, rooms, timeslots)
    best_schedule = scheduler.evolve()

    # Tampilkan hasil dalam tabel
    df_schedule = pd.DataFrame(best_schedule, columns=["Tugas", "Dosen", "Mata Kuliah", "Ruangan", "Waktu"])
    
    st.write("### Jadwal Optimal:")
    st.dataframe(df_schedule)
