# 🚀 **OpenArc — Minimal Preprint Server**

OpenArc is a lightweight preprint server that lets you upload PDFs, search papers, and generate fake DOIs — all with a tiny Flask backend and a single-file frontend.

---

## ✨ Features

- 📄 PDF uploads  
- 🔍 Search + categories  
- 🔖 Auto-generated fake DOIs  
- 🗂 JSON storage (no database)  
- 🎨 Clean, modern UI  
- ⚡ Runs locally, no dependencies

---

## 🛠 Quick Start

### Backend

```bash
pip install flask flask-cors
python3 server.py
```

Runs at:

```
http://localhost:5001
```

### Frontend

Open:

```
index.html
```

---

## 🔗 API (Simple)

- **GET** `/api/preprints/` — list preprints  
- **POST** `/api/preprints/` — upload  
- **GET** `/api/preprints/<id>/` — get one  
- **POST** `/api/preprints/<id>/mint/` — create fake DOI  

---

## 🧪 DOI Format

```
10.55555/openarc.YYYYMM-####
```

---

## 📂 Structure

```
openarc/
  index.html
  server.py
  data.json
  uploads/
```

---

## 📜 License

MIT License.
