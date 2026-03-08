"""
scheduler.py — Optional: Run main.py automatically on a schedule
================================================================
This uses the `schedule` library to run your automation tool
every X minutes/hours without you having to do anything.

Install first:  pip install schedule
Then run:       python scheduler.py
Stop it:        Ctrl + C

🧪 Experiment:
  - Change schedule.every(1).hours  →  schedule.every(30).minutes
  - Add schedule.every().day.at("09:00").do(job)  to run at 9am daily
  - Add a print that counts how many times it has run
"""

import schedule
import time
import logging
from main import main     # imports the main() function from main.py

logger = logging.getLogger(__name__)


def job():
    """The task that runs on every scheduled tick."""
    print("\n⏰ Scheduler triggered — running automation tool...\n")
    main()


# ── Set your schedule here ──────────────────
schedule.every(1).hours.do(job)          # run every 1 hour
# schedule.every(30).minutes.do(job)     # ← uncomment to run every 30 min
# schedule.every().day.at("09:00").do(job)  # ← uncomment to run at 9am daily


if __name__ == "__main__":
    print("🗓️  Scheduler started. Press Ctrl+C to stop.")
    print(f"   Next run at: {schedule.next_run()}\n")

    job()   # run once immediately on start

    while True:
        schedule.run_pending()
        time.sleep(60)    # check every 60 seconds
