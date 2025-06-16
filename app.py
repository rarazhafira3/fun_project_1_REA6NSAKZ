
import streamlit as st

# --- Data Pertanyaan ---
# Setiap pertanyaan adalah dictionary dengan:
# 'question': Teks pertanyaan
# 'options': List pilihan jawaban
# 'scores': Dictionary yang memetakan indeks jawaban ke skor kategori.
#           Format: {indeks_jawaban: {'Programmer': skor, 'Designer': skor, 'Data Scientist': skor}}
#           Skor yang lebih tinggi menunjukkan kecocokan yang lebih kuat dengan profesi tersebut.
questions = [
    {
        "question": "Ketika menghadapi masalah, pendekatanmu yang pertama adalah...",
        "options": [
            "Menganalisis data yang ada dan mencari pola tersembunyi.",
            "Membuat rencana sistematis dan menulis kode untuk solusinya.",
            "Mencari cara untuk memvisualisasikan masalah dan solusinya secara intuitif."
        ],
        "scores": {
            0: {'Programmer': 1, 'Designer': 0, 'Data Scientist': 3},  # Jawaban 1 cocok Data Scientist
            1: {'Programmer': 3, 'Designer': 1, 'Data Scientist': 1},  # Jawaban 2 cocok Programmer
            2: {'Programmer': 0, 'Designer': 3, 'Data Scientist': 0}   # Jawaban 3 cocok Designer
        }
    },
    {
        "question": "Software atau aplikasi apa yang paling menarik perhatianmu?",
        "options": [
            "Software yang bisa mengolah data besar dan menghasilkan insight.",
            "Game atau aplikasi yang memiliki antarmuka pengguna yang indah dan mudah digunakan.",
            "Tools pengembangan yang efisien dan memungkinkan untuk membangun sesuatu dari nol."
        ],
        "scores": {
            0: {'Programmer': 0, 'Designer': 0, 'Data Scientist': 3},
            1: {'Programmer': 0, 'Designer': 3, 'Data Scientist': 0},
            2: {'Programmer': 3, 'Designer': 1, 'Data Scientist': 0}
        }
    },
    {
        "question": "Mana yang lebih kamu sukai: bekerja dengan angka dan statistik, membuat desain visual yang menarik, atau membangun sistem yang kompleks?",
        "options": [
            "Bekerja dengan angka dan statistik.",
            "Membuat desain visual yang menarik.",
            "Membangun sistem yang kompleks."
        ],
        "scores": {
            0: {'Programmer': 1, 'Designer': 0, 'Data Scientist': 3},
            1: {'Programmer': 0, 'Designer': 3, 'Data Scientist': 0},
            2: {'Programmer': 3, 'Designer': 0, 'Data Scientist': 1}
        }
    },
    {
        "question": "Ketika memulai proyek baru, hal pertama yang kamu pikirkan adalah...",
        "options": [
            "Bagaimana data akan dikumpulkan, dianalisis, dan divisualisasikan.",
            "Struktur kode, algoritma, dan bagaimana mengimplementasikannya secara efisien.",
            "Pengalaman pengguna, estetika, dan bagaimana membuat interaksi yang intuitif."
        ],
        "scores": {
            0: {'Programmer': 0, 'Designer': 0, 'Data Scientist': 3},
            1: {'Programmer': 3, 'Designer': 1, 'Data Scientist': 0},
            2: {'Programmer': 0, 'Designer': 3, 'Data Scientist': 1}
        }
    },
    {
        "question": "Bagian mana dari sebuah website/aplikasi yang menurutmu paling krusial?",
        "options": [
            "Antarmuka pengguna (UI) dan pengalaman pengguna (UX).",
            "Fungsionalitas backend dan logika bisnis.",
            "Bagaimana data dikumpulkan, disimpan, dan digunakan untuk pengambilan keputusan."
        ],
        "scores": {
            0: {'Programmer': 0, 'Designer': 3, 'Data Scientist': 1},
            1: {'Programmer': 3, 'Designer': 1, 'Data Scientist': 0},
            2: {'Programmer': 1, 'Designer': 0, 'Data Scientist': 3}
        }
    },
]

