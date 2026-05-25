import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

# === CONFIG ===
st.set_page_config(page_title="TemanMood Dashboard", page_icon="🧠", layout="wide")

# === LOAD DATA ===
@st.cache_data
def load_data():
    df = pd.read_csv('Daylio_Abid.csv')
    df = df.dropna(subset=['activities'])
    df['mood'] = df['mood'].str.strip()
    df['sub_mood'] = df['sub_mood'].str.strip()
    df['full_date'] = pd.to_datetime(df['full_date'], format='%d/%m/%Y')

    def parse_hour(t):
        try:
            parts = t.strip().split()
            hour = int(parts[0].split(':')[0])
            if parts[1].lower() == 'pm' and hour != 12: hour += 12
            elif parts[1].lower() == 'am' and hour == 12: hour = 0
            return hour
        except:
            return None

    df['hour'] = df['time'].apply(parse_hour)

    def get_time_cat(h):
        if h is None: return 'Unknown'
        if 5 <= h < 12: return 'Pagi'
        elif 12 <= h < 17: return 'Siang'
        elif 17 <= h < 21: return 'Sore'
        else: return 'Malam'

    df['time_category'] = df['hour'].apply(get_time_cat)
    mood_map = {'Negatif':1,'Netral':2,'Positif':3}
    df['mood_score'] = df['mood'].map(mood_map)
    df['activities_list'] = df['activities'].apply(lambda x: [a.strip() for a in str(x).split('|') if a.strip()])
    df['activity_count'] = df['activities_list'].apply(len)
    df['is_weekend'] = df['weekday'].isin(['Saturday','Sunday']).astype(int)
    return df

df = load_data()
df_exploded = df.explode('activities_list')

mood_order = ['Negatif','Netral','Positif']
mood_colors = {'Negatif':'#e74c3c','Netral':'#f1c40f','Positif':'#2ecc71'}

# === SIDEBAR ===
st.sidebar.title("🧠 TemanMood")
st.sidebar.markdown("Dashboard Analisis Mood & Aktivitas")

page = st.sidebar.radio("Navigasi", ["📊 Overview", "🏃 Aktivitas", "🔗 Mood-Aktivitas", "⏰ Analisis Waktu", "💡 Rekomendasi"])

mood_filter = st.sidebar.multiselect("Filter Mood", mood_order, default=mood_order)
df_filtered = df[df['mood'].isin(mood_filter)]
df_exp_filtered = df_exploded[df_exploded['mood'].isin(mood_filter)]

