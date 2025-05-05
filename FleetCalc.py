import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Data konversi jarak
data_konversi = {
    "jarak": [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2,
              1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3,
              2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4,
              3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5,
              4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6,
              5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7],
    "konversi": [1.342, 1.342, 1.342, 1.342, 1.342, 1.231, 1.140, 1.064, 1.000,
                 0.945, 0.898, 0.856, 0.820, 0.787, 0.758, 0.732, 0.708, 0.687,
                 0.667, 0.649, 0.632, 0.617, 0.603, 0.590, 0.578, 0.566, 0.555,
                 0.545, 0.536, 0.527, 0.519, 0.511, 0.504, 0.497, 0.490, 0.483,
                 0.477, 0.469, 0.461, 0.454, 0.447, 0.440, 0.433, 0.427, 0.420,
                 0.412, 0.405, 0.399, 0.392, 0.386, 0.379, 0.373, 0.368, 0.362,
                 0.357, 0.352, 0.347, 0.342, 0.337, 0.332, 0.328, 0.324, 0.322,
                 0.319, 0.315, 0.312]
}
df_konversi = pd.DataFrame(data_konversi)

def get_konversi(jarak_input):
    return float(df_konversi.set_index("jarak").interpolate(method="linear").loc[jarak_input]["konversi"])

# Target ritasi berdasarkan jarak
target_ritasi_data = {
    "jarak": data_konversi["jarak"],
    "target_ritasi": [
        7, 7, 7, 7, 7, 7, 6, 6, 6, 5, 5, 5, 5, 4, 4, 4, 4, 4,
        4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
        3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
    ]
}
df_target_ritasi = pd.DataFrame(target_ritasi_data)

def get_target_ritasi(jarak_input):
    return float(df_target_ritasi.set_index("jarak").interpolate(method="linear").loc[jarak_input]["target_ritasi"])

# Target produktivitas loader
target_loader_map = {
    "EX1765": 800, "EX1862": 950,
    "EX1836": 800, "EX1791": 800,
    "EX1250": 525, "EX1284": 525, "EX1266": 525, "EX1280": 525,
    "EX1262": 525, "EX1260": 525, "EX1283": 525, "EX1183": 525,
    "EX1313": 525, "EX1185": 525, "EX1171": 525,
}

# Fungsi plot MF Macro vs Micro
def plot_mf_chart(unit_loader, spotting_time, loading_time_pc, cycle_time_pc, cycle_time_hd, jarak):
    jumlah_hd_range = list(range(2, 13))
    konversi_jarak = get_konversi(jarak)
    unit_productivity_map = {
        "EX1862": 13, "EX1765": 12, "EX1836": 12, "EX1791": 12,
        "EX1250": 7, "EX1284": 7, "EX1266": 7, "EX1280": 7, "EX1262": 7,
        "EX1260": 7, "EX1283": 7, "EX1183": 6.5, "EX1313": 6.5,
        "EX1185": 6.5, "EX1171": 6.5,
    }
    x = unit_productivity_map.get(unit_loader, 0)

    Serving_Time = (spotting_time / 60) + loading_time_pc
    Productivity_Loader = (((x * 0.85) * (3600 * 0.8)) / cycle_time_pc) / 1.43

    mf_macro_list = []
    mf_micro_list = []

    for jumlah_hd in jumlah_hd_range:
        MF_Macro = (jumlah_hd * (231 * konversi_jarak)) / Productivity_Loader
        MF_Micro = (jumlah_hd * Serving_Time) / cycle_time_hd
        mf_macro_list.append(MF_Macro)
        mf_micro_list.append(MF_Micro)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(jumlah_hd_range, mf_macro_list, label="MF Macro", marker='o')
    ax.plot(jumlah_hd_range, mf_micro_list, label="MF Micro", marker='s')
    ax.axhline(1, color='gray', linestyle='--', linewidth=1)
    ax.set_title("Perbandingan Matching Factor Macro vs Micro")
    ax.set_xlabel("Jumlah HD785")
    ax.set_ylabel("Matching Factor")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Streamlit UI
st.title("Fleet Performance Calculator")

