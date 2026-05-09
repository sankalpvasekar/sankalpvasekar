import argparse
import os
import re
from datetime import datetime
import asciichartpy
import berserk

HSIZE = 60

def _result_from_ascii(ratings):
    config = {"height": 9, "format": "{:8.0f}"}
    return asciichartpy.plot(ratings, config)

class LichessChartGenerator:
    def __init__(self, rating_type):
        self.rating_type = rating_type
        api_token = os.environ.get("LICHESS_TOKEN")
        if not api_token:
            raise KeyError("LICHESS_TOKEN environment variable not found")
        session = berserk.TokenSession(api_token)
        self.client = berserk.Client(session=session)

    def get_ratings(self):
        user_info = self.client.account.get()
        user_id = user_info["id"]
        rating_history = self.client.users.get_rating_history(user_id)
        
        # Find the specific rating type
        data = next((d for d in rating_history if d["name"] == self.rating_type), None)
        if not data:
            raise ValueError(f"Rating type {self.rating_type} not found in history")
            
        ratings = [row[3] for row in data["points"]]
        if not ratings:
            raise ValueError("No rating points found")

        if len(ratings) >= HSIZE:
            step = int(len(ratings) / HSIZE)
            ratings = ratings[0 : len(ratings) : step]
        
        return user_id, ratings

    def generate_output(self, user_id, ratings_ascii):
        header = r"""
          _      _      _
         | |    (_)    | |
         | |     _  ___| |__   ___  ___ ___
         | |    | |/ __| '_ \ / _ \/ __/ __|
         | |____| | (__| | | |  __/\__ \__ \
         |______|_|\___|_| |_|\___||___/___/
"""
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        footer = f"\nUser: {user_id}, Rating type: {self.rating_type} on lichess.org\nLast update: {now}"
        return f"{header}\n{ratings_ascii}\n{footer}"

def update_readme(new_content):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    pattern = r"(<!-- LICHESS_START -->).*?(<!-- LICHESS_END -->)"
    replacement = f"\\1\n<pre><code>\n{new_content}\n</code></pre>\n\\2"
    
    new_readme = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rating_type", default="Bullet")
    args = parser.parse_args()
    
    try:
        gen = LichessChartGenerator(args.rating_type)
        uid, ratings = gen.get_ratings()
        ascii_graph = _result_from_ascii(ratings)
        output = gen.generate_output(uid, ascii_graph)
        update_readme(output)
        print("Successfully updated README with Lichess stats")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
