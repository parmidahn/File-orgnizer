from flask import Flask, render_template, request, jsonify
import os
import datetime

app = Flask(__name__)

def copypaste(src_file, dst_file):
    with open(src_file, "rb") as f_src, open(dst_file, "wb") as f_dst:
        while True:
            chunk = f_src.read(1024)
            if not chunk:
                break
            f_dst.write(chunk)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/organize', methods=['POST'])
def organize():
    data = request.get_json()
    src = data['src']
    dst = data['dst']
    images = ["jpg", "jpeg", "png"]

    if not os.path.exists(src) or not os.path.exists(dst):
        return jsonify({"message": "Invalid path."})

    try:
        for root, dirs, files in os.walk(src):
            for name in files:
                if name.lower().endswith(tuple(images)):
                    file_path = os.path.join(root, name)
                    modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                    year = modification_date.strftime("%Y")
                    year_folder = os.path.join(dst, year, "photos")
                    os.makedirs(year_folder, exist_ok=True)
                    dst_file_path = os.path.join(year_folder, name)
                    copypaste(file_path, dst_file_path)
        return jsonify({"message": "✅ Done organizing photos by year!"})
    except Exception as e:
        return jsonify({"message": f"❌ Error: {e}"})

if __name__ == '__main__':
    app.run(debug=True)
