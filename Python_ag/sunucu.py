import socket

# Sunucu soketi oluşturulur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Sunucu IP adresi ve port numarasına bağlanır
server_socket.bind(('localhost', 8080))

# Bağlantılar dinlenir
server_socket.listen(1)
print("Sunucu dinlemede...")

# İstemciden gelen bağlantı kabul edilir
client_socket, client_address = server_socket.accept()
print(f"Bağlantı kabul edildi: {client_address}")

# Veri alışverişi yapılır
data = client_socket.recv(1024)
print(f"Gelen veri: {data.decode()}")

client_socket.sendall("Veri alındı".encode())

# Bağlantı kapatılır
client_socket.close()
server_socket.close()