# === PAGES ===
if page == "📊 Overview":
    st.title("📊 Overview Mood Pengguna")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Entri", len(df_filtered))
    c2.metric("Rata-rata Mood", f"{df_filtered['mood_score'].mean():.2f}")
    c3.metric("Mood Terbaik", df_filtered['mood'].mode().iloc[0] if len(df_filtered) > 0 else "-")
    c4.metric("Aktivitas Unik", df_exp_filtered['activities_list'].nunique())

    col1, col2 = st.columns(2)
    with col1:
        counts = df_filtered['mood'].value_counts().reindex(mood_order).fillna(0)
        fig = px.bar(x=counts.index, y=counts.values, color=counts.index,
                     color_discrete_map=mood_colors, title="Distribusi Mood")
        fig.update_layout(xaxis_title="Mood", yaxis_title="Jumlah", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.pie(values=counts.values, names=counts.index,
                     color=counts.index, color_discrete_map=mood_colors, title="Proporsi Mood")
        st.plotly_chart(fig, use_container_width=True)

    monthly = df_filtered.groupby(df_filtered['full_date'].dt.to_period('M'))['mood_score'].mean()
    monthly.index = monthly.index.astype(str)
    fig = px.line(x=monthly.index, y=monthly.values, title="Trend Mood Score per Bulan",
                  labels={'x':'Bulan','y':'Mood Score'})
    fig.add_hline(y=3, line_dash="dash", line_color="gray", annotation_text="Netral")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🏃 Aktivitas":
    st.title("🏃 Analisis Aktivitas")

    top_n = st.slider("Jumlah Top Aktivitas", 5, 20, 10)
    top_act = df_exp_filtered['activities_list'].value_counts().head(top_n)

    fig = px.bar(x=top_act.values, y=top_act.index, orientation='h',
                 color=top_act.values, color_continuous_scale='viridis',
                 title=f"Top {top_n} Aktivitas")
    fig.update_layout(yaxis=dict(autorange="reversed"), xaxis_title="Frekuensi", yaxis_title="Aktivitas")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Distribusi Jumlah Aktivitas per Entri")
    fig = px.histogram(df_filtered, x='activity_count', nbins=20, title="Distribusi Jumlah Aktivitas",
                       color_discrete_sequence=['#3498db'])
    st.plotly_chart(fig, use_container_width=True)

elif page == "🔗 Mood-Aktivitas":
    st.title("🔗 Hubungan Mood & Aktivitas")

    top10 = df_exp_filtered['activities_list'].value_counts().head(10).index
    df_top = df_exp_filtered[df_exp_filtered['activities_list'].isin(top10)]
    heatmap = pd.crosstab(df_top['activities_list'], df_top['mood'], normalize='index') * 100
    heatmap = heatmap.reindex(columns=[m for m in mood_order if m in heatmap.columns])

    fig = px.imshow(heatmap, text_auto='.1f', color_continuous_scale='YlOrRd',
                    title="Proporsi Mood per Aktivitas (%)", aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Mood Score per Aktivitas")
    act_score = df_exp_filtered.groupby('activities_list')['mood_score'].agg(['mean','count'])
    act_score = act_score[act_score['count'] >= 10].sort_values('mean', ascending=False).head(15)
    fig = px.bar(x=act_score.index, y=act_score['mean'], color=act_score['mean'],
                 color_continuous_scale='RdYlGn', title="Rata-rata Mood Score per Aktivitas (min 10 entries)")
    fig.add_hline(y=3, line_dash="dash", line_color="gray")
    st.plotly_chart(fig, use_container_width=True)

elif page == "⏰ Analisis Waktu":
    st.title("⏰ Analisis Berbasis Waktu")

    col1, col2 = st.columns(2)
    with col1:
        day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        day_score = df_filtered.groupby('weekday')['mood_score'].mean().reindex(day_order)
        fig = px.bar(x=day_score.index, y=day_score.values, color=day_score.values,
                     color_continuous_scale='RdYlGn', title="Mood Score per Hari")
        fig.add_hline(y=day_score.mean(), line_dash="dash", annotation_text="Rata-rata")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        time_order = ['Pagi','Siang','Sore','Malam']
        time_score = df_filtered.groupby('time_category')['mood_score'].mean().reindex(time_order)
        fig = px.bar(x=time_score.index, y=time_score.values, color=time_score.values,
                     color_continuous_scale='RdYlGn', title="Mood Score per Waktu")
        st.plotly_chart(fig, use_container_width=True)

    day_mood = pd.crosstab(df_filtered['weekday'], df_filtered['mood'], normalize='index') * 100
    day_mood = day_mood.reindex(day_order)
    day_mood = day_mood[[m for m in mood_order if m in day_mood.columns]]
    fig = px.imshow(day_mood, text_auto='.1f', color_continuous_scale='YlOrRd',
                    title="Heatmap: Hari vs Mood (%)", aspect="auto")
    st.plotly_chart(fig, use_container_width=True)

elif page == "💡 Rekomendasi":
    st.title("💡 Sistem Rekomendasi Aktivitas")

    selected_mood = st.selectbox("Pilih Mood Anda Saat Ini:", mood_order)

    df_mood = df_exp_filtered[df_exp_filtered['mood'] == selected_mood]
    top_activities = df_mood['activities_list'].value_counts().head(5)

    msgs = {
        "Positif": "Pertahankan energi positif dan lanjutkan rutinitas baikmu! 🌟",
        "Netral": "Lakukan aktivitas ringan untuk boost mood. 🙂",
        "Negatif": "Tidak apa-apa merasa kurang baik. Prioritaskan istirahat dan pemulihan. 💙"
    }

    st.info(msgs.get(selected_mood, "Jaga keseimbangan emosi."))

    st.subheader(f"Top 5 Aktivitas Saat Mood '{selected_mood}'")
    for i, (act, count) in enumerate(top_activities.items(), 1):
        st.write(f"**{i}. {act}** — {count} kali dilakukan")

    if len(top_activities) > 0:
        fig = px.bar(x=top_activities.index, y=top_activities.values,
                     color=top_activities.values, color_continuous_scale='viridis',
                     title=f"Aktivitas Rekomendasi untuk Mood '{selected_mood}'")
        st.plotly_chart(fig, use_container_width=True)

# === FOOTER ===
st.sidebar.markdown("---")
st.sidebar.markdown("**Capstone DBS 2026**")
st.sidebar.markdown("Data: Daylio Mood Tracker")
