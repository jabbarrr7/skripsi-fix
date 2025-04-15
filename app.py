import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from genetic_algorithm import GeneticScheduler
from utils import parse_csv_input, save_schedule_as_csv

st.title("Optimisasi Jadwal Perkuliahan dengan Algoritma Genetika")

uploaded_file = st.file_uploader("Upload file CSV jadwal perkuliahan", type=["csv"])
if uploaded_file:
    courses = parse_csv_input(uploaded_file)
    rooms = list({c["room"] for c in courses})
    start_times = list({c["start_time"] for c in courses})

    scheduler = GeneticScheduler(courses, rooms, start_times)

    generations = st.slider("Jumlah generasi", 10, 500, 100)
    population_size = st.slider("Ukuran populasi", 10, 100, 50)

    best_schedule, history, evolution_log = scheduler.evolve(generations, population_size)

    st.subheader("Grafik Perkembangan Fitness")
    st.line_chart(history)

    st.subheader("Jadwal Terbaik")
    st.dataframe(pd.DataFrame(best_schedule))

    st.subheader("\U0001F4D8 Log Evolusi per Generasi")
    df_log = pd.DataFrame({
        "Generasi": [entry["Generasi"] for entry in evolution_log],
        "Fitness": [entry["Fitness"] for entry in evolution_log]
    })
    st.dataframe(df_log)

    selected_gen = st.slider("Lihat jadwal pada generasi ke-", 1, generations, 1)
    selected = next((entry for entry in evolution_log if entry["Generasi"] == selected_gen), None)

    if selected:
        st.markdown(f"### Jadwal Generasi {selected_gen} (Fitness: {selected['Fitness']})")
        st.dataframe(pd.DataFrame(selected["Jadwal"]))

    if st.button("Download Jadwal"):
        save_schedule_as_csv(best_schedule)
        st.success("Jadwal berhasil disimpan.")
