import os
import random
import subprocess
from datetime import datetime, timedelta

# -------------------- INPUT HELPERS -------------------- #

def ask_int(prompt, default):
    val = input(f"{prompt} (default {default}): ").strip()
    return int(val) if val.isdigit() else default

def ask_yes_no(prompt, default="n"):
    val = input(f"{prompt} (y/n, default {default}): ").strip().lower()
    return val if val in ["y", "n"] else default

# -------------------- DATE HELPERS -------------------- #

def is_weekend(date):
    return date.weekday() >= 5  # Sat = 5, Sun = 6

def random_time_on_day(day):
    return day + timedelta(
        hours=random.randint(9, 21),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

def get_random_day_previous_year(weekend_only=False):
    today = datetime.now()
    prev_year = today.year - 1

    start = datetime(prev_year, 1, 1)
    end = datetime(prev_year, 12, 31)
    total_days = (end - start).days

    while True:
        day = start + timedelta(days=random.randint(0, total_days))
        if not weekend_only or is_weekend(day):
            return day.replace(hour=0, minute=0, second=0)

# -------------------- COMMIT DATE GENERATORS -------------------- #

def generate_random_commits_prev_year(total, weekend_only):
    commits = []
    for _ in range(total):
        day = get_random_day_previous_year(weekend_only)
        commits.append(random_time_on_day(day))
    return commits

def generate_commits_one_day_prev_year(commits, weekend_only):
    day = get_random_day_previous_year(weekend_only)
    return [random_time_on_day(day) for _ in range(commits)]

# -------------------- GIT COMMIT LOGIC -------------------- #

def make_commit(repo, filename, date, message="graph-greener"):
    filepath = os.path.join(repo, filename)

    with open(filepath, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")

    subprocess.run(["git", "add", filename], cwd=repo)

    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo,
        env=env
    )

# -------------------- MAIN PROGRAM -------------------- #

def main():
    print("\n🌿 Graph-Greener — Previous Year Commit Generator 🌿\n")

    repo = input("Enter repo path (default current): ").strip() or "."
    filename = input("Filename to modify (default data.txt): ").strip() or "data.txt"

    weekend_only = ask_yes_no("Weekend-only commits?", "n") == "y"

    print("\nChoose Commit Mode:")
    print("1 → Random commits across ENTIRE previous year")
    print("2 → MANY commits in ONE single day (previous year)")

    mode = input("Enter mode (1/2): ").strip()

    if mode == "2":
        commits_per_day = ask_int("How many commits in that ONE day", 10)
        commit_dates = generate_commits_one_day_prev_year(
            commits_per_day,
            weekend_only
        )
    else:
        total_commits = ask_int("Total commits across previous year", 200)
        commit_dates = generate_random_commits_prev_year(
            total_commits,
            weekend_only
        )

    print(f"\nCreating {len(commit_dates)} commits...\n")

    for i, date in enumerate(commit_dates, 1):
        print(f"[{i}/{len(commit_dates)}] Commit at {date}")
        make_commit(repo, filename, date)

    print("\n🚀 Pushing commits to GitHub...")
    subprocess.run(["git", "push"], cwd=repo)

    print("\n✅ DONE!")
    print("⏳ GitHub graph will update in a few minutes.\n")

# -------------------- RUN -------------------- #

if __name__ == "__main__":
    main()
