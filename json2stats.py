import os
import argparse
import re
import json
from pathlib import Path

def main() -> None:
    # Function argument parsing
    parser = argparse.ArgumentParser(description="Post processing of the book JSON data")
    parser.add_argument("--input", required=True, help="Relative path for the JSON book files")
    parser.add_argument("--output", required=True, help="Author level statistics")
    args = parser.parse_args()

    # -------------------------    
    # Loop over the files to list them
    # -------------------------
    books = os.listdir(Path(args.input))
    authors = set([re.split("--", book)[0] for book in books])
    all_data = []

    for yazar in authors:
        books_per_auth = [f for f in os.listdir(Path(args.input)) if f.startswith(yazar + "--")]
        auth_stats = {}
        auth_titles = []
        
        for kitap in books_per_auth:
        
            # Read the JSON file
            all_data = []
            with open(Path(args.input, kitap), "r", encoding="utf-8") as f:
                data = json.load(f)
                all_data.append(data)
        
            # -------------------------
            # Process data (Token statistics per author and book)
            # -------------------------
            author = all_data[0]['metadata']['author']
            title = all_data[0]['metadata']['title']
            stats = all_data[0]['token_stats']
            auth_titles.append(title)

            # Token frequencies per author
            for token in stats.keys():
                if token in auth_stats.keys():
                    auth_stats[token] += stats[token]
                else:
                    auth_stats[token] = stats[token]
                        
        # Save the final data in a JSON file
        metadata = {
            "author": author,
            "titles" : auth_titles
        }
        
        # auth_stats is sorted to be in descending order
        data = {
            "metadata": metadata,
            "total_stats": dict(sorted(auth_stats.items(), key=lambda item: item[1], reverse=True))
        }
        
        # Save as JSON
        with open(Path(args.output, yazar + '.json'), "w+", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        # Print status
        print(f"    ✔ Processed {author}")

# Main function call
if __name__ == "__main__":
    main()
    