with st.form("input_form"):
    st.markdown("### Masukkan Parameter")
    unit_loader = st.selectbox("Pilih Unit Loader:", list(target_loader_map.keys()))
    jumlah_hd = st.number_input("Jumlah HD785 (unit):", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    spotting_time = st.number_input("Spotting Time Unit Hauler:", min_value=0.0, value=0.0, step=1.0)
    cycle_time_pc = st.number_input("Cycle Time Loader (detik):", min_value=0.0, value=0.0, step=0.1)
    loading_time_pc = st.number_input("Loading Time Loader (menit):", min_value=0.0, value=0.0, step=0.1)
    jumlah_passing = st.number_input("Jumlah Passing Loader:", min_value=0.0, value=0.0, step=1.0)
    cycle_time_hd = st.number_input("Cycle Time HD (menit):", min_value=0.0, value=0.0, step=0.1)
    jarak = round(st.number_input("Jarak Front ke Disposal (KM):", min_value=0.0, value=0.0, step=0.1))
    submit = st.form_submit_button("Hitung")

if submit:
    if all([jumlah_hd > 0, cycle_time_pc > 0, loading_time_pc > 0, jumlah_passing > 0, cycle_time_hd > 0, jarak > 0]):
        unit_productivity_map = {
            "EX1862": 13, "EX1765": 12, "EX1836": 12, "EX1791": 12,
            "EX1250": 7, "EX1284": 7, "EX1266": 7, "EX1280": 7, "EX1262": 7,
            "EX1260": 7, "EX1283": 7, "EX1183": 6.5, "EX1313": 6.5,
            "EX1185": 6.5, "EX1171": 6.5,
        }

        x = unit_productivity_map.get(unit_loader, 0)
        konversi_jarak = get_konversi(jarak)

        Serving_Time = (spotting_time / 60) + loading_time_pc
        Productivity_Loader = (((x * 0.85) * (3600 * 0.8)) / cycle_time_pc) / 1.43
        Productivity_Hauler = Productivity_Loader / jumlah_hd / konversi_jarak
        Kebutuhan_HD = round((cycle_time_hd * Productivity_Loader) / (60 * 60 * 0.8) + 1)
        Matching_Factor_Macro = (jumlah_hd * (231 * konversi_jarak)) / Productivity_Loader
        Matching_Factor_Micro = (jumlah_hd * Serving_Time) / cycle_time_hd
        Ach_Ritasi = Productivity_Hauler * konversi_jarak / 42 * jumlah_hd

        target_loader = target_loader_map.get(unit_loader, 0)
        target_hauler = 231
        target_ritasi = get_target_ritasi(jarak)

        st.markdown("### Hasil Perhitungan")
        st.write(f"**Match Factor Macro:** {Matching_Factor_Macro:.2f}")
        st.write(f"**Match Factor Micro:** {Matching_Factor_Micro:.2f}")
        st.write(f"**Productivity Loader:** {Productivity_Loader:.2f} Bcm/Jam")
        st.write(f"**Productivity Hauler:** {Productivity_Hauler:.2f} Bcm/Jam")
        st.write(f"**Ritasi Should Be:** {Ach_Ritasi:.2f} Rit/Jam")

        if Productivity_Loader >= target_loader:
            st.success(f"✅ Produktivitas Loader ({Productivity_Loader:.2f}) telah mencapai target {target_loader} Bcm/Jam.")
        else:
            st.warning(f"⚠️ Produktivitas Loader ({Productivity_Loader:.2f}) belum mencapai target {target_loader} Bcm/Jam.")

        if Productivity_Hauler >= target_hauler:
            st.success(f"✅ Produktivitas Hauler ({Productivity_Hauler:.2f}) telah mencapai target {target_hauler} Bcm/Jam.")
        else:
            st.warning(f"⚠️ Produktivitas Hauler ({Productivity_Hauler:.2f}) belum mencapai target {target_hauler} Bcm/Jam.")

        if Ach_Ritasi >= target_ritasi:
            st.success(f"✅ Ritasi aktual {Ach_Ritasi:.2f} Rit telah mencapai target ({target_ritasi:.0f} Rit/Unit/Jam).")
        else:
            st.warning(f"⚠️ Ritasi aktual {Ach_Ritasi:.2f} Rit belum mencapai target ({target_ritasi:.0f} Rit/Unit/Jam).")

        if jumlah_hd < Kebutuhan_HD:
            st.warning(f"Rekomendasi: Tambahkan **{Kebutuhan_HD - jumlah_hd:.2f} unit HD785**.")
        elif jumlah_hd > Kebutuhan_HD + 1:
            st.warning(f"⚠️ Jumlah HD785 melebihi ideal **{Kebutuhan_HD:.2f} unit**.")
        else:
            st.success("✅ Jumlah HD785 saat ini sudah optimal.")

        # Analisis Matching Factor
        st.markdown("### 📊 Analisis Matching Factor")
        
        # MF chart setelah perhitungan
        plot_mf_chart(unit_loader, spotting_time, loading_time_pc, cycle_time_pc, cycle_time_hd, jarak)        

        if Matching_Factor_Macro < 1:
            st.info("🔄 *MF Macro < 1*: Risiko Loader Hanging.")
        elif Matching_Factor_Macro > 1:
            st.info("🔄 *MF Macro > 1*: Risiko antrian/idle HD.")

        if Matching_Factor_Micro < 1:
            st.info("⏱ *MF Micro < 1*: Loader sering idle, hauler belum standby saat dibutuhkan.")
        elif Matching_Factor_Micro > 1:
            st.info("⏱ *MF Micro > 1*: Hauler idle, terlalu cepat datang sebelum material/area siap.")

        if abs(Matching_Factor_Macro - Matching_Factor_Micro) > 0.2:
            st.warning("⚠️ Gap besar antara MF Macro dan Micro → Evaluasi akurasi waktu loading & cycle time hauler.")
        else:
            st.success("✅ MF Macro & Micro seimbang → Perpaduan waktu & kapasitas sudah optimal.")

# Tabel Target
st.markdown("### 📌 Target Fleet Performance")
data = {
    "EGI Unit": ["PC2000-11R", "PC2000-8", "PC1250 Series", "HD785-7"],
    "Prodty (Bcm/Jam)": [950, 800, 525, 231],
    "CT Mat OB (detik)": ["27 - 30", "27 - 30", "24 - 28", "-"],
    "Loading Time (menit)": ["2,5", "2,8", "3", "-"]
}
st.table(data)
