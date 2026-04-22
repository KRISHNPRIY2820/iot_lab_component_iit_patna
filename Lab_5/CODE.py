import os
import urllib.parse
import socketserver
import http.server
import sys
import socket
import threading
import subprocess


def get_ip():
    try:
        return subprocess.check_output(['hostname', '-I']).decode().split()[0]
    except Exception:
        return "127.0.0.1"


def get_bt_addr():
    try:
        out = subprocess.check_output("hciconfig", text=True)
        for line in out.splitlines():
            if "BD Address" in line:
                return line.split("BD Address:")[1].split()[0]
    except Exception:
        return None


PI_IPs = ["10.42.0.1", "10.42.0.113"]
PI_BT_MACs = ["DC:A6:32:72:66:ED", "D8:3A:DD:0E:02:BC"]
MY_IP = get_ip()    # Pi 1 WiFi IP
MY_BT_MAC = get_bt_addr()
BT_PORT = 1
WIFI_PORT = 5000


HTTP_PORT = 8000
LOG_FILE = "msg.log"


def start_listener(addr, port, proto_type):
    if proto_type == socket.AF_BLUETOOTH:
        s = socket.socket(proto_type, socket.SOCK_STREAM,
                          socket.BTPROTO_RFCOMM)
    else:
        s = socket.socket(proto_type, socket.SOCK_STREAM)

    s.bind((addr, port))
    s.listen(1)
    print(f"Listening on {addr}... using ", proto_type)

    while True:
        client, client_info = s.accept()

        try:
            while True:  # Keep this connection open for multiple messages
                data = client.recv(1024)
                if not data:
                    # print("Client disconnected")
                    break

                msg = f"Received: {data.decode()}  | via {addr} \n"
                print(msg)
                with open(LOG_FILE, 'a') as f:
                    f.write(msg)
                client.send(b"Hi back!")
        except socket.error:
            pass
        finally:
            client.close()  # Now we close only when the loop finishes


def send_message(msg, pi_id):
    # Try Bluetooth first
    print("sending msg", msg)

    try:
        s = socket.socket(socket.AF_BLUETOOTH,
                          socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        s.settimeout(2.0)
        s.connect((PI_BT_MACs[pi_id], BT_PORT))

        send_msg = msg.encode()
        # Use sendall to ensure the entire buffer is transmitted
        s.sendall(send_msg)
        print(f"Sent msg - ( {msg} ) via BT")
        s.close()
        return True
    except socket.error as e:
        # Fallback to WiFi
        print("ble error msg - ", e)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((PI_IPs[pi_id], WIFI_PORT))
            print(
                f"Sent msg - ( {msg} ) to {PI_IPs[pi_id]} via WiFi (BT Out of Range)")
            s.send(msg.encode())
            s.close()
            return True
        except socket.error:
            print("Both connections failed")
            return False


if MY_IP is None or PI_BT_MACs is None:
    raise Exception("bad ip or mac")

# raise Exception("done")
print("ip -", MY_IP, "bt mac -", PI_BT_MACs)

PI_ID = 0
if len(sys.argv) != 2:
    print("provide arg")
    raise Exception("no arg")
elif sys.argv[1] == "pi1":
    PI_ID = 0
elif sys.argv[1] == "pi2":
    PI_ID = 1


# The HTML and JavaScript payload
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Polling Chat</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 20px auto; }
        #logArea { 
            height: 300px; 
            overflow-y: scroll; 
            border: 1px solid #ccc; 
            padding: 10px; 
            background: #f9f9f9;
            white-space: pre-wrap;
        }
        #msgForm { display: flex; margin-top: 10px; }
        #msgInput { flex-grow: 1; padding: 8px; font-size: 16px; }
        button { padding: 8px 16px; font-size: 16px; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Live Message Log</h2>
    <div id="logArea"></div>
    
    <form id="msgForm">
        <input type="text" id="msgInput" placeholder="Type a message..." required autocomplete="off">
        <button type="submit">Send</button>
    </form>

    <script>
        const logArea = document.getElementById('logArea');
        const msgForm = document.getElementById('msgForm');
        const msgInput = document.getElementById('msgInput');

        // 1. Poll the /log endpoint every 1000ms (1 second)
        setInterval(() => {
            fetch('/log')
                .then(response => response.text())
                .then(data => {
                    // Only update if data changed to prevent annoying scroll jumps
                    if (logArea.textContent !== data) {
                        logArea.textContent = data;
                        logArea.scrollTop = logArea.scrollHeight; // Auto-scroll to bottom
                    }
                })
                .catch(err => console.error("Polling error:", err));
        }, 1000);

        // 2. Handle form submission via POST to /send
        msgForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent page reload
            const msg = msgInput.value;
            
            fetch('/send', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'msg=' + encodeURIComponent(msg)
            }).then(() => {
                msgInput.value = ''; // Clear input box on success

            fetch('/log')
                .then(response => response.text())
                .then(data => {
                    // Only update if data changed to prevent annoying scroll jumps
                    if (logArea.textContent !== data) {
                        logArea.textContent = data;
                        logArea.scrollTop = logArea.scrollHeight; // Auto-scroll to bottom
                    }
                })
                .catch(err => console.error("Polling error:", err));
            }).catch(err => console.error("Send error:", err));

        });
    </script>
</body>
</html>
"""


class SimpleChatHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests for the HTML page and the log file."""
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))

        elif self.path == '/log':
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"")  # Return empty string if no logs yet

        else:
            self.send_error(404, "File not found")

    def do_POST(self):
        """Handle POST requests to append messages to the log."""
        if self.path == '/send':
            # Extract the POST payload
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')

            # Parse URL-encoded data (e.g., "msg=Hello%20World")
            parsed_data = urllib.parse.parse_qs(post_data)

            if 'msg' in parsed_data:
                message = parsed_data['msg'][0]
                # Append to the log file securely
                # with open(LOG_FILE, 'a') as f:
                #     f.write(message + '\n')
                send_message(message, (PI_ID+1) % 2)

            # Acknowledge receipt
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        """Silences the default logging to the console."""
        pass


print("starting server at ", MY_IP, "bluetooth adr - ", MY_BT_MAC)
threading.Thread(target=start_listener, args=(
    MY_BT_MAC, BT_PORT, socket.AF_BLUETOOTH)).start()
threading.Thread(target=start_listener, args=(
    MY_IP, WIFI_PORT, socket.AF_INET)).start()

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", HTTP_PORT), SimpleChatHandler) as httpd:
    print(f"[*] Server running on http://localhost:{HTTP_PORT}")
    print("[*] Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Server stopped.")
