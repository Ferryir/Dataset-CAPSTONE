# 📊 Dataset — Teman Mood

Folder ini berisi **pipeline Data Science end-to-end** untuk proyek **Teman Mood**: mulai dari data mentah, notebook analisis, dashboard interaktif, hingga dataset bersih yang siap digunakan oleh AI Engineer.

---

## 📁 Struktur Folder

```
Dataset/
├── Daylio_Abid.csv                     ← Dataset mentah (sumber)
├── capstone_data_scientist_dbs26.ipynb  ← Notebook analisis (pipeline utama)
├── app.py                              ← Dashboard Streamlit interaktif
├── temanmood_recommendation.json       ← Mapping rekomendasi aktivitas per mood
├── requirements.txt                    ← Dependensi Python
├── README.md                           ← Dokumentasi (file ini)
└── output/                             ← Hasil ekspor data bersih
    ├── all_moods_cleaned.csv           ← Seluruh data bersih (1 file)
    ├── mood_awful.csv                  ← Data mood: Awful
    ├── mood_bad.csv                    ← Data mood: Bad
    ├── mood_normal.csv                 ← Data mood: Normal
    ├── mood_good.csv                   ← Data mood: Good
    ├── mood_amazing.csv               ← Data mood: Amazing
    └── temanmood_recommendation.json   ← Mapping rekomendasi (output notebook)
```

---

## 📥 Sumber Data

