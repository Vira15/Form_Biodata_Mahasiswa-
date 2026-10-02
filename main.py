"""
Aplikasi Form Biodata Desktop Mahasiswa
Materi: Pemrograman Visual Desktop (Pertemuan 02)
Teknologi: Python 3, Tkinter, dan ttk

Fitur:
- Input Lengkap: Nama, NIM, Tanggal Lahir, Jenis Kelamin, Program Studi, Semester, Email, Hobi, Alamat
- Validasi Lengkap: Field wajib, NIM angka, format Tanggal (DD-MM-YYYY), format Email, minimal 1 hobi
- Penyimpanan Multi-Data (In-Memory)
- Tabel Sederhana (ttk.Treeview) dengan seleksi baris untuk melihat detail
- Tombol: SIMPAN, RESET, BERSIHKAN DATA, KELUAR
- Tampilan Modern, Rapi, dan Responsif
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re


# ==============================================================================
# STRUKTUR DATA IN-MEMORY (Penyimpanan Sementara Selama Aplikasi Berjalan)
# ==============================================================================
daftar_mahasiswa = []


# ==============================================================================
# FUNGSI VALIDASI DATA
# ==============================================================================

def validasi_email(email_str):
    """
    Validasi format email standar menggunakan regular expression.
    Format yang valid: nama@domain.ekstensi (contoh: vira@kampus.ac.id)
    """
    pola = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pola, email_str) is not None


def validasi_data():
    """
    Melakukan validasi seluruh input formulir biodata.
    Mengembalikan: (is_valid: bool, pesan_atau_data: dict/str, widget_fokus)
    """
    nama = entry_nama.get().strip()
    nim = entry_nim.get().strip()
    tgl_lahir = entry_tgl_lahir.get().strip()
    jenis_kelamin = var_jk.get().strip()
    prodi = combo_prodi.get().strip()
    semester = combo_semester.get().strip()
    email = entry_email.get().strip()
    alamat = text_alamat.get("1.0", tk.END).strip()

    # Kumpulkan hobi yang dicentang
    hobi_list = []
    if var_hobi_membaca.get():
        hobi_list.append("Membaca")
    if var_hobi_musik.get():
        hobi_list.append("Musik")
    if var_hobi_olahraga.get():
        hobi_list.append("Olahraga")
    if var_hobi_gaming.get():
        hobi_list.append("Gaming")

    # 1. Validasi Nama Lengkap (Field Wajib)
    if not nama:
        return False, "Nama Lengkap tidak boleh kosong!", entry_nama

    # 2. Validasi NIM (Field Wajib & Hanya Angka)
    if not nim:
        return False, "NIM tidak boleh kosong!", entry_nim
    if not nim.isdigit():
        return False, "NIM harus berupa angka!", entry_nim

    # 3. Validasi Tanggal Lahir (Field Wajib & Format DD-MM-YYYY)
    if not tgl_lahir:
        return False, "Tanggal Lahir tidak boleh kosong!", entry_tgl_lahir
    try:
        datetime.strptime(tgl_lahir, "%d-%m-%Y")
    except ValueError:
        return False, "Format Tanggal Lahir harus DD-MM-YYYY (contoh: 25-04-2003)!", entry_tgl_lahir

    # 4. Validasi Jenis Kelamin (Field Wajib)
    if not jenis_kelamin:
        return False, "Silakan pilih Jenis Kelamin!", None

    # 5. Validasi Program Studi (Field Wajib)
    if not prodi or prodi == "-- Pilih Program Studi --":
        return False, "Silakan pilih Program Studi!", combo_prodi

    # 6. Validasi Semester (Field Wajib)
    if not semester or semester == "-- Pilih Semester --":
        return False, "Silakan pilih Semester!", combo_semester

    # 7. Validasi Email (Field Wajib & Format Email)
    if not email:
        return False, "Email tidak boleh kosong!", entry_email
    if not validasi_email(email):
        return False, "Format Email tidak valid!\nContoh yang benar: mahasiswa@kampus.ac.id", entry_email

    # 8. Validasi Hobi (Minimal 1 Hobi Dipilih)
    if not hobi_list:
        return False, "Pilih minimal satu Hobi!", None

    # 9. Validasi Alamat (Field Wajib)
    if not alamat:
        return False, "Alamat tidak boleh kosong!", text_alamat

    # Jika seluruh data valid
    data_bersih = {
        "nama": nama,
        "nim": nim,
        "tgl_lahir": tgl_lahir,
        "jenis_kelamin": jenis_kelamin,
        "prodi": prodi,
        "semester": semester,
        "email": email,
        "hobi": ", ".join(hobi_list),
        "alamat": alamat,
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }
    return True, data_bersih, None


# ==============================================================================
# FUNGSI MANIPULASI DATA & EVENT HANDLER
# ==============================================================================

def perbarui_tabel():
    """
    Me-refresh seluruh baris pada widget Treeview berdasarkan daftar_mahasiswa.
    """
    # Hapus semua data yang sedang ditampilkan di tabel
    for row in tree_tabel.get_children():
        tree_tabel.delete(row)

    # Masukkan ulang semua data dari list
    for idx, mhs in enumerate(daftar_mahasiswa, start=1):
        tree_tabel.insert(
            "",
            "end",
            iid=str(idx - 1),
            values=(
                idx,
                mhs["nim"],
                mhs["nama"],
                mhs["prodi"],
                f"Smt {mhs['semester']}",
                mhs["jenis_kelamin"]
            )
        )

    # Perbarui label jumlah data
    lbl_total_data.config(text=f"Total Tersimpan: {len(daftar_mahasiswa)} Mahasiswa")


def tampilkan_detail(mhs):
    """
    Menampilkan detail lengkap satu data mahasiswa pada area teks hasil.
    """
    text_hasil.config(state="normal")
    text_hasil.delete("1.0", tk.END)

    detail_str = (
        "================================================================\n"
        "                    DETAIL BIODATA MAHASISWA                    \n"
        "================================================================\n"
        f"Nama Lengkap    : {mhs['nama']}\n"
        f"NIM             : {mhs['nim']}\n"
        f"Tanggal Lahir   : {mhs['tgl_lahir']}\n"
        f"Jenis Kelamin   : {mhs['jenis_kelamin']}\n"
        f"Program Studi   : {mhs['prodi']}\n"
        f"Semester        : Semester {mhs['semester']}\n"
        f"Email           : {mhs['email']}\n"
        f"Hobi            : {mhs['hobi']}\n"
        f"Alamat          : {mhs['alamat']}\n"
        "----------------------------------------------------------------\n"
        f"Waktu Tersimpan : {mhs['waktu']}\n"
        "================================================================\n"
    )
    text_hasil.insert(tk.END, detail_str)
    text_hasil.config(state="disabled")


def on_select_tabel(event):
    """
    Event handler saat pengguna mengklik baris pada tabel data mahasiswa.
    Menampilkan detail data baris tersebut di area hasil.
    """
    selected_items = tree_tabel.selection()
    if not selected_items:
        return

    idx_str = selected_items[0]
    try:
        idx = int(idx_str)
        if 0 <= idx < len(daftar_mahasiswa):
            mhs = daftar_mahasiswa[idx]
            tampilkan_detail(mhs)
    except (ValueError, IndexError):
        pass


def simpan_data():
    """
    Handler tombol SIMPAN:
    1. Memvalidasi data input.
    2. Menyimpan data ke dalam list in-memory.
    3. Memperbarui tabel Treeview.
    4. Menampilkan detail pada area hasil.
    5. Mengosongkan form input agar siap untuk pengisian data berikutnya.
    """
    is_valid, hasil, widget = validasi_data()

    if not is_valid:
        messagebox.showwarning("Peringatan Validasi", hasil)
        if widget and hasattr(widget, "focus_set"):
            widget.focus_set()
        return

    # Tambahkan data baru ke list
    daftar_mahasiswa.append(hasil)

    # Perbarui tabel
    perbarui_tabel()

    # Pilih baris data yang baru saja ditambahkan
    idx_baru = str(len(daftar_mahasiswa) - 1)
    tree_tabel.selection_set(idx_baru)
    tree_tabel.see(idx_baru)

    # Tampilkan detail data yang baru disimpan
    tampilkan_detail(hasil)

    messagebox.showinfo(
        "Sukses",
        f"Data biodata untuk '{hasil['nama']}' berhasil disimpan ke dalam tabel!"
    )

    # Reset formulir input agar siap untuk input data mahasiswa baru berikutnya
    reset_input_form()


def reset_input_form():
    """
    Mengosongkan isian formulir input tanpa menghapus data tabel atau detail.
    """
    entry_nama.delete(0, tk.END)
    entry_nim.delete(0, tk.END)
    entry_tgl_lahir.delete(0, tk.END)
    var_jk.set("")
    combo_prodi.current(0)
    combo_semester.current(0)
    entry_email.delete(0, tk.END)
    var_hobi_membaca.set(False)
    var_hobi_musik.set(False)
    var_hobi_olahraga.set(False)
    var_hobi_gaming.set(False)
    text_alamat.delete("1.0", tk.END)
    entry_nama.focus_set()


def reset_form():
    """
    Handler tombol RESET:
    Mengosongkan formulir input dan mereset area detail ke teks placeholder.
    (Tidak menghapus data yang tersimpan di tabel).
    """
    reset_input_form()

    # Bersihkan area detail
    text_hasil.config(state="normal")
    text_hasil.delete("1.0", tk.END)
    text_hasil.insert(
        tk.END,
        "Formulir telah direset.\n"
        "Pilih salah satu baris pada tabel di atas untuk melihat detail biodata,\n"
        "atau isi formulir lalu tekan 'SIMPAN DATA' untuk menambah data baru.\n"
    )
    text_hasil.config(state="disabled")


def bersihkan_data():
    """
    Handler tombol BERSIHKAN DATA:
    Menghapus seluruh data mahasiswa yang tersimpan di memori dan tabel setelah konfirmasi.
    """
    if not daftar_mahasiswa:
        messagebox.showinfo("Informasi", "Belum ada data mahasiswa yang tersimpan di tabel.")
        return

    konfirmasi = messagebox.askyesno(
        "Konfirmasi Bersihkan Data",
        f"Apakah Anda yakin ingin menghapus seluruh data ({len(daftar_mahasiswa)} mahasiswa) yang tersimpan di tabel?\n\n"
        "Data yang dihapus tidak dapat dikembalikan."
    )

    if konfirmasi:
        daftar_mahasiswa.clear()
        perbarui_tabel()

        # Reset area hasil
        text_hasil.config(state="normal")
        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(
            tk.END,
            "Semua data mahasiswa telah dibersihkan.\n"
            "Tabel saat ini kosong. Silakan input biodata baru melalui formulir di sebelah kiri.\n"
        )
        text_hasil.config(state="disabled")

        messagebox.showinfo("Data Dibersihkan", "Seluruh data mahasiswa berhasil dihapus dari tabel.")


def keluar_aplikasi():
    """
    Handler tombol KELUAR:
    Meminta konfirmasi pengguna sebelum menutup aplikasi.
    """
    jawaban = messagebox.askyesno(
        "Konfirmasi Keluar",
        "Apakah Anda yakin ingin keluar dari aplikasi Form Biodata?"
    )
    if jawaban:
        root.destroy()


# ==============================================================================
# INISIALISASI WINDOW UTAMA
# ==============================================================================

root = tk.Tk()
root.title("Form Biodata Diri - Pemrograman Visual Desktop")
root.geometry("1060x720")
root.minsize(980, 660)

# Posisikan window di tengah layar monitor
root.update_idletasks()
lebar_layar = root.winfo_screenwidth()
tinggi_layar = root.winfo_screenheight()
pos_x = max(10, (lebar_layar // 2) - (1060 // 2))
pos_y = max(10, (tinggi_layar // 2) - (720 // 2) - 20)
root.geometry(f"1060x720+{pos_x}+{pos_y}")

# Tangani event penutupan window lewat tombol X (silang)
root.protocol("WM_DELETE_WINDOW", keluar_aplikasi)


# ==============================================================================
# TEMA & STYLE APLIKASI
# ==============================================================================

style = ttk.Style()
style.theme_use("clam")

# Palet warna modern
BG_MAIN = "#F1F5F9"        # Latar utama
BG_CARD = "#FFFFFF"        # Kartu putih
HEADER_BG = "#1E293B"      # Header slate gelap
HEADER_FG = "#FFFFFF"
HEADER_SUB = "#94A3B8"
PRIMARY = "#2563EB"        # Biru (Simpan)
PRIMARY_HOVER = "#1D4ED8"
WARNING = "#F59E0B"        # Oranye/Amber (Reset)
WARNING_HOVER = "#D97706"
DANGER = "#DC2626"         # Merah (Bersihkan)
DANGER_HOVER = "#B91C1C"
DARK_BTN = "#334155"       # Slate (Keluar)
DARK_BTN_HOVER = "#1E293B"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#64748B"
BORDER_COLOR = "#CBD5E1"

root.configure(bg=BG_MAIN)

# Konfigurasi style ttk global
style.configure(".", background=BG_MAIN, font=("Segoe UI", 9))
style.configure("TLabelframe", background=BG_CARD, bordercolor=BORDER_COLOR, relief="solid", borderwidth=1)
style.configure("TLabelframe.Label", background=BG_CARD, foreground=TEXT_DARK, font=("Segoe UI", 9, "bold"))
style.configure("TLabel", background=BG_CARD, foreground=TEXT_DARK, font=("Segoe UI", 9))
style.configure("TEntry", fieldbackground="#FFFFFF", foreground=TEXT_DARK)
style.configure("TRadiobutton", background=BG_CARD, foreground=TEXT_DARK, font=("Segoe UI", 9))
style.configure("TCheckbutton", background=BG_CARD, foreground=TEXT_DARK, font=("Segoe UI", 9))
style.configure("TCombobox", fieldbackground="#FFFFFF", foreground=TEXT_DARK)

# Konfigurasi style Treeview
style.configure(
    "Treeview",
    background="#FFFFFF",
    fieldbackground="#FFFFFF",
    foreground=TEXT_DARK,
    rowheight=24,
    font=("Segoe UI", 9)
)
style.configure(
    "Treeview.Heading",
    background="#E2E8F0",
    foreground=TEXT_DARK,
    font=("Segoe UI", 9, "bold"),
    relief="flat"
)
style.map("Treeview", background=[("selected", "#2563EB")], foreground=[("selected", "#FFFFFF")])
style.map("Treeview.Heading", background=[("active", "#CBD5E1")])


# ==============================================================================
# HEADER APLIKASI
# ==============================================================================

header_frame = tk.Frame(root, bg=HEADER_BG, pady=10, padx=16)
header_frame.pack(fill="x")

lbl_judul = tk.Label(
    header_frame,
    text="FORM BIODATA MAHASISWA",
    font=("Segoe UI", 14, "bold"),
    fg=HEADER_FG,
    bg=HEADER_BG
)
lbl_judul.pack(anchor="w")

lbl_subjudul = tk.Label(
    header_frame,
    text="Pemrograman Visual Desktop - Pertemuan 02 | Validasi Data & Penyimpanan Multi-Record",
    font=("Segoe UI", 8),
    fg=HEADER_SUB,
    bg=HEADER_BG
)
lbl_subjudul.pack(anchor="w")


# ==============================================================================
# CONTAINER DUA KOLOM (Kiri: Formulir, Kanan: Tabel & Detail)
# ==============================================================================

body_container = tk.Frame(root, bg=BG_MAIN, padx=12, pady=10)
body_container.pack(fill="both", expand=True)

# Grid 2 kolom: Kiri bobot 4, Kanan bobot 6
body_container.columnconfigure(0, weight=4)
body_container.columnconfigure(1, weight=6)
body_container.rowconfigure(0, weight=1)


# ==============================================================================
# KOLOM KIRI: FORMULIR INPUT BIODATA
# ==============================================================================

left_frame = tk.Frame(body_container, bg=BG_MAIN)
left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
left_frame.rowconfigure(0, weight=1)
left_frame.columnconfigure(0, weight=1)

card_form = ttk.LabelFrame(left_frame, text=" Formulir Input Data ", padding=(14, 10))
card_form.grid(row=0, column=0, sticky="nsew")
card_form.columnconfigure(1, weight=1)

# 1. Nama Lengkap (Entry)
lbl_nama = ttk.Label(card_form, text="Nama Lengkap *")
lbl_nama.grid(row=0, column=0, sticky="w", pady=3)
entry_nama = ttk.Entry(card_form)
entry_nama.grid(row=0, column=1, sticky="ew", pady=3, padx=(8, 0))

# 2. NIM (Entry)
lbl_nim = ttk.Label(card_form, text="NIM *")
lbl_nim.grid(row=1, column=0, sticky="w", pady=3)
entry_nim = ttk.Entry(card_form)
entry_nim.grid(row=1, column=1, sticky="ew", pady=3, padx=(8, 0))

# 3. Tanggal Lahir (Entry)
lbl_tgl = ttk.Label(card_form, text="Tanggal Lahir *")
lbl_tgl.grid(row=2, column=0, sticky="w", pady=3)

frame_tgl = tk.Frame(card_form, bg=BG_CARD)
frame_tgl.grid(row=2, column=1, sticky="ew", pady=3, padx=(8, 0))
frame_tgl.columnconfigure(0, weight=1)

entry_tgl_lahir = ttk.Entry(frame_tgl)
entry_tgl_lahir.grid(row=0, column=0, sticky="ew")

lbl_hint_tgl = tk.Label(frame_tgl, text="(DD-MM-YYYY)", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD)
lbl_hint_tgl.grid(row=0, column=1, padx=(6, 0), sticky="w")

# 4. Jenis Kelamin (Radiobutton)
lbl_jk = ttk.Label(card_form, text="Jenis Kelamin *")
lbl_jk.grid(row=3, column=0, sticky="w", pady=3)

frame_jk = tk.Frame(card_form, bg=BG_CARD)
frame_jk.grid(row=3, column=1, sticky="w", pady=3, padx=(8, 0))

var_jk = tk.StringVar(value="")
rb_lk = ttk.Radiobutton(frame_jk, text="Laki-laki", value="Laki-laki", variable=var_jk)
rb_lk.pack(side="left", padx=(0, 12))
rb_pr = ttk.Radiobutton(frame_jk, text="Perempuan", value="Perempuan", variable=var_jk)
rb_pr.pack(side="left")

# 5. Program Studi (Combobox)
lbl_prodi = ttk.Label(card_form, text="Program Studi *")
lbl_prodi.grid(row=4, column=0, sticky="w", pady=3)

daftar_prodi = [
    "-- Pilih Program Studi --",
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Komputer",
    "Sains Data",
    "Teknologi Informasi",
    "Rekayasa Perangkat Lunak",
    "Manajemen Informatika"
]
combo_prodi = ttk.Combobox(card_form, values=daftar_prodi, state="readonly")
combo_prodi.current(0)
combo_prodi.grid(row=4, column=1, sticky="ew", pady=3, padx=(8, 0))

# 6. Semester (Combobox)
lbl_semester = ttk.Label(card_form, text="Semester *")
lbl_semester.grid(row=5, column=0, sticky="w", pady=3)

daftar_semester = ["-- Pilih Semester --"] + [f"Semester {i}" for i in range(1, 9)]
combo_semester = ttk.Combobox(card_form, values=daftar_semester, state="readonly")
combo_semester.current(0)
combo_semester.grid(row=5, column=1, sticky="ew", pady=3, padx=(8, 0))

# 7. Email (Entry)
lbl_email = ttk.Label(card_form, text="Email *")
lbl_email.grid(row=6, column=0, sticky="w", pady=3)
entry_email = ttk.Entry(card_form)
entry_email.grid(row=6, column=1, sticky="ew", pady=3, padx=(8, 0))

# 8. Hobi (Checkbutton)
lbl_hobi = ttk.Label(card_form, text="Hobi (Min. 1) *")
lbl_hobi.grid(row=7, column=0, sticky="w", pady=3)

frame_hobi = tk.Frame(card_form, bg=BG_CARD)
frame_hobi.grid(row=7, column=1, sticky="w", pady=3, padx=(8, 0))

var_hobi_membaca = tk.BooleanVar(value=False)
var_hobi_musik = tk.BooleanVar(value=False)
var_hobi_olahraga = tk.BooleanVar(value=False)
var_hobi_gaming = tk.BooleanVar(value=False)

cb_membaca = ttk.Checkbutton(frame_hobi, text="Membaca", variable=var_hobi_membaca)
cb_membaca.pack(side="left", padx=(0, 6))

cb_musik = ttk.Checkbutton(frame_hobi, text="Musik", variable=var_hobi_musik)
cb_musik.pack(side="left", padx=(0, 6))

cb_olahraga = ttk.Checkbutton(frame_hobi, text="Olahraga", variable=var_hobi_olahraga)
cb_olahraga.pack(side="left", padx=(0, 6))

cb_gaming = ttk.Checkbutton(frame_hobi, text="Gaming", variable=var_hobi_gaming)
cb_gaming.pack(side="left")

# 9. Alamat (Text)
lbl_alamat = ttk.Label(card_form, text="Alamat *")
lbl_alamat.grid(row=8, column=0, sticky="nw", pady=3)

frame_alamat = tk.Frame(card_form, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
frame_alamat.grid(row=8, column=1, sticky="ew", pady=3, padx=(8, 0))
frame_alamat.columnconfigure(0, weight=1)

text_alamat = tk.Text(
    frame_alamat,
    height=3,
    font=("Segoe UI", 9),
    bg="#FFFFFF",
    fg=TEXT_DARK,
    bd=0,
    wrap="word"
)
text_alamat.grid(row=0, column=0, sticky="ew", padx=3, pady=2)

scroll_alamat = ttk.Scrollbar(frame_alamat, orient="vertical", command=text_alamat.yview)
scroll_alamat.grid(row=0, column=1, sticky="ns")
text_alamat.config(yscrollcommand=scroll_alamat.set)

# Tombol Aksi Formulir (SIMPAN & RESET)
frame_btn_form = tk.Frame(card_form, bg=BG_CARD)
frame_btn_form.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(12, 0))

btn_simpan = tk.Button(
    frame_btn_form,
    text="✔  SIMPAN DATA",
    font=("Segoe UI", 9, "bold"),
    bg=PRIMARY,
    fg="#FFFFFF",
    activebackground=PRIMARY_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    padx=16,
    pady=6,
    command=simpan_data
)
btn_simpan.pack(side="left", padx=(0, 8))

btn_reset = tk.Button(
    frame_btn_form,
    text="↺  RESET FORM",
    font=("Segoe UI", 9, "bold"),
    bg=WARNING,
    fg="#FFFFFF",
    activebackground=WARNING_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    padx=14,
    pady=6,
    command=reset_form
)
btn_reset.pack(side="left")


# ==============================================================================
# KOLOM KANAN: TABEL DATA MAHASISWA & AREA DETAIL BIODATA
# ==============================================================================

right_frame = tk.Frame(body_container, bg=BG_MAIN)
right_frame.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
right_frame.columnconfigure(0, weight=1)
right_frame.rowconfigure(0, weight=3)  # Tabel
right_frame.rowconfigure(1, weight=2)  # Detail Hasil

# ------------------------------------------------------------------------------
# CARD 1: TABEL DATA MAHASISWA (Treeview)
# ------------------------------------------------------------------------------
card_tabel = ttk.LabelFrame(right_frame, text=" Tabel Data Mahasiswa Tersimpan ", padding=(10, 8))
card_tabel.grid(row=0, column=0, sticky="nsew", pady=(0, 8))
card_tabel.columnconfigure(0, weight=1)
card_tabel.rowconfigure(0, weight=1)

# Frame Tabel & Scrollbar
frame_tree = tk.Frame(card_tabel, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
frame_tree.grid(row=0, column=0, sticky="nsew")
frame_tree.columnconfigure(0, weight=1)
frame_tree.rowconfigure(0, weight=1)

kolom_tabel = ("no", "nim", "nama", "prodi", "semester", "jk")
tree_tabel = ttk.Treeview(
    frame_tree,
    columns=kolom_tabel,
    show="headings",
    selectmode="browse"
)

# Konfigurasi Header Kolom
tree_tabel.heading("no", text="No")
tree_tabel.heading("nim", text="NIM")
tree_tabel.heading("nama", text="Nama Lengkap")
tree_tabel.heading("prodi", text="Program Studi")
tree_tabel.heading("semester", text="Smt")
tree_tabel.heading("jk", text="Jenis Kelamin")

# Lebar dan Alignment Kolom
tree_tabel.column("no", width=35, anchor="center")
tree_tabel.column("nim", width=85, anchor="center")
tree_tabel.column("nama", width=140, anchor="w")
tree_tabel.column("prodi", width=125, anchor="w")
tree_tabel.column("semester", width=55, anchor="center")
tree_tabel.column("jk", width=80, anchor="center")

tree_tabel.grid(row=0, column=0, sticky="nsew")

# Scrollbar Vertikal & Horizontal untuk Tabel
scroll_tree_y = ttk.Scrollbar(frame_tree, orient="vertical", command=tree_tabel.yview)
scroll_tree_y.grid(row=0, column=1, sticky="ns")
tree_tabel.config(yscrollcommand=scroll_tree_y.set)

scroll_tree_x = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree_tabel.xview)
scroll_tree_x.grid(row=1, column=0, sticky="ew")
tree_tabel.config(xscrollcommand=scroll_tree_x.set)

# Binding event klik baris tabel
tree_tabel.bind("<<TreeviewSelect>>", on_select_tabel)

# Baris Kontrol di Bawah Tabel
frame_kontrol_tabel = tk.Frame(card_tabel, bg=BG_CARD)
frame_kontrol_tabel.grid(row=1, column=0, sticky="ew", pady=(6, 0))

lbl_total_data = tk.Label(
    frame_kontrol_tabel,
    text="Total Tersimpan: 0 Mahasiswa",
    font=("Segoe UI", 9, "bold"),
    fg=TEXT_DARK,
    bg=BG_CARD
)
lbl_total_data.pack(side="left")

btn_keluar = tk.Button(
    frame_kontrol_tabel,
    text="✖  KELUAR",
    font=("Segoe UI", 8, "bold"),
    bg=DARK_BTN,
    fg="#FFFFFF",
    activebackground=DARK_BTN_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=4,
    command=keluar_aplikasi
)
btn_keluar.pack(side="right")

btn_bersihkan = tk.Button(
    frame_kontrol_tabel,
    text="🗑  BERSIHKAN DATA",
    font=("Segoe UI", 8, "bold"),
    bg=DANGER,
    fg="#FFFFFF",
    activebackground=DANGER_HOVER,
    activeforeground="#FFFFFF",
    relief="flat",
    cursor="hand2",
    padx=12,
    pady=4,
    command=bersihkan_data
)
btn_bersihkan.pack(side="right", padx=(0, 6))

# ------------------------------------------------------------------------------
# CARD 2: DETAIL BIODATA TERPILIH (Area Hasil)
# ------------------------------------------------------------------------------
card_detail = ttk.LabelFrame(right_frame, text=" Detail Biodata Mahasiswa ", padding=(10, 8))
card_detail.grid(row=1, column=0, sticky="nsew")
card_detail.columnconfigure(0, weight=1)
card_detail.rowconfigure(0, weight=1)

frame_text_hasil = tk.Frame(card_detail, bg=BG_CARD, highlightbackground=BORDER_COLOR, highlightthickness=1)
frame_text_hasil.grid(row=0, column=0, sticky="nsew")
frame_text_hasil.columnconfigure(0, weight=1)
frame_text_hasil.rowconfigure(0, weight=1)

text_hasil = tk.Text(
    frame_text_hasil,
    font=("Consolas", 9),
    bg="#F8FAFC",
    fg=TEXT_DARK,
    bd=0,
    wrap="word",
    state="normal"
)
text_hasil.grid(row=0, column=0, sticky="nsew", padx=6, pady=4)

scroll_hasil = ttk.Scrollbar(frame_text_hasil, orient="vertical", command=text_hasil.yview)
scroll_hasil.grid(row=0, column=1, sticky="ns")
text_hasil.config(yscrollcommand=scroll_hasil.set)

# Pesan Awal pada Area Hasil
text_hasil.insert(
    tk.END,
    "Belum ada data yang dipilih.\n"
    "Isi formulir di sebelah kiri lalu klik 'SIMPAN DATA' untuk menyimpan biodata,\n"
    "atau klik salah satu baris pada tabel untuk melihat rincian biodata.\n"
)
text_hasil.config(state="disabled")

# Fokuskan kursor pada input pertama saat aplikasi dimulai
entry_nama.focus_set()


# ==============================================================================
# MAINLOOP APLIKASI
# ==============================================================================

if __name__ == "__main__":
    root.mainloop()
