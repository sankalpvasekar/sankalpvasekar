import os
import subprocess
from datetime import datetime, timedelta

# S pixel map (7 rows x 5 cols)
# Each row = a day of week (row 0 = Sunday, row 6 = Saturday)
# Each col = a week
S = [
    "#####",  # row 0 = Sunday
    "#    ",  # row 1 = Monday
    "#    ",  # row 2 = Tuesday
    "#####",  # row 3 = Wednesday
    "    #",  # row 4 = Thursday
    "    #",  # row 5 = Friday
    "#####"   # row 6 = Saturday
]

# The grid starts at the Sunday of the week containing May 11, 2025
# May 11, 2025 is a Sunday, so grid_start = May 11, 2025
# We want S to start at column 0 (May 11, 2025)
GRID_START = datetime(2025, 5, 11)  # Sunday
S_START_COL = 0  # S starts right at grid_start (May 2025)
INTENSITY = 15   # commits per pixel for bright green

def patch_s():
    commits_count = 0
    env = os.environ.copy()

    print(f"Patching 'S' letter starting at column {S_START_COL} from {GRID_START.strftime('%Y-%m-%d')}...")

    for col_offset, row_data in enumerate(zip(*S)):
        col_idx = S_START_COL + col_offset
        for row_idx, pixel in enumerate(row_data):
            if pixel == "#":
                commit_date = GRID_START + timedelta(weeks=col_idx, days=row_idx)
                date_str = commit_date.strftime("%Y-%m-%d 12:00:00")

                env["GIT_AUTHOR_DATE"] = date_str
                env["GIT_COMMITTER_DATE"] = date_str

                for _ in range(INTENSITY):
                    subprocess.run(
                        ["git", "commit", "--allow-empty", "-m", "chore: contribution art", "--no-gpg-sign"],
                        env=env,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    commits_count += 1

        week_date = GRID_START + timedelta(weeks=col_idx)
        print(f"  Week of {week_date.strftime('%Y-%m-%d')} done.")

    print(f"\nSuccessfully created {commits_count} commits for 'S'.")
    print("Pushing to 'main' branch...")
    subprocess.run(["git", "push", "origin", "main"])
    print("Done!")

if __name__ == "__main__":
    patch_s()