# --- Inisialisasi State Aplikasi ---
# Gunakan st.session_state untuk menyimpan data yang perlu dipertahankan antar rerun Streamlit.
# Ini penting karena Streamlit menjalankan ulang seluruh script setiap kali ada interaksi.
if 'scores' not in st.session_state:
    st.session_state.scores = {'Programmer': 0, 'Designer': 0, 'Data Scientist': 0}
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'answers' not in st.session_state:
    # Menyimpan indeks jawaban yang dipilih pengguna untuk setiap pertanyaan.
    # Diinisialisasi dengan None untuk setiap pertanyaan.
    st.session_state.answers = [None] * len(questions)

# --- Tampilan Aplikasi ---
# Konfigurasi halaman Streamlit (judul tab browser, ikon, layout).
st.set_page_config(
    page_title="Mini Quiz App Profesi",
    page_icon="🧠", # Kamu bisa ganti ikon ini
    layout="centered" # Layout 'wide' jika ingin lebih lebar
)

st.title("🧠 Mini Quiz: Profesi yang Cocok Untukmu!")
st.write("Jawab pertanyaan-pertanyaan di bawah ini untuk mengetahui profesi yang paling cocok dengan minat dan kemampuanmu.")

# Bagian kuis akan ditampilkan jika kuis belum selesai
if not st.session_state.quiz_finished:
    # Gunakan st.form untuk mengelompokkan input dan tombol submit.
    # Ini memastikan bahwa aksi submit hanya terjadi saat tombol ditekan, bukan setiap perubahan radio button.
    with st.form(key='quiz_form'):
        user_answers = [] # List sementara untuk menyimpan jawaban pengguna saat form di-submit
        for i, q in enumerate(questions):
            st.markdown(f"**{i+1}. {q['question']}**") # Menampilkan pertanyaan dengan format Markdown (bold)

            # st.radio digunakan untuk pilihan ganda.
            # 'key' harus unik untuk setiap widget.
            # 'index' memuat jawaban yang sudah dipilih sebelumnya dari session_state.answers.
            selected_option = st.radio(
                "Pilih jawabanmu:",
                q['options'],
                key=f"q_{i}",
                index=st.session_state.answers[i] # Memuat jawaban sebelumnya jika ada
            )
            try:
                # Dapatkan indeks dari opsi yang dipilih.
                # Ini penting untuk mencari skor yang benar di dictionary 'scores'.
                selected_index = q['options'].index(selected_option)
                user_answers.append(selected_index)
            except ValueError:
                # Jika tidak ada yang dipilih (misalnya saat pertama kali aplikasi dimuat), anggap None.
                user_answers.append(None)
            st.write("---") # Garis pemisah antar pertanyaan untuk keterbacaan

        submit_button = st.form_submit_button("Lihat Hasil!")

        if submit_button:
            # Periksa apakah semua pertanyaan sudah dijawab sebelum menghitung skor
            if None in user_answers:
                st.warning("Mohon jawab semua pertanyaan sebelum melihat hasil.")
            else:
                # Reset skor sebelum menghitung ulang agar tidak ada akumulasi dari percobaan sebelumnya.
                st.session_state.scores = {'Programmer': 0, 'Designer': 0, 'Data Scientist': 0}
                st.session_state.answers = user_answers # Simpan jawaban final pengguna

                # Hitung skor berdasarkan jawaban yang dipilih
                for i, answer_index in enumerate(user_answers):
                    if answer_index is not None: # Pastikan ada jawaban yang dipilih
                        # Tambahkan skor dari jawaban yang dipilih ke total skor masing-masing profesi
                        if answer_index in questions[i]['scores']: # Pastikan indeks jawaban valid
                            for profession, score in questions[i]['scores'][answer_index].items():
                                st.session_state.scores[profession] += score

                st.session_state.quiz_finished = True # Set status kuis menjadi selesai
                st.rerun() # Refresh halaman untuk menampilkan bagian hasil
