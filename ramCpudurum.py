import tkinter as tk
import psutil

# RAM kullanımını gösteren fonksiyon
def show_ram_usage():
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 ** 2)  # MB cinsinden
    available_memory = memory_info.available / (1024 ** 2)  # MB cinsinden
    used_memory = memory_info.used / (1024 ** 2)  # MB cinsinden
    memory_usage_percent = memory_info.percent
    output_label.config(text=f"RAM Kullanımı: {memory_usage_percent}%\n"
                             f"Toplam RAM: {total_memory:.2f} MB\n"
                             f"Kullanılan RAM: {used_memory:.2f} MB\n"
                             f"Kullanılabilir RAM: {available_memory:.2f} MB")

# CPU kullanımını gösteren fonksiyon
def show_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_times = psutil.cpu_times_percent(interval=1)
    output_label.config(text=f"CPU Kullanımı: {cpu_usage}%\n"
                             f"Kullanıcı Modu: {cpu_times.user}%\n"
                             f"Sistem Modu: {cpu_times.system}%\n"
                             f"Boşta: {cpu_times.idle}%")

# RAM ve CPU kullanımını bir arada gösteren fonksiyon
def show_ram_cpu_usage():
    memory_info = psutil.virtual_memory()
    total_memory = memory_info.total / (1024 ** 2)  # MB cinsinden
    available_memory = memory_info.available / (1024 ** 2)  # MB cinsinden
    used_memory = memory_info.used / (1024 ** 2)  # MB cinsinden
    memory_usage_percent = memory_info.percent

    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_times = psutil.cpu_times_percent(interval=1)

    output_label.config(text=f"RAM Kullanımı: {memory_usage_percent}%\n"
                             f"Toplam RAM: {total_memory:.2f} MB\n"
                             f"Kullanılan RAM: {used_memory:.2f} MB\n"
                             f"Kullanılabilir RAM: {available_memory:.2f} MB\n\n"
                             f"CPU Kullanımı: {cpu_usage}%\n"
                             f"Kullanıcı Modu: {cpu_times.user}%\n"
                             f"Sistem Modu: {cpu_times.system}%\n"
                             f"Boşta: {cpu_times.idle}%")

# Ana pencere oluşturma
root = tk.Tk()
root.title("Sistem Kullanımı İzleyici")
root.geometry("500x400")  # Pencere boyutunu ayarlama
root.configure(bg="black")  # Arka plan rengini siyah yapma

# Çıktı Etiketi
output_label = tk.Label(root, text="Sistem Bilgisi", font=("Helvetica", 14), justify="left", fg="white", bg="black", anchor="w")
output_label.pack(pady=20, padx=10, fill="x")

# RAM Kullanımı Butonu
ram_button = tk.Button(root, text="RAM Kullanımı", command=show_ram_usage, width=20, height=2)
ram_button.pack(pady=10)

# CPU Kullanımı Butonu
cpu_button = tk.Button(root, text="CPU Kullanımı", command=show_cpu_usage, width=20, height=2)
cpu_button.pack(pady=10)

# RAM ve CPU Kullanımı Butonu
ram_cpu_button = tk.Button(root, text="RAM ve CPU Kullanımı", command=show_ram_cpu_usage, width=20, height=2)
ram_cpu_button.pack(pady=10)

# Pencereyi çalıştırma
root.mainloop()
