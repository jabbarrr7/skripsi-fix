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

    best_schedule, history, evolution_log = scheduler.evolve(generations, population_size)

    
    st.subheader("Grafik Perkembangan Fitness")
    st.line_chart(history)

    st.subheader("Jadwal Terbaik")
    st.dataframe(pd.DataFrame(best_schedule))

    st.subheader("📘 Log Evolusi per Generasi")

    # Tampilkan ringkasan fitness tiap generasi
    df_log = pd.DataFrame({
        "Generasi": [entry["Generasi"] for entry in evolution_log],
        "Fitness": [entry["Fitness"] for entry in evolution_log]
    })
    st.dataframe(df_log)

    # Pilih generasi tertentu untuk lihat detail
    selected_gen = st.slider("Lihat jadwal pada generasi ke-", 1, generations, 1)
    selected = next((entry for entry in evolution_log if entry["Generasi"] == selected_gen), None)

    if selected:
        st.markdown(f"### Jadwal Generasi {selected_gen} (Fitness: {selected['Fitness']})")
        st.dataframe(pd.DataFrame(selected["Jadwal"]))


    if st.button("Download Jadwal"):
        save_schedule_as_csv(best_schedule)
        st.success("Jadwal berhasil disimpan.")