else:
    # --- Tampilkan Hasil Kuis ---
    st.subheader("🎉 Hasil Kuis Anda!")

    # Temukan profesi dengan skor tertinggi
    final_scores = st.session_state.scores
    if not final_scores or all(score == 0 for score in final_scores.values()):
        # Kasus jika tidak ada skor yang dihitung atau semua skor nol (mungkin karena belum menjawab)
        st.info("Sepertinya Anda belum menjawab semua pertanyaan atau skornya seimbang. Silakan coba lagi!")
    else:
        max_score = 0
        top_professions = []

        # Iterasi untuk menemukan skor tertinggi dan profesi terkait
        for profession, score in final_scores.items():
            if score > max_score:
                max_score = score
                top_professions = [profession]
            elif score == max_score and score > 0: # Tangani jika ada lebih dari satu profesi dengan skor tertinggi
                top_professions.append(profession)

        if len(top_professions) > 1:
            st.success(f"Anda cocok untuk beberapa profesi! Anda memiliki potensi kuat sebagai: **{', '.join(top_professions)}**.")
            st.write("Berikut adalah deskripsi singkatnya:")
            # Ganti URL dengan path lokal:
            if 'Programmer' in top_professions:
                st.image("assets/programmer.png", width=100) # <--- UBAH DI SINI
                st.write("**Programmer:** Jika Anda suka memecahkan masalah dengan kode, membangun aplikasi, dan menciptakan sesuatu dari nol.")
            if 'Designer' in top_professions:
                st.image("assets/designer.png", width=100) # <--- UBAH DI SINI
                st.write("**Designer:** Jika Anda memiliki mata untuk estetika, suka membuat antarmuka yang indah dan intuitif, serta memahami pengalaman pengguna.")
            if 'Data Scientist' in top_professions:
                st.image("assets/data_scientist.png", width=100) # <--- UBAH DI SINI
                st.write("**Data Scientist:** Jika Anda tertarik menganalisis data, menemukan pola tersembunyi, dan menggunakan statistik untuk membuat keputusan.")
        else:
           # ... kode sebelumnya untuk hasil profesi tunggal ...
            if result_profession == "Programmer":
                st.image("assets/programmer.png", width=100) # <--- UBAH DI SINI
                st.write("Anda memiliki jiwa **Programmer**! Anda suka memecahkan masalah dengan kode, membangun aplikasi, dan menciptakan sesuatu dari nol. Dunia koding dan logika adalah playground Anda.")
            elif result_profession == "Designer":
                st.image("assets/designer.png", width=100) # <--- UBAH DI SINI
                st.write("Anda memiliki jiwa **Designer**! Anda memiliki mata untuk estetika, suka membuat antarmuka yang indah dan intuitif, serta memahami pengalaman pengguna. Kreativitas adalah kunci Anda.")
            elif result_profession == "Data Scientist":
                st.image("assets/data_scientist.png", width=100) # <--- UBAH DI SINI
                st.write("Anda memiliki jiwa **Data Scientist**! Anda tertarik menganalisis data, menemukan pola tersembunyi, dan menggunakan statistik untuk membuat keputusan. Data adalah bahasa Anda.")

    st.write("---")
    # Tombol untuk mengulangi kuis (mereset semua state)
    if st.button("Ulangi Kuis"):
        st.session_state.scores = {'Programmer': 0, 'Designer': 0, 'Data Scientist': 0}
        st.session_state.quiz_finished = False
        st.session_state.answers = [None] * len(questions) # Reset jawaban tersimpan
        st.rerun() # Paksa Streamlit untuk menjalankan ulang skrip dari awal

# # Ini opsional: Tampilkan skor di sidebar untuk debug saat pengembangan
# st.sidebar.subheader("Skor Saat Ini (Debug):")
# st.sidebar.write(st.session_state.scores)
