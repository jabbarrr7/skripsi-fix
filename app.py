import streamlit as st
import pandas as pd
from genetic_algorithm import GeneticScheduler
from utils import parse_csv_input, save_schedule_as_csv

st.title("Optimisasi Jadwal Perkuliahan dengan Algoritma Genetika")

uploaded_file = st.file_uploader("Upload file CSV jadwal perkuliahan", type=["csv"])
if uploaded_file:
    # Parsing CSV; file CSV harus memiliki kolom: course, teacher, sks, room, semester, class
    courses, teachers, rooms, timeslots, semesters, classes = parse_csv_input(uploaded_file)
    
    # Buat instance scheduler
    scheduler = GeneticScheduler(courses, teachers, rooms, timeslots, semesters, classes)
    
    generations = st.slider("Jumlah generasi", 10, 500, 100)
    population_size = st.slider("Ukuran populasi", 10, 100, 50)
    
    best_schedule, history, evolution_log = scheduler.evolve(generations, population_size)
    
    st.subheader("Grafik Perkembangan Fitness")
    st.line_chart(history)
    
    st.subheader("Jadwal Terbaik (Semua)")
    st.dataframe(pd.DataFrame(best_schedule))
    
    # Pisahkan jadwal berdasarkan semester ganjil dan genap
    jadwal_ganjil = [entry for entry in best_schedule if entry["semester"] % 2 == 1]
    jadwal_genap = [entry for entry in best_schedule if entry["semester"] % 2 == 0]
    
    st.subheader("Jadwal Semester Ganjil")
    if jadwal_ganjil:
        st.dataframe(pd.DataFrame(jadwal_ganjil))
    else:
        st.info("Tidak ada data jadwal untuk semester ganjil.")
    
    st.subheader("Jadwal Semester Genap")
    if jadwal_genap:
        st.dataframe(pd.DataFrame(jadwal_genap))
    else:
        st.info("Tidak ada data jadwal untuk semester genap.")
    
    st.subheader("📘 Log Evolusi per Generasi")
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
    
    if st.button("Download Jadwal (Semua)"):
        filename = save_schedule_as_csv(best_schedule, filename_prefix="jadwal_semua")
        st.success(f"Jadwal berhasil disimpan sebagai {filename}.")
    
    if st.button("Download Jadwal Semester Ganjil"):
        filename = save_schedule_as_csv(jadwal_ganjil, filename_prefix="jadwal_ganjil")
        st.success(f"Jadwal ganjil berhasil disimpan sebagai {filename}.")
    
    if st.button("Download Jadwal Semester Genap"):
        filename = save_schedule_as_csv(jadwal_genap, filename_prefix="jadwal_genap")
        st.success(f"Jadwal genap berhasil disimpan sebagai {filename}.")
