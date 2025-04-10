import socket
import subprocess

# Start the mining proxy subprocess
process = subprocess.Popen(
    ["python", "mining_proxy.py", "-o", "us-east.stratum.slushpool.com", "-sh", "0.0.0.0", "-sp", "3333", "--enable-stratum-extensions"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True  # Use this instead of text=True for Python < 3.7
)

# Create a TCP server socket
s = socket.socket()
s.bind(("localhost", 9998))
s.listen(1)
print("Waiting for connection...")

# Accept connection from client
conn, addr = s.accept()
print("Connected by", addr)

try:
    # Stream subprocess output to the socket
    for line in process.stdout:
        if line.strip():
            print("Sending to client:", line.strip())
            conn.sendall((line.strip() + "\n").encode())  # Send with newline delimiter
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
    s.close()
    process.terminate()

