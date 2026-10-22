import tkinter as tk

def prediksi_prodi():
    label_hasil.config(text="Hasil Prediksi: Teknologi Informasi")


root = tk.Tk()
root.title("Aplikasi Prediksi Prodi Pilihan")
root.geometry("450x550")
root.configure(padx=20, pady=20)

label_judul = tk.Label(
    root, 
    text="Aplikasi Prediksi Prodi Pilihan", 
    font=("Helvetica", 16, "bold"),
    pady=10
)
label_judul.pack()

frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

entries = []
for i in range(1, 11):
    row_frame = tk.Frame(frame_inputs)
    row_frame.pack(fill="x", pady=2)
    
    lbl = tk.Label(row_frame, text=f"Nilai Mata Pelajaran {i}:", width=22, anchor="w")
    lbl.pack(side="left")
    
    entry = tk.Entry(row_frame, width=15)
    entry.pack(side="right")
    entries.append(entry)

btn_prediksi = tk.Button(
    root, 
    text="Hasil Prediksi", 
    command=prediksi_prodi,
    fg="Black", 
    font=("Helvetica", 10, "bold"),
    padx=10, 
    pady=5
)
btn_prediksi.pack(pady=15)

label_hasil = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 12, "bold"), 
    fg="blue"
)
label_hasil.pack(pady=5)

root.mainloop()