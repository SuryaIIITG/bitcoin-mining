import socket

client = socket.socket()
client.connect(("localhost", 9998))

try:
    while True:
        data = client.recv(1024)
        if not data:
            break
        print("Received from server:", data.decode().strip())
except Exception as e:
    print("Client error:", e)
finally:
    client.close()

