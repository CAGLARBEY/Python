import socket

# İstemci soketi oluşturulur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sunucuya bağlanılır
client_socket.connect(('localhost', 8080))

# Veri gönderilir
client_socket.sendall("Merhaba, sunucu!".encode())

# Sunucudan gelen veri alınır
data = client_socket.recv(1024)
print(f"Sunucudan gelen veri: {data.decode()}")

# Bağlantı kapatılır
client_socket.close()
