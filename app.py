import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from genetic_algorithm import GeneticScheduler
from utils import parse_csv_input, save_schedule_as_csv

st.title("Optimisasi Penjadwalan Tugas dengan Algoritma Genetika")

uploaded_file = st.file_uploader("Upload file CSV jadwal", type=["csv"])
if uploaded_file:
    tasks, teachers, rooms, timeslots = parse_csv_input(uploaded_file)
    scheduler = GeneticScheduler(tasks, teachers, rooms, timeslots)
    
    generations = st.slider("Jumlah generasi", 10, 500, 100)
    population_size = st.slider("Ukuran populasi", 10, 100, 50)

    best_schedule, history = scheduler.evolve(generations, population_size)
    
    st.subheader("Grafik Perkembangan Fitness")
    st.line_chart(history)

    st.subheader("Jadwal Terbaik")
    st.dataframe(pd.DataFrame(best_schedule))

    if st.button("Download Jadwal"):
        save_schedule_as_csv(best_schedule)
        st.success("Jadwal berhasil disimpan.")
