# 🔍 GitLab Project Size Analyzer

A simple Python tool to analyze storage usage of all projects on a self-hosted GitLab instance — including repository size, LFS objects, CI artifacts, and wiki size.

---

## 🚀 Features

- Lists all GitLab projects sorted by total storage usage
- Optionally displays detailed breakdowns (repo, LFS, artifacts, wiki)
- Exports results to CSV file
- Warns for projects larger than 2 GB
- Supports HTTPS with self-signed certificates

---

## 🛠️ Requirements

- Python 3.6+
- Modules:
  - `requests`

Install (Debian/Ubuntu):
```bash
sudo apt install python3 python3-pip
pip3 install requests
```

---

## 🔐 GitLab Access Token

To access the GitLab API, you need a **Personal Access Token** with the following scope:

- ✅ `api`

How to create one:
1. Go to GitLab → Profile → Access Tokens
2. Set a name, enable the `api` scope
3. Save the token and paste it into the script:
   ```python
   PRIVATE_TOKEN = "glpat-..."
   ```

---

## ⚙️ Configuration

Edit the following values in `gitlab_project_sizes.py`:

```python
GITLAB_URL = "https://gitlab.your-domain.com"
PRIVATE_TOKEN = "YOUR_ACCESS_TOKEN"
```

> For self-signed certificates, `verify=False` is already set in the code.

---

## ▶️ Usage

```bash
python3 gitlab_project_sizes.py
```

The script will ask:
- if you want to see detailed statistics
- if you want to export the results to a CSV file

---

## 📁 Output

Terminal example:

```
📁 Top 20 Projects by Storage Usage:
   1.5 GB  Gerald / Website
  38.3 MB  Gerald / cryptopricetracker
   ...
```

CSV output:
```
gitlab_project_sizes.csv
```

---

## 📎 Example CSV Output

| Project | Total | Repository | LFS | Artifacts | Wiki |
|---------|-------|------------|-----|-----------|------|
| Gerald / ProjectX | 1.5 GB | 1.3 GB | 200 MB | 0 B | 0 B |

---

## 📜 License

MIT License — free to use, modify, and redistribute.

---

## 🙌 Author

Gerald Hasani  
[https://github.com/Gerald-Ha](https://github.com/Gerald-Ha)

---
