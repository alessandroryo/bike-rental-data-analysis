
import streamlit as st
import pandas as pd
import plotly.express as px

# Memuat dataset day.csv
day_df = pd.read_csv('./data/day.csv')

# Memuat dataset hour.csv
hour_df = pd.read_csv('./data/hour.csv')

# Mengubah kode hari menjadi nama hari dalam seminggu dan mengurutkannya dari Senin
day_names = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
day_df['weekday_name'] = day_df['weekday'].map(day_names)

# Mengurutkan data berdasarkan hari dalam seminggu
day_names_ordered = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
day_df['weekday_name'] = pd.Categorical(day_df['weekday_name'], categories=day_names_ordered, ordered=True)
clustered_data = day_df.groupby(['weekday_name', 'weathersit']).agg({'cnt': 'mean'}).reset_index()

# Mempersiapkan data untuk plot penggunaan per jam
hourly_usage = hour_df.groupby('hr')['cnt'].mean().reset_index()

st.set_page_config(layout="wide")

st.title("Dashboard Penggunaan Sepeda di Washington D.C.")

# Membuat dua kolom untuk tata letak berdampingan
col1, col2 = st.columns(2)

with col1:
    # Plot 1: Rata-Rata Penggunaan Sepeda Berdasarkan Hari dan Kondisi Cuaca
    st.subheader("Bagaimana tingkat penggunaan sepeda berdasarkan hari kerja dan akhir pekan di Washington D.C. dengan dipengaruhi oleh kondisi cuaca?")
    fig1 = px.bar(clustered_data, x='weathersit', y='cnt', color='weekday_name', barmode='group',
                  labels={'weathersit': 'Kondisi Cuaca', 'cnt': 'Jumlah Rata-Rata Sepeda', 'weekday_name': 'Hari dalam Seminggu'},
                  title='Rata-Rata Penggunaan Sepeda Berdasarkan Hari dan Kondisi Cuaca')
    fig1.update_layout(xaxis=dict(tickmode='array', tickvals=[1, 2, 3], ticktext=['Cerah', 'Berkabut', 'Salju/Hujan Ringan']))
    st.plotly_chart(fig1)
    st.markdown("""
    1. **Penggunaan Sepeda pada Hari Cerah:**
       - Penggunaan sepeda tertinggi terjadi pada hari Rabu, lalu pada Jumat dan Kamis.
       - Hari Minggu memiliki penggunaan sepeda terendah pada hari cerah.
       - Hari kerja cenderung memiliki penggunaan sepeda yang tinggi pada hari cerah, kemungkinan karena banyak orang yang menggunakan sepeda untuk berangkat kerja atau sekolah.

    2. **Penggunaan Sepeda pada Hari Berkabut:**
       - Penggunaan sepeda pada hari berkabut masih cukup tinggi tetapi sedikit lebih rendah dibandingkan hari cerah.
       - Hari Kamis memiliki penggunaan sepeda tertinggi pada hari berkabut, diikuti oleh Senin dan Jumat.
       - Penggunaan sepeda pada hari Rabu menjadi yang terendah, menunjukkan bahwa hari Rabu memiliki penggunaan sepeda yang rendah karena kondisi cuaca.

    3. **Penggunaan Sepeda pada Hari Salju/Hujan Ringan:**
       - Penggunaan sepeda menurun secara signifikan pada kondisi cuaca buruk seperti salju atau hujan ringan.
       - Selasa memiliki penggunaan sepeda tertinggi pada kondisi cuaca ini, diikuti oleh Sabtu.
       - Hari Jumat memiliki penggunaan sepeda terendah pada kondisi cuaca buruk, menunjukkan bahwa cuaca buruk sangat mempengaruhi keputusan orang untuk menggunakan sepeda.
    """)

with col2:
    # Plot 2: Perubahan Penggunaan Sepeda Sepanjang Hari
    st.subheader("Bagaimana perubahan penggunaan sepeda sepanjang hari atau 24 jam dan apakah ada waktu-waktu puncak tertentu penyewaan sepeda di Washington D.C.?")
    fig2 = px.line(hourly_usage, x='hr', y='cnt', markers=True, 
                   labels={'hr': 'Jam', 'cnt': 'Jumlah Rata-Rata Sepeda'},
                   title='Perubahan Penggunaan Sepeda Sepanjang Hari')
    fig2.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
    st.plotly_chart(fig2)
    st.markdown("""
    1. **Jam Dini Hari (00:00 - 05:00):**
       - Penggunaan sepeda sangat rendah selama jam-jam ini, menunjukkan bahwa sangat sedikit orang yang menggunakan sepeda pada dini hari.
       - Ini mungkin karena kebanyakan orang sedang tidur atau tidak melakukan aktivitas yang memerlukan penggunaan sepeda.

    2. **Jam Pagi (06:00 - 09:00):**
       - Terjadi lonjakan penggunaan sepeda mulai sekitar jam 6 pagi, mencapai puncaknya sekitar jam 8 pagi.
       - Puncak ini kemungkinan besar disebabkan oleh orang-orang yang berangkat kerja atau sekolah, menunjukkan bahwa sepeda digunakan sebagai moda transportasi untuk perjalanan pagi.
    
    3. **Jam Siang (10:00 - 15:00):**
       - Penggunaan sepeda menurun setelah jam puncak pagi, namun tetap stabil pada tingkat yang sedang sepanjang jam-jam siang.
       - Ini menunjukkan bahwa sepeda masih digunakan untuk aktivitas siang hari, seperti perjalanan singkat atau makan siang.
    
    4. **Jam Sore (16:00 - 19:00):**
       - Ada lonjakan penggunaan sepeda kedua yang mencapai puncaknya sekitar jam 17-18 sore.
       - Lonjakan ini kemungkinan besar disebabkan oleh orang-orang yang pulang kerja, mirip dengan penggunaan di pagi hari.
    
    5. **Jam Malam (20:00 - 23:00):**
       - Penggunaan sepeda menurun secara signifikan setelah jam 7 malam, dengan jumlah pengguna yang terus menurun hingga tengah malam.
       - Ini menunjukkan bahwa aktivitas malam hari yang melibatkan penggunaan sepeda berkurang drastis, kemungkinan karena kebanyakan orang telah selesai dengan aktivitas sehari-hari mereka.
    """)
