import tkinter as tk
from tkinter import messagebox

# Kelas Token bertugas mengenali jenis kata (S, P, O, K) dalam kalimat
class Token:
    def __init__(self):
        # Daftar kata-kata yang dikenal
        self.S = ["Aku", "Kamu", "Sean", "Rio", "Azmi"]
        self.P = ["membaca", "menulis", "menggambar", "bermain", "memasak"]
        self.O = ["buku", "surat", "mobil", "bola", "laptop"]
        self.K = ["di kampus", "di kostan", "di asrama", "di rumah", "di kantor"]

    # Fungsi untuk mengenali jenis kata
    def recognize(self, kata):
        if kata in self.S:
            return 'S'
        elif kata in self.P:
            return 'P'
        elif kata in self.O:
            return 'O'
        elif kata in self.K:
            return 'K'
        else:
            return '-'

# Kelas Parser bertugas memeriksa struktur kalimat
class Parser:
    def __init__(self, token):
        self.token = token
    
    def bersihkan_kalimat(self, kalimat):
        return ' '.join(kalimat.split())

    # Fungsi untuk memeriksa apakah struktur kalimat valid
    def cek(self, kalimat):
        kalimat = self.bersihkan_kalimat(kalimat)
        token = kalimat.split()
        stack = []
        i = 0

        # Memeriksa setiap token dalam kalimat
        while i < len(token):
            # Menggabungkan token multi-kata jika ditemukan
            if i < len(token) - 1 and f"{token[i]} {token[i+1]}" in self.token.K:
                kata = f"{token[i]} {token[i+1]}"
                i += 1
            else:
                kata = token[i]

            # Mengenali jenis kata
            kenal = self.token.recognize(kata)
            if kenal == '-':
                return False

            # Memeriksa urutan kata sesuai aturan struktur
            if kenal == 'S':
                if not stack:
                    stack.append('S')
                else:
                    return False
            elif kenal == 'P':
                if stack == ['S']:
                    stack.append('P')
                else:
                    return False
            elif kenal == 'O':
                if stack == ['S', 'P']:
                    stack.append('O')
                else:
                    return False
            elif kenal == 'K':
                if stack in [['S', 'P'], ['S', 'P', 'O']]:
                    stack.append('K')
                else:
                    return False

            i += 1

        # Mengembalikan hasil stack jika struktur valid
        if stack in [['S', 'P'], ['S', 'P', 'O'], ['S', 'P', 'O', 'K'], ['S', 'P', 'K']]:
            return stack  # Mengembalikan daftar stack
        else:
            return False  # Mengembalikan False jika tidak valid

# Kelas MyGUI bertugas membuat antarmuka grafis untuk aplikasi
class MyGUI:
    def __init__(self, Parser):
        self.root = tk.Tk()
        self.root.geometry("400x250")  # Sesuaikan ukuran jendela
        self.root.title("Program Tugas Besar TBA")
        self.root.configure(bg="#f0f0f0")  # Warna latar belakang jendela

        # Judul Program (Label)
        self.label_judul = tk.Label(
            self.root, 
            text="Program Kelompok X", 
            font=("Arial", 20, "bold"),  # Font tebal
            fg="#333333",  # Warna teks
            bg="#f0f0f0"  # Warna latar belakang
        )
        self.label_judul.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        # Tombol Anggota (Di Tengah)
        self.button_anggota = tk.Button(
            self.root,
            text="Anggota",
            command=self.list_anggota,
            width=15, 
            height=2,  # Ukuran tombol
            font=("Arial", 12),
            fg="#ffffff",  # Warna teks tombol
            bg="#008080"  # Warna latar belakang tombol
        )
        self.button_anggota.grid(row=1, column=0, padx=10, pady=10, sticky="ew") 

        # Tombol Program (Di Tengah)
        self.button_program = tk.Button(
            self.root, 
            text="Program", 
            command=self.mulai,
            width=15, 
            height=2,
            font=("Arial", 12),
            fg="#ffffff",
            bg="#008080"
        )
        self.button_program.grid(row=1, column=1, padx=10, pady=10, sticky="ew")  

        # Tombol Keluar (Di Tengah)
        self.button_keluar = tk.Button(
            self.root, 
            text="Exit", 
            command=self.root.destroy,
            width=15,
            height=2,
            font=("Arial", 12),
            fg="#ffffff",
            bg="#008080"
        )
        self.button_keluar.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")  

        # Menyimpan referensi ke objek Parser
        self.Parser = Parser

        self.root.mainloop()

    # Fungsi untuk menampilkan daftar anggota kelompok
    def list_anggota(self):
        self.anggota_window = tk.Tk()
        self.anggota_window.geometry("300x150")
        self.anggota_window.title("List Anggota Tugas Besar TBA")

        # Label untuk setiap anggota kelompok
        self.label_azmi = tk.Label(self.anggota_window, text="1. Muhammad Azmi", font=('Arial', 12))
        self.label_azmi.pack(padx=5, pady=5)

        self.label_riodino = tk.Label(self.anggota_window, text="2. Riodino Raihan", font=('Arial', 12))
        self.label_riodino.pack(padx=5, pady=5)

        self.label_sean = tk.Label(self.anggota_window, text="3. Sean Willian F.", font=('Arial', 12))
        self.label_sean.pack(padx=5, pady=5)

        # Tombol untuk kembali ke menu utama
        self.button_back = tk.Button(self.anggota_window, text="Back", command=self.anggota_window.destroy)
        self.button_back.pack(padx=10, pady=8)

    # Fungsi untuk memulai program pemeriksaan kalimat
    def mulai(self):
        self.program_window = tk.Tk()
        self.program_window.geometry("250x100")
        self.program_window.title("Program Tugas Besar TBA")
        self.label_kalimat = tk.Label(self.program_window, text="Masukkan kalimat: ")
        self.label_kalimat.pack()

        # Kotak entri untuk memasukkan kalimat
        self.entry_kalimat = tk.Entry(self.program_window, width=30)
        self.entry_kalimat.pack()

        # Tombol untuk memeriksa kalimat yang dimasukkan
        self.button_periksa = tk.Button(self.program_window, text="Periksa", command=self.cek_kalimat)
        self.button_periksa.pack(padx=10, pady=10)

    # Fungsi untuk memeriksa kalimat yang dimasukkan
    def cek_kalimat(self):
        kalimat = self.entry_kalimat.get()
        # Menampilkan pesan berdasarkan hasil pemeriksaan kalimat
        if self.Parser.cek(kalimat):
            # Mendapatkan hasil stack dari Parser
            stack = self.Parser.cek(kalimat)
            output = "".join(stack)  # Menggabungkan elemen stack menjadi string
            messagebox.showinfo("Output", f"Struktur dikenali: {output}") 
        else:
            messagebox.showerror("Output", "Struktur tidak dikenali")

# Main program
if __name__ == "__main__":
    # Membuat objek Token dan Parser
    token = Token()
    parser = Parser(token)

    # Membuat antarmuka grafis
    MyGUI(parser)