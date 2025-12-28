import os
import random
import subprocess
from datetime import datetime, timedelta

# ---------------- Utility Functions ---------------- #

def ask_int(prompt, default):
    val = input(f"{prompt} (default {default}): ").strip()
    return int(val) if val.isdigit() else default

def ask_yes_no(prompt, default="n"):
    val = input(f"{prompt} (y/n, default {default}): ").strip().lower()
    return val if val in ["y", "n"] else default

def random_time_on_day(day):
    return day + timedelta(
        hours=random.randint(9, 21),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

def is_weekend(date):
    return date.weekday() >= 5  # 5 = Sat, 6 = Sun

# ---------------- Date Generators ---------------- #

def get_random_day(last_n_days, weekend_only=False):
    today = datetime.now()
    start = today - timedelta(days=last_n_days)

    while True:
        day = start + timedelta(days=random.randint(0, last_n_days))
        if not weekend_only or is_weekend(day):
            return day.replace(hour=0, minute=0, second=0)

def generate_commits_one_day(commits, last_n_days, weekend_only):
    day = get_random_day(last_n_days, weekend_only)
    return [random_time_on_day(day) for _ in range(commits)]

def generate_random_commits(total, last_n_days, weekend_only):
    commits = []
    for _ in range(total):
        day = get_random_day(last_n_days, weekend_only)
        commits.append(random_time_on_day(day))
    return commits

# ---------------- Git Commit Logic ---------------- #

def make_commit(repo, filename, date, msg="graph-greener"):
    path = os.path.join(repo, filename)
    with open(path, "a") as f:
        f.write(f"Commit at {date.isoformat()}\n")

    subprocess.run(["git", "add", filename], cwd=repo)

    env = os.environ.copy()
    date_str = date.strftime("%Y-%m-%dT%H:%M:%S")
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=repo,
        env=env
    )

# ---------------- Main Program ---------------- #

def main():
    print("\n🌱 GitHub Contribution Graph Generator 🌱\n")

    repo = input("Enter repo path (default current): ").strip() or "."
    filename = input("Filename to modify (default data1.txt): ").strip() or "data1.txt"

    weekend_only = ask_yes_no("Weekend only commits?", "n") == "y"

    print("\nChoose Mode:")
    print("1 → Random commits over days")
    print("2 → MANY commits in ONE single day")

    mode = input("Enter mode (1/2): ").strip()

    last_n_days = ask_int("Consider commits within how many days", 20)

    if mode == "2":
        commits_per_day = ask_int("How many commits in that ONE day", 10)
        commit_dates = generate_commits_one_day(
            commits_per_day,
            last_n_days,
            weekend_only
        )
    else:
        total_commits = ask_int("Total number of commits", 20)
        commit_dates = generate_random_commits(
            total_commits,
            last_n_days,
            weekend_only
        )

    print(f"\nCreating {len(commit_dates)} commits...\n")

    for i, date in enumerate(commit_dates, 1):
        print(f"[{i}] Commit at {date}")
        make_commit(repo, filename, date)

    print("\n🚀 Pushing to remote...")
    subprocess.run(["git", "push"], cwd=repo)

    print("\n✅ DONE! Check GitHub graph in few minutes.\n")

# ---------------- Run ---------------- #

if __name__ == "__main__":
    main()
