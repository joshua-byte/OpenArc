#!/usr/bin/env python3
import os
import json
import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# ==========================
# CONFIG
# ==========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
DATA_FILE = os.path.join(BASE_DIR, "data.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

# ==========================
# UTILS
# ==========================

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def generate_fake_doi(existing_preprints):
    """
    Generates a realistic fake DOI.
    Example: 10.55555/openarc.202502-0001
    """
    prefix = "10.55555/openarc"
    now = datetime.datetime.utcnow()
    date_label = f"{now.year}{now.month:02d}"

    month_entries = [
        p for p in existing_preprints
        if p.get("doi", "").startswith(f"{prefix}.{date_label}")
    ]
    seq = f"{len(month_entries) + 1:04d}"

    return f"{prefix}.{date_label}-{seq}"

# ==========================
# ROUTES
# ==========================

@app.route("/api/preprints/", methods=["GET"])
def list_preprints():
    data = load_data()
    return jsonify(data), 200


@app.route("/api/preprints/<int:pid>/", methods=["GET"])
def get_preprint(pid):
    data = load_data()
    for p in data:
        if p["id"] == pid:
            return jsonify(p), 200
    return jsonify({"error": "Not found"}), 404


@app.route("/api/preprints/", methods=["POST"])
def upload_preprint():
    data = load_data()

    title = request.form.get("title", "").strip()
    abstract = request.form.get("abstract", "").strip()
    category = request.form.get("category", "uncategorized")
    mint_doi = request.form.get("mint_doi")

    file = request.files.get("pdf_file")

    if not title or not abstract or not file:
        return jsonify({"error": "Missing required fields"}), 400

    # Save PDF
    ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    safe_name = f"{ts}_{file.filename.replace(' ', '_')}"
    save_path = os.path.join(UPLOAD_DIR, safe_name)
    file.save(save_path)

    # Create record
    new_id = (data[-1]["id"] + 1) if data else 1

    record = {
        "id": new_id,
        "title": title,
        "abstract": abstract,
        "category": category,
        "version": 1,
        "uploaded_at": datetime.datetime.utcnow().isoformat(),
        "pdf_file": f"http://{request.host}/api/files/{safe_name}",
        "doi": None
    }

    # Mint a fake DOI if requested
    if mint_doi == "true":
        record["doi"] = generate_fake_doi(data)

    data.append(record)
    save_data(data)

    return jsonify(record), 201


@app.route("/api/preprints/<int:pid>/mint/", methods=["POST"])
def mint_doi(pid):
    data = load_data()
    for p in data:
        if p["id"] == pid:
            if p.get("doi"):
                return jsonify({"doi": p["doi"]}), 200

            fake = generate_fake_doi(data)
            p["doi"] = fake
            save_data(data)
            return jsonify({"doi": fake}), 201

    return jsonify({"error": "Not found"}), 404


@app.route("/api/files/<path:filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


# ==========================
# LAUNCH
# ==========================
if __name__ == "__main__":
    print("Running OpenArc backend on http://localhost:5001")
    app.run(host="0.0.0.0", port=5001, debug=True)
