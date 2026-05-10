import os
import subprocess
from datetime import datetime, timedelta

# Improved 7x5 pixel maps
# Row 0: Sunday, Row 6: Saturday
S = [
    "#####",
    "#    ",
    "#    ",
    "#####",
    "    #",
    "    #",
    "#####"
]
A = [
    " ### ",
    "#   #",
    "#   #",
    "#####",
    "#   #",
    "#   #",
    "#   #"
]
N = [
    "#   #",
    "##  #",
    "# # #",
    "#  ##",
    "#   #",
    "#   #",
    "#   #"
]
K = [
    "#   #",
    "#  # ",
    "# #  ",
    "##   ",
    "# #  ",
    "#  # ",
    "#   #"
]
L = [
    "#    ",
    "#    ",
    "#    ",
    "#    ",
    "#    ",
    "#    ",
    "#####"
]
P = [
    "#####",
    "#   #",
    "#   #",
    "#####",
    "#    ",
    "#    ",
    "#    "
]

def combine_letters(letters):
    grid = [""] * 7
    for letter in letters:
        for i in range(7):
            grid[i] += letter[i] + " " # Add space between letters
    return grid

grid = combine_letters([S, A, N, K, A, L, P])

def generate_art():
    today = datetime.now()
    days_to_sunday = (today.weekday() + 1) % 7
    recent_sunday = today - timedelta(days=days_to_sunday)
    grid_start = recent_sunday - timedelta(weeks=52)
    
    start_col = 5
    intensity = 15 # High intensity for bright green
    
    print(f"Generating high-intensity art starting from {grid_start.strftime('%Y-%m-%d')}...")
    
    commits_count = 0
    for col_idx, col_data in enumerate(zip(*grid)):
        if col_idx < start_col:
            continue
            
        for row_idx, pixel in enumerate(col_data):
            if pixel == "#":
                commit_date = grid_start + timedelta(weeks=col_idx, days=row_idx)
                date_str = commit_date.strftime("%Y-%m-%d 12:00:00")
                
                env = os.environ.copy()
                env["GIT_AUTHOR_DATE"] = date_str
                env["GIT_COMMITTER_DATE"] = date_str
                
                # Make multiple commits per day for intensity
                for _ in range(intensity):
                    subprocess.run(
                        ["git", "commit", "--allow-empty", "-m", "chore: contribution art", "--no-gpg-sign"],
                        env=env,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    commits_count += 1
                    
        # Log progress every few columns
        if col_idx % 5 == 0:
            print(f"Progress: Column {col_idx}, total commits: {commits_count}")
    
    print(f"Successfully created {commits_count} commits.")
    print("Pushing directly to 'main' branch...")
    subprocess.run(["git", "push", "origin", "main", "--force"])

if __name__ == "__main__":
    generate_art()
