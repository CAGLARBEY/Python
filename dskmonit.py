import shutil

# Disk kullanımını kontrol etmek için fonksiyon
def check_disk_usage(path, threshold):
    total, used, free = shutil.disk_usage(path)
    usage_percent = (used / total) * 100
    return usage_percent

# Ana fonksiyon
def monitor_disk_usage():
    disk_path = "/"  # Kontrol edilecek disk (Linux için kök dizin, Windows için örn. 'C:\\')
    threshold = 80   # Eşik değeri (%)
    
    usage = check_disk_usage(disk_path, threshold)
    print(f"Disk Kullanımı: {usage:.2f}%")
    
    if usage > threshold:
        print(f"UYARI: {disk_path} kullanım oranı {usage:.2f}% ile kritik seviyeyi aştı!")
    else:
        print(f"{disk_path} kullanım oranı normal: {usage:.2f}%.")

if __name__ == "__main__":
    monitor_disk_usage()
