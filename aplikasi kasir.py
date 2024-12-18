import tkinter as tk
from tkinter import messagebox
import datetime as dt
import os

daftar_barang = {
    "magelangan": 12000,
    "indomie": 7000,
    "nutrisari": 5000,
    "teh": 3000,
    "nasi goreng": 15000,
}

pembelian = {}

if not os.path.exists("receipts"):
    os.makedirs("receipts")

def add_item():
    barang = item_var.get().lower()
    jumlah = int(quantity_var.get())
    
    if barang in daftar_barang:
        if barang in pembelian:
            pembelian[barang] += jumlah
        else:
            pembelian[barang] = jumlah
        update_cart()
    else:
        messagebox.showerror("Error", "Barang tidak tersedia.")

def update_cart():
    cart_text.delete(1.0, tk.END)
    for barang, jumlah in pembelian.items():
        cart_text.insert(tk.END, f"{barang}: {jumlah} pcs\n")
    total_label.config(text=f"Total: Rp. {totalbelanja()}")

def totalbelanja():
    total_tagihan = 0
    for barang, jumlah in pembelian.items():
        total_tagihan += daftar_barang[barang] * jumlah
    return total_tagihan

def process_payment():
    try:
        jumlhuang = int(payment_var.get())
        tagihan = totalbelanja()
        if jumlhuang < tagihan:
            messagebox.showerror("Error", "Uang tidak cukup.")
            return
        
        kembalian_amount = jumlhuang - tagihan
        show_receipt(nama_var.get(), tagihan, jumlhuang, kembalian_amount)
    except ValueError:
        messagebox.showerror("Error", "Masukkan jumlah uang yang valid.")

def show_receipt(nama, tagihan, uang, kembalian):
    waktu = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    struk_text = f"==============================\n====STRUK====\n==============================\n"
    struk_text += f"NAMA : {nama}\n"
    struk_text += f"Tagihan : Rp. {tagihan}\n"
    for barang, jumlah in pembelian.items():
        struk_text += f"{barang}: {jumlah} pcs\n"
    struk_text += f"Uang : Rp. {uang}\n"
    struk_text += f"Kembalian : Rp. {kembalian}\n"
    struk_text += f"Waktu pemesanan : {waktu}\n"
    
    save_receipt(nama, struk_text)

    receipt_window = tk.Toplevel(root)
    receipt_window.title("Struk Pembelian")
    receipt_text = tk.Text(receipt_window, height=15, width=40)
    receipt_text.insert(tk.END, struk_text)
    receipt_text.pack()
    tk.Button(receipt_window, text="Tutup", command=receipt_window.destroy).pack()

def save_receipt(nama, struk_text):
    filename = f"receipts/struk_{nama}_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as file:
        file.write(struk_text)

def view_history():
    history_window = tk.Toplevel(root)
    history_window.title("Riwayat Struk")
    
    history_text = tk.Text(history_window, height=20, width=50)
    history_text.pack()

    for filename in os.listdir("receipts"):
        if filename.endswith(".txt"):
            with open(os.path.join("receipts", filename), 'r') as file:
                history_text.insert(tk.END, file.read() + "\n\n")

root = tk.Tk()
root.title("Kasir")

tk.Label(root, text="Nama Pelanggan:").grid(row=0, column=0)
nama_var = tk.StringVar()
tk .Entry(root, textvariable=nama_var).grid(row=0, column=1)

tk.Label(root, text="Pilih Barang:").grid(row=1, column=0)
item_var = tk.StringVar()
item_menu = tk.OptionMenu(root, item_var, *daftar_barang.keys())
item_menu.grid(row=1, column=1)

tk.Label(root, text="Jumlah:").grid(row=2, column=0)
quantity_var = tk.StringVar()
tk.Entry(root, textvariable=quantity_var).grid(row=2, column=1)

tk.Button(root, text="Tambah ke Keranjang", command=add_item).grid(row=3, columnspan=2)

cart_text = tk.Text(root, height=10, width=30)
cart_text.grid(row=4, columnspan=2)

total_label = tk.Label(root, text="Total: Rp. 0")
total_label.grid(row=5, columnspan=2)

tk.Label(root, text="Jumlah Uang:").grid(row=6, column=0)
payment_var = tk.StringVar()
tk.Entry(root, textvariable=payment_var).grid(row=6, column=1)

tk.Button(root, text="Proses Pembayaran", command=process_payment).grid(row=7, columnspan=2)

tk.Button(root, text="Lihat Riwayat Struk", command=view_history).grid(row=8, columnspan=2)

root.mainloop()