from flask import Flask, render_template, send_from_directory
import socket
import os
import sys

# ==========================
if getattr(sys, "frozen", False):
	ROOT = os.path.dirname(sys.executable)
else :
	ROOT = os.path.dirname(os.path.abspath(__file__))
# ==========================

FILES_DIR = os.path.join(ROOT, "files")

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT, "templates"),
    static_folder=os.path.join(ROOT, "static")
)


@app.route("/")
def home():

    files = []

    for file in sorted(os.listdir(FILES_DIR)):

        path = os.path.join(FILES_DIR, file)

        if os.path.isfile(path):

            files.append({
                "name": file,
                "size": round(os.path.getsize(path)/1024,2)
            })

    return render_template(
        "index.html",
        files=files
    )


@app.route("/files/<path:filename>")
def download(filename):

    return send_from_directory(
        FILES_DIR,
        filename,
        as_attachment=True
    )


if __name__ == "__main__":

    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    if ip.startswith("127."):

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.connect(("8.8.8.8",80))
            ip = s.getsockname()[0]
        finally:
            s.close()

    print()
    print("="*40)
    print("Local Share Started")
    print("="*40)
    print(f"http://{ip}:8000")
    print("="*40)

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False
    )