import base64

def decode_base64_multiple_times(encoded_string, times):
    decoded_string = encoded_string
    for _ in range(times):
        decoded_string = base64.b64decode(decoded_string).decode('utf-8')
    return decoded_string

def decode_file(file_path, times):
    with open(file_path, "r") as file:
        encoded_content = file.read()
    decoded_content = decode_base64_multiple_times(encoded_content, times)
    return decoded_content

# Örnek kullanım
file_path = "base64.txt"  # Base64 ile kodlanmış metin içeren dosya yolu
times =50  # Çözme sayısı

# Dosya içeriğini belirli bir sayıda base64 ile çözme
decoded_content = decode_file(file_path, times)
print("Çözülen içerik:")
print(decoded_content)
