import sqlite3
import tkinter as tk
import tkinter.messagebox as msg


def create_db():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS nilai_siswa
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nama_siswa TEXT NOT NULL,
                       biologi INTEGER NOT NULL,
                       fisika INTEGER NOT NULL,
                       inggris INTEGER NOT NULL,
                       prediksi_fakultas TEXT NOT NULL)''')
    conn.commit()
    conn.close()


def prediksi(bio, fis, ing):
    if ing > bio and ing > fis:
        return "Bahasa"
    elif bio > ing and bio > fis:
        return "Kedokteran"
    elif fis > ing and fis > bio:
        return "Teknik"
    return "Gausah Kuliah"


def tampilkan_data():
    listbox.delete(0, tk.END)
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    for baris in cursor.fetchall():
        listbox.insert(tk.END, baris)
    conn.close()


def submit():
    nama = entry_nama.get()
    bio = entry_bio.get()
    fis = entry_fis.get()
    ing = entry_ing.get()
    if nama == "" or bio == "" or fis == "" or ing == "":
        msg.showerror("Error", "Semua nilai harus diisi!")
        return
    if not (bio.isdigit() and fis.isdigit() and ing.isdigit()):
        msg.showerror("Error", "Nilai harus angka!")
        return
    bio = int(bio)
    fis = int(fis)
    ing = int(ing)

    fakultas = prediksi(bio, fis, ing)
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas) VALUES (?, ?, ?, ?, ?)",
                   (nama, bio, fis, ing, fakultas))
    conn.commit()
    conn.close()

    msg.showinfo("Hasil", nama + " diprediksi untuk masuk ke  " + fakultas)
    tampilkan_data()

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)


create_db()
window = tk.Tk()
window.title("Prediksi Skor")
window.geometry("600x400")

tk.Label(window, text="Nama:").grid(row=0, column=0, padx=5, pady=3, sticky="w")
entry_nama = tk.Entry(window)
entry_nama.grid(row=0, column=1, padx=5, pady=3)

tk.Label(window, text="Skor Biologi:").grid(row=1, column=0, padx=5, pady=3, sticky="w")
entry_bio = tk.Entry(window)
entry_bio.grid(row=1, column=1, padx=5, pady=3)

tk.Label(window, text="Skor Fisika:").grid(row=2, column=0, padx=5, pady=3, sticky="w")
entry_fis = tk.Entry(window)
entry_fis.grid(row=2, column=1, padx=5, pady=3)

tk.Label(window, text="Skor Inggris:").grid(row=3, column=0, padx=5, pady=3, sticky="w")
entry_ing = tk.Entry(window)
entry_ing.grid(row=3, column=1, padx=5, pady=3)

tk.Button(window, text="Submit", command=submit).grid(row=4, column=0, columnspan=2, pady=10)

listbox = tk.Listbox(window, width=80)
listbox.grid(row=5, column=0, columnspan=2, padx=5)

tampilkan_data()
window.mainloop()