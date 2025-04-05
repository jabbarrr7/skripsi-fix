# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from genetic_algorithm import GeneticScheduler
from datetime import datetime
import os

st.set_page_config(page_title="Genetic Scheduler", layout="wide")

st.title("📅 Optimisasi Penjadwalan Tugas dengan Algoritma Genetika")

st.sidebar.header("📂 Upload Data Penjadwalan")
tasks_file = st.sidebar.file_uploader("Tugas (CSV)", type="csv")
teachers_file = st.sidebar.file_uploader("Pengajar (CSV)", type="csv")
rooms_file = st.sidebar.file_uploader("Ruangan (CSV)", type="csv")
timeslots_file = st.sidebar.file_uploader("Waktu (CSV)", type="csv")

if tasks_file and teachers_file and rooms_file and timeslots_file:
    tasks_df = pd.read_csv(tasks_file)
    teachers_df = pd.read_csv(teachers_file)
    rooms_df = pd.read_csv(rooms_file)
    timeslots_df = pd.read_csv(timeslots_file)

    st.success("✅ Semua data berhasil dimuat!")

    st.subheader("Contoh Data Tugas")
    st.dataframe(tasks_df.head())

    with st.spinner("Menjalankan algoritma genetika..."):
        scheduler = GeneticScheduler(tasks_df, teachers_df, rooms_df, timeslots_df,
                                     population_size=50, generations=100)
        best_schedule, fitness_history = scheduler.evolve()

    st.subheader("📈 Performa Evolusi")
    fig, ax = plt.subplots()
    ax.plot(fitness_history)
    ax.set_xlabel("Generasi")
    ax.set_ylabel("Nilai Fitness")
    ax.set_title("Grafik Perkembangan Fitness")
    st.pyplot(fig)

    st.subheader("🗓️ Jadwal Terbaik")
    schedule_df = pd.DataFrame(best_schedule)
    st.dataframe(schedule_df)

    csv = schedule_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Download Jadwal sebagai CSV",
        data=csv,
        file_name=f"jadwal_terbaik_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv',
    )

else:
    st.warning("Silakan unggah semua file data terlebih dahulu.")
