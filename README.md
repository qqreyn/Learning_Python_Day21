# 📰 News Automation Tool

A beginner-friendly Python automation project that fetches live news,
cleans and analyzes the data, generates a report, and saves everything
to disk — with optional scheduling.

---

## 📁 Project Structure

```
news_automation/
├── main.py            ← main script (all the logic lives here)
├── scheduler.py       ← optional: run automatically on a timer
├── requirements.txt   ← libraries this project needs
├── README.md          ← you are here
│
│   (these are created when you run main.py)
├── raw_data.json      ← full raw API response saved here
├── history.csv        ← one row added per run (your historical log)
├── report.txt         ← the generated report saved here
└── automation.log     ← log of every run (errors, info, timestamps)
```

---

## 🚀 Setup (do this once)

**1. Get a free API key**
- Go to https://newsapi.org/register
- Sign up (free) and copy your API key

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key to main.py**
Open `main.py` and replace line:
```python
API_KEY = "YOUR_API_KEY_HERE"
```
with your actual key:
```python
API_KEY = "abc123yourkeyhere"
```

**4. Run it!**
```bash
python main.py
```

---

## ⚙️ Configuration

At the top of `main.py` you can change:

| Variable        | Default        | What it does                         |
|----------------|----------------|--------------------------------------|
| `TOPIC`         | `"technology"` | News topic to search for             |
| `MAX_ARTICLES`  | `10`           | How many articles to fetch           |
| `REPORT_FILE`   | `"report.txt"` | Where the report is saved            |
| `HISTORY_FILE`  | `"history.csv"`| Where the run history is saved       |

---

## 🗓️ Optional Scheduling

To run the tool automatically every hour:
```bash
python scheduler.py
```
Edit `scheduler.py` to change the interval. Press `Ctrl+C` to stop.

---

## 🧪 What to Experiment With (Beginner Tips)

- Change `TOPIC` to `"sports"`, `"science"`, or `"bitcoin"` and re-run
- Run `main.py` 3 times, then open `history.csv` — see how it grows
- Open `raw_data.json` and compare it to the cleaned data in the report
- Open `automation.log` to see a timestamped record of every run
- Comment out a step in `main()` and see what breaks and why

---

## 📦 How It Works (Step by Step)

```
1. fetch_news()       → calls NewsAPI, gets raw JSON
2. clean_articles()   → removes junk, fills in missing fields
3. analyze_articles() → counts sources, finds top source
4. generate_report()  → formats everything, prints + saves to .txt
5. save_raw_data()    → saves full API response to raw_data.json
6. append_to_history()→ adds one summary row to history.csv
```

Each step is its own function — read them one at a time!
