import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
import requests
from bs4 import BeautifulSoup, Comment
import threading

# Yorumları çekme fonksiyonu
def get_comments(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            return comments
        else:
            return None
    except requests.exceptions.RequestException:
        return None

# Dosya yükleme fonksiyonu
def on_file_load():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])  # Dosya açma penceresi
    if file_path:
        try:
            with open(file_path, 'r') as file:
                urls = file.readlines()  # Dosyadaki her satırdaki URL'yi al
                all_comments = []  # Tüm yorumları buraya toplayacağız
                load_comments(urls, all_comments)

        except Exception as e:
            messagebox.showerror("Hata", f"Dosya işlenirken bir hata oluştu: {e}")

# Yorumları yüklerken asenkron işlem
def load_comments(urls, all_comments):
    comment_box.delete(1.0, tk.END)  # Önceki yorumları sil
    comment_box.insert(tk.END, "Yorumlar Yükleniyor...\n")
    for url in urls:
        url = url.strip()
        if url:
            comments = get_comments(url)
            if comments:
                all_comments.append(f"Yorumlar: {url}")
                for comment in comments:
                    all_comments.append(comment.strip())  # Yorumları ekle
                all_comments.append('\n' + '-'*50 + '\n')  # Yorumlar arasında ayırıcı ekle
            else:
                all_comments.append(f"Yorum bulunamadı: {url}")
                all_comments.append('-'*50)
    
    # Sonuçları TextBox'a yazdır
    for comment in all_comments:
        comment_box.insert(tk.END, comment + '\n')

# Yorumları kaydetme fonksiyonu
def save_results():
    result = comment_box.get(1.0, tk.END)  # Text kutusundaki veriyi al
    
    if not result.strip():
        messagebox.showwarning("Uyarı", "Henüz hiçbir sonuç yok!")
        return
    
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(result)  # Yorumları dosyaya kaydet
            messagebox.showinfo("Başarılı", "Sonuçlar başarıyla kaydedildi!")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu: {e}")

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Yorum Bulucu")
root.geometry("700x600")
root.configure(bg="#f0f0f0")  # Arka plan rengini yumuşak gri yaptık

# Menü çubuğu oluştur
menu_bar = tk.Menu(root, bg="#4CAF50", fg="white")

# Dosya menüsünü ekle
file_menu = tk.Menu(menu_bar, tearoff=0, bg="#f0f0f0", fg="black")
file_menu.add_command(label="Dosya Yükle", command=on_file_load)  # Dosya yükle
file_menu.add_separator()
file_menu.add_command(label="Çıkış", command=root.quit)  # Çıkış

menu_bar.add_cascade(label="Dosya", menu=file_menu)  # Dosya menüsünü menü barına ekle

# Sonuçlar menüsünü ekle
result_menu = tk.Menu(menu_bar, tearoff=0, bg="#f0f0f0", fg="black")
result_menu.add_command(label="Sonuçları Kaydet", command=save_results)  # Sonuçları kaydet
menu_bar.add_cascade(label="Sonuçlar", menu=result_menu)  # Sonuçlar menüsünü menü barına ekle

root.config(menu=menu_bar)  # Menü barı pencereye ekle

# URL girme kısmı
url_label = tk.Label(root, text="Web Sitesinin URL'sini Girin:", font=('Arial', 12), bg="#f0f0f0")
url_label.pack(pady=10)

url_entry = tk.Entry(root, width=50, font=('Arial', 10), bd=2, relief="solid", highlightthickness=1)
url_entry.pack(pady=10)

# Yorumları gösteren scrolled text (kaydırılabilir metin kutusu)
comment_box = scrolledtext.ScrolledText(root, width=70, height=20, font=('Arial', 10), bd=2, relief="solid")
comment_box.pack(pady=10)

# Yorumları çekme butonu
fetch_button = tk.Button(root, text="Sonuçları Göster", command=lambda: threading.Thread(target=get_comments, args=(url_entry.get(),)).start(), font=('Arial', 10, 'bold'), bg="#4CAF50", fg="white", relief="raised")
fetch_button.pack(pady=20, fill=tk.X)

# Sonuçları kaydetme butonu
save_button = tk.Button(root, text="Sonuçları Kaydet", command=save_results, font=('Arial', 10, 'bold'), bg="#2196F3", fg="white", relief="raised")
save_button.pack(pady=10, fill=tk.X)

# Ana döngüyü başlat
root.mainloop()
