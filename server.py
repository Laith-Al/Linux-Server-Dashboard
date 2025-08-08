# Made by Laith Al, Visit https://github.com/Laith-Al For More Projects
from flask import Flask, jsonify, send_file, abort, make_response
import psutil
import socket
import time
import os

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    try:
        return send_file("data/404.html"), 404
    except FileNotFoundError:
        return make_response("<h1>404 Not Found</h1><p>Please re-install software!</p>", 404)

@app.route("/favicon.ico")
def favicon():
    return send_file("data/favicon.ico")

@app.route("/")
def index():
    try:
        return send_file("index.html")
    except FileNotFoundError:
        abort(404, description="Dashboard HTML not found, Please Re-Install!")

@app.route("/stats")
def stats():
    try:
        cpu = psutil.cpu_percent(interval=0.5)
        ram = psutil.virtual_memory().percent
        uptime = int(time.time() - psutil.boot_time())
        hostname = socket.gethostname()
        try:
            ip_address = socket.gethostbyname(hostname)
            if ip_address.startswith("127."):
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.connect(("8.8.8.8", 80))
                    ip_address = s.getsockname()[0]
        except Exception:
            ip_address = "Unknown"

        cpu_temp = None
        temp_paths = [
            "/sys/class/thermal/thermal_zone0/temp",
            "/sys/devices/virtual/thermal/thermal_zone0/temp"
        ]
        for path in temp_paths:
            if os.path.isfile(path):
                try:
                    with open(path, "r") as f:
                        temp_raw = f.readline()
                        cpu_temp = round(int(temp_raw) / 1000.0, 1)
                        break
                except Exception:
                    cpu_temp = None

        return jsonify({
            "cpu": cpu,
            "ram": ram,
            "uptime": uptime,
            "hostname": hostname,
            "ip": ip_address,
            "cputemp": cpu_temp
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=49200)
    except Exception as e:
        print(f"Failed to start server: {e}")
#Thank you for using Linux Server Dashboard