| Item       | Detail                                                                                     |
| ---------- | ------------------------------------------------------------------------------------------ |
| **Dataset**    | [Kaggle — Daylio Mood Tracker](https://www.kaggle.com/datasets/kingabzpro/daylio-mood-tracker) |
| **Ukuran**     | 940 entri (baris mentah)                                                                   |
| **File**       | `Daylio_Abid.csv`                                                                          |
| **Deskripsi**  | Catatan mood harian pengguna aplikasi Daylio beserta aktivitas yang dilakukan               |

---

## 📋 Data Dictionary

### Dataset Mentah (`Daylio_Abid.csv`)

| No | Kolom       | Tipe     | Deskripsi                                          |
| -- | ----------- | -------- | -------------------------------------------------- |
| 1  | `full_date` | object   | Tanggal pencatatan (format: `dd/mm/yyyy`)          |
| 2  | `date`      | object   | Format singkat tanggal                             |
| 3  | `weekday`   | object   | Hari dalam seminggu (Monday–Sunday)                |
| 4  | `time`      | object   | Waktu pencatatan (format 12 jam AM/PM)             |
| 5  | `mood`      | object   | **Label klasifikasi**: Awful / Bad / Normal / Good / Amazing |
| 6  | `sub_mood`  | object   | Emosi spesifik (sub-kategori mood)                 |
| 7  | `activities`| object   | Daftar aktivitas, dipisahkan dengan pipe (`\|`)    |

### Dataset Bersih (`output/all_moods_cleaned.csv`)

Kolom hasil proses **data wrangling** dan **feature engineering**:

| No | Kolom            | Tipe     | Deskripsi                                  |
| -- | ---------------- | -------- | ------------------------------------------ |
| 1  | `full_date`      | datetime | Tanggal (sudah dikonversi)                 |
| 2  | `weekday`        | object   | Hari dalam seminggu                        |
| 3  | `hour`           | int      | Jam pencatatan (0–23)                      |
| 4  | `mood`           | object   | Label mood: Awful / Bad / Normal / Good / Amazing |
| 5  | `mood_score`     | int      | Skor numerik mood (1–5)                    |
| 6  | `sub_mood`       | object   | Sub-kategori emosi                         |
| 7  | `activities`     | object   | Aktivitas mentah (pipe-separated)          |
| 8  | `activity_count` | int      | Jumlah aktivitas per entri                 |
| 9  | `is_weekend`     | int      | 1 jika hari weekend, 0 jika weekday        |
| 10 | `has_meditation` | int      | 1 jika ada aktivitas meditasi              |
| 11 | `has_exercise`   | int      | 1 jika ada aktivitas olahraga              |
| 12 | `mood_positive`  | int      | 1 jika mood positif (Good/Amazing)         |

---

## 🔬 Pipeline Analisis

Pipeline yang dijalankan melalui notebook `capstone_data_scientist_dbs26.ipynb`:

```
1. Problem Discovery     → Identifikasi masalah & solusi
2. Data Wrangling        → Gathering, Assessing, Cleaning
3. Pertanyaan Bisnis     → 4 pertanyaan terukur
4. EDA                   → Distribusi mood, top aktivitas, heatmap
5. Explanatory Analysis  → Menjawab pertanyaan bisnis dengan data
6. Feature Engineering   → 6 fitur baru untuk modeling
7. A/B Testing           → Mann-Whitney U Test (meditasi vs non-meditasi)
8. Ekspor Data           → CSV per mood + JSON rekomendasi
```

### Proses Data Wrangling

| Langkah | Tindakan                                          |
| ------- | ------------------------------------------------- |
| 1       | Drop baris dengan `activities` kosong (47 baris)  |
| 2       | Strip whitespace pada kolom `mood`, `sub_mood`    |
| 3       | Konversi `full_date` ke tipe datetime             |
| 4       | Parsing jam dari kolom `time` (12h → 24h)         |
| 5       | Split aktivitas pipe-separated menjadi list       |

### Feature Engineering

| Fitur              | Deskripsi                                      |
| ------------------ | ---------------------------------------------- |
| `mood_score`       | Mapping mood ke skor numerik (1–5)             |
| `activity_count`   | Jumlah aktivitas yang dicatat per entri        |
| `is_weekend`       | Flag weekend (Saturday/Sunday = 1)             |
| `has_meditation`   | Flag ada/tidaknya meditasi                     |
| `has_exercise`     | Flag ada/tidaknya olahraga (walk, exercise, yoga, hiking) |
| `mood_positive`    | Flag mood positif (Good/Amazing = 1)           |

### A/B Testing

| Parameter | Detail                              |
| --------- | ----------------------------------- |
| Grup A    | Hari dengan meditasi                |
| Grup B    | Hari tanpa meditasi                 |
| Metrik    | Mood Score (1–5)                    |
| Metode    | Mann-Whitney U Test                 |
| α (alpha) | 0.05                                |

---

## 📄 Mapping Rekomendasi (`temanmood_recommendation.json`)

File JSON berisi rekomendasi aktivitas berbasis data untuk setiap kategori mood:

```json
{
  "Awful": {
    "recommendation_message": "Ini hari yang berat. Prioritaskan istirahat dan pemulihan.",
    "scientific_references": ["Sleep Foundation", "Mental Health America"],
    "top_activities": ["youtube", "streaming", "Dota 2", "Audio books", "good meal"],
    "activities_distribution": [...]
  },
  ...
}
```

Setiap mood memiliki:
- **`recommendation_message`** — Pesan motivasi kontekstual
- **`scientific_references`** — Referensi ilmiah pendukung
- **`top_activities`** — 5 aktivitas teratas berdasarkan frekuensi
- **`activities_distribution`** — 10 aktivitas dengan `count` dan `weight`

---

## 🖥️ Dashboard Streamlit (`app.py`)

Dashboard interaktif dengan 5 halaman:

| Halaman              | Deskripsi                                           |
| -------------------- | --------------------------------------------------- |
| 📊 Overview          | Metrik ringkasan, distribusi mood, tren bulanan     |
| 🏃 Aktivitas         | Top aktivitas, distribusi jumlah aktivitas per entri |
| 🔗 Mood-Aktivitas    | Heatmap proporsi mood per aktivitas, mood score     |
| ⏰ Analisis Waktu    | Mood score per hari & waktu, heatmap hari vs mood   |
| 💡 Rekomendasi       | Sistem rekomendasi aktivitas berdasarkan mood        |

### Menjalankan Dashboard

```bash
# 1. Install dependensi
pip install -r requirements.txt

# 2. Jalankan dashboard
streamlit run app.py
```

---

## 📦 Dependensi

```
pandas
numpy
seaborn
matplotlib
scipy
streamlit
plotly
```

Install semua dependensi:

```bash
pip install -r requirements.txt
```

---

## 🏷️ Label Klasifikasi Mood

| Mood      | Skor | Warna   | Jumlah File Output       |
| --------- | ---- | ------- | ------------------------ |
| Awful     | 1    | 🔴 Merah  | `output/mood_awful.csv`   |
| Bad       | 2    | 🟠 Orange | `output/mood_bad.csv`     |
| Normal    | 3    | 🟡 Kuning | `output/mood_normal.csv`  |
| Good      | 4    | 🟢 Hijau  | `output/mood_good.csv`    |
| Amazing   | 5    | 🔵 Biru   | `output/mood_amazing.csv` |

---

## 🚀 Cara Penggunaan

### Untuk Data Scientist

1. Buka dan jalankan `capstone_data_scientist_dbs26.ipynb` untuk mereproduksi seluruh analisis
2. Hasil data bersih akan diekspor ke folder `output/`

### Untuk AI Engineer

1. Gunakan file di folder `output/` sebagai input untuk membangun model klasifikasi mood
2. `all_moods_cleaned.csv` — dataset lengkap dengan semua fitur
3. `mood_*.csv` — dataset per kategori mood (sudah terklasifikasi)
4. `temanmood_recommendation.json` — mapping rekomendasi untuk sistem AI

### Untuk Deployment

1. Jalankan `streamlit run app.py` untuk melihat dashboard interaktif
2. Dashboard membaca langsung dari `Daylio_Abid.csv` dan `temanmood_recommendation.json`

---

## 📝 Catatan

- Dataset berasal dari **sumber publik** (Kaggle) dan telah melalui proses **data wrangling** sebelum digunakan
- Notebook dirancang untuk **Capstone Project DBS Coding Camp 2026**
- Semua visualisasi menggunakan **matplotlib**, **seaborn** (notebook), dan **Plotly** (dashboard)
- Ekspor laporan PDF dapat dilakukan melalui notebook: *File → Print → Save as PDF*
