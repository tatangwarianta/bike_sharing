import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded")

# Sidebar
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)
st.sidebar.markdown("""
    <style>
    .sidebar-title {
        font-size: 24px !important;
        font-weight: bold;
    }
    .sidebar-option {
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)
st.sidebar.markdown('<p class="sidebar-title">🚲 Bike Sharing Dashboard</p>', unsafe_allow_html=True)
year_option = st.sidebar.radio("📅 Pilih Rentang Tahun:", ["2011", "2012", "2011-2012"])

# Filter data
if year_option == "2011":
    filtered_df = hour_df[hour_df["yr"] == 0]
elif year_option == "2012":
    filtered_df = hour_df[hour_df["yr"] == 1]
else:
    filtered_df = hour_df

# **Membuat tiga kolom yang lebih proporsional**
col1, col2, col3 = st.columns([1.2, 2.5, 1.5])

# **Kolom 1: Metrik Utama**
with col1:
    st.subheader("📊 Metrik Penyewaan")
    st.metric("Total Penyewaan", filtered_df["cnt"].sum())
    st.metric("Registered Users", filtered_df["registered"].sum())
    st.metric("Casual Users", filtered_df["casual"].sum())

# **Kolom 2: Visualisasi Utama**
with col2:
    st.subheader("📅 Penyewaan Tiap Jam Hari Kerja vs Hari Libur")
    filtered_df["workingday"] = filtered_df["workingday"].replace({0: "Hari Libur", 1: "Hari Kerja"})
    workingday_avg = filtered_df.groupby("workingday")["cnt"].mean().round(2).reset_index()
    
    # Visualisasi Data
    fig, ax = plt.subplots(figsize=(6, 4))
    ax = sns.barplot(data=workingday_avg, x="workingday", y="cnt", zorder=3, color="#2980B9")
    for container in ax.containers:
        ax.bar_label(container, label_type="center", color="white", fontsize=12)
    plt.gca().set_facecolor("lightgray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.xlabel("", fontsize=14, color="#404040")
    plt.ylabel("Jumlah Penyewaan", fontsize=14, color="#404040")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", color="white", linestyle="--", alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("⛅ Penyewaan Tiap Jam Berdasarkan Cuaca")
    weather_labels = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    filtered_df["weathersit"] = filtered_df["weathersit"].replace(weather_labels)
    weather_rental = filtered_df.groupby("weathersit")["cnt"].mean().reset_index()
    order_weather = ["Cerah", "Berawan", "Hujan Ringan", "Hujan Lebat"]
    weather_rental["weathersit"] = pd.Categorical(weather_rental["weathersit"], categories=order_weather, ordered=True)
    weather_rental = weather_rental.sort_values("weathersit")
    
    # Visualisasi Data
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.barplot(data=weather_rental, x="weathersit", y="cnt", zorder=3, color="#2980B9")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", label_type="center", color="white", fontsize=12)
    plt.gca().set_facecolor("lightgray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.xlabel("", fontsize=14, color="#404040")
    plt.ylabel("Jumlah Penyewaan", fontsize=14, color="#404040")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", color="white", linestyle="--", alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)
    
    st.subheader("⏳ Penyewaan Berdasarkan Waktu")
    def rentang_waktu(hr):
        if 6 <= hr < 12:
            return "Pagi"
        elif 12 <= hr < 15:
            return "Siang"
        elif 15 <= hr < 20:
            return "Sore"
        else:
            return "Malam"
    filtered_df["time_cluster"] = filtered_df["hr"].apply(rentang_waktu)
    time_group = filtered_df.groupby("time_cluster")[["casual", "registered"]].sum().reset_index()
    order_time = ["Pagi", "Siang", "Sore", "Malam"]
    time_group["time_cluster"] = pd.Categorical(time_group["time_cluster"], categories=order_time, ordered=True)
    time_group = time_group.sort_values("time_cluster")
    
    # Visualisasi Data
    fig, ax = plt.subplots(figsize=(12, 8))
    ax = sns.barplot(data=time_group.melt(id_vars="time_cluster", var_name="User Type", value_name="Jumlah"), 
                    x="time_cluster", y="Jumlah", hue="User Type", zorder=3, 
                    palette={"casual": "#F39C12", "registered": "#2980B9"})
    for container in ax.containers:
        ax.bar_label(container, fmt="%.0f", label_type="center", color="white", fontsize=12)
    plt.gca().set_facecolor("lightgray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.xlabel("Kategori Waktu", fontsize=14, color="#404040")
    plt.ylabel("Jumlah Penyewaan (in Million)", fontsize=14, color="#404040")
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", color="white", linestyle="--", alpha=0.7)
    plt.legend(title="Tipe Pengguna", fontsize=12)
    plt.tight_layout()
    st.pyplot(fig)

# **Kolom 3: Penyewaan berdasarkan waktu dan jenis pengguna**
with col3:
    filtered_df_sorted = filtered_df.sort_values(by="cnt", ascending=False)
    st.subheader("🏆 Top Penyewaan")
    st.dataframe(filtered_df_sorted,
                 column_order=("dteday", "hr", "cnt"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "dteday": st.column_config.TextColumn(
                        "📅 Tanggal",
                    ),
                    "hr": st.column_config.TextColumn(
                        "⏰ Jam",
                    ),
                    "cnt": st.column_config.ProgressColumn(
                        "Total",
                        format="%f",
                        min_value=0,
                        max_value=max(filtered_df_sorted.cnt),
                     )}
                 )

    # **About Section**
    st.markdown("""
    ---
    ### 📌 About
    - **Dashboard ini dibuat untuk menganalisis data penyewaan sepeda.**
    - **Menampilkan tren penyewaan berdasarkan waktu dan cuaca.**
    - **Menyediakan metrik utama terkait total penyewaan.**
    """)