import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


DB_NAME = "prediksi_diabetes.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS riwayat_pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT NOT NULL,
            usia INTEGER NOT NULL,
            gula_darah REAL NOT NULL,
            bmi REAL NOT NULL,
            riwayat_ortu TEXT NOT NULL,
            hasil_prediksi TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


init_db()



def hitung_prediksi(gula_darah, bmi, riwayat_ortu):
    has_history = riwayat_ortu == "Ya"

    if gula_darah >= 200:
        if bmi >= 30 or has_history:
            return "Sangat Tinggi", "#d9534f"  
        return "Tinggi", "#f0ad4e"  

    elif 140 <= gula_darah <= 199:
        if bmi >= 30 or has_history:
            return "Tinggi", "#f0ad4e"  
        return "Sedang", "#ffc107"  

    else:  
        if bmi >= 30:
            return "Sedang", "#ffc107"  
        elif has_history:
            return "Waspada", "#17a2b8"  
        else:
            return "Rendah", "#28a745"  


def simpan_data():
    nama = entry_nama.get().strip()
    usia_str = entry_usia.get().strip()
    gula_str = entry_gula.get().strip()
    bmi_str = entry_bmi.get().strip()
    riwayat = combo_riwayat.get()

   
    if not nama or not usia_str or not gula_str or not bmi_str or not riwayat:
        messagebox.showwarning("Validasi Gagal", "Semua kolom harus diisi!")
        return

    try:
        usia = int(usia_str)
        gula_darah = float(gula_str)
        bmi = float(bmi_str)

        if usia <= 0 or gula_darah <= 0 or bmi <= 0:
            raise ValueError()
    except ValueError:
        messagebox.showerror(
            "Validasi Gagal",
            "Usia, Gula Darah, dan BMI harus berupa angka positif!",
        )
        return

   
    hasil, warna = hitung_prediksi(gula_darah, bmi, riwayat)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO riwayat_pasien (nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        (nama, usia, gula_darah, bmi, riwayat, hasil),
    )
    conn.commit()
    conn.close()

  
    lbl_hasil_val.config(text=hasil, bg=warna, fg="white")

    messagebox.showinfo(
        "Sukses", f"Data pasien {nama} berhasil disimpan ke database!"
    )
    reset_form()


def reset_form():
    entry_nama.delete(0, tk.END)
    entry_usia.delete(0, tk.END)
    entry_gula.delete(0, tk.END)
    entry_bmi.delete(0, tk.END)
    combo_riwayat.set("")


def tampilkan_data():
    win_data = tk.Toplevel(root)
    win_data.title("Riwayat Data Pasien")
    win_data.geometry("650x300")

    columns = (
        "id",
        "nama_pasien",
        "usia",
        "gula_darah",
        "bmi",
        "riwayat_ortu",
        "hasil_prediksi",
    )
    tree = ttk.Treeview(win_data, columns=columns, show="headings")

    tree.heading("id", text="ID")
    tree.heading("nama_pasien", text="Nama Pasien")
    tree.heading("usia", text="Usia")
    tree.heading("gula_darah", text="Gula Darah")
    tree.heading("bmi", text="BMI")
    tree.heading("riwayat_ortu", text="Riwayat Ortu")
    tree.heading("hasil_prediksi", text="Hasil Prediksi")

    tree.column("id", width=30, anchor="center")
    tree.column("nama_pasien", width=120)
    tree.column("usia", width=50, anchor="center")
    tree.column("gula_darah", width=80, anchor="center")
    tree.column("bmi", width=60, anchor="center")
    tree.column("riwayat_ortu", width=90, anchor="center")
    tree.column("hasil_prediksi", width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM riwayat_pasien")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)



root = tk.Tk()
root.title("Aplikasi Prediksi Risiko Diabetes")
root.geometry("420x450")
root.configure(padx=20, pady=20)


tk.Label(
    root, text="Form Prediksi Diabetes", font=("Helvetica", 14, "bold")
).grid(row=0, column=0, columnspan=2, pady=10)


tk.Label(root, text="Nama Pasien:").grid(row=1, column=0, sticky="w", pady=5)
entry_nama = tk.Entry(root, width=25)
entry_nama.grid(row=1, column=1, pady=5)

tk.Label(root, text="Usia (tahun):").grid(row=2, column=0, sticky="w", pady=5)
entry_usia = tk.Entry(root, width=25)
entry_usia.grid(row=2, column=1, pady=5)

tk.Label(root, text="Gula Darah (mg/dL):").grid(
    row=3, column=0, sticky="w", pady=5
)
entry_gula = tk.Entry(root, width=25)
entry_gula.grid(row=3, column=1, pady=5)

tk.Label(root, text="BMI:").grid(row=4, column=0, sticky="w", pady=5)
entry_bmi = tk.Entry(root, width=25)
entry_bmi.grid(row=4, column=1, pady=5)

tk.Label(root, text="Riwayat Ortu:").grid(row=5, column=0, sticky="w", pady=5)
combo_riwayat = ttk.Combobox(
    root, values=["Ya", "Tidak"], state="readonly", width=22
)
combo_riwayat.grid(row=5, column=1, pady=5)

btn_hitung = tk.Button(
    root,
    text="Prediksi & Simpan Data",
    fg="white",
    command=simpan_data,
)
btn_hitung.grid(row=6, column=0, columnspan=2, pady=15, sticky="we")

tk.Label(
    root, text="Hasil Prediksi Risiko:", font=("Helvetica", 10, "bold")
).grid(row=7, column=0, sticky="w", pady=5)
lbl_hasil_val = tk.Label(
    root,
    text="-",
    font=("Helvetica", 11, "bold"),
    width=15,
    relief="groove",
)
lbl_hasil_val.grid(row=7, column=1, pady=5, sticky="w")

btn_view = tk.Button(
    root,
    text="Lihat Data Pasien",
    fg="white",
    command=tampilkan_data,
)
btn_view.grid(row=8, column=0, columnspan=2, pady=10, sticky="we")

root.mainloop()