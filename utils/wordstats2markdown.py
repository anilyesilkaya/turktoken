import os 
import argparse
from pathlib import Path

def main() -> None:
    # Function argument parsing
    parser = argparse.ArgumentParser(description="Process author statistics and generate markdown")
    parser.add_argument("--input", required=True, help="Relative path to the author JSON statistic files")
    parser.add_argument("--output", required=True, help="Relative path the the markdown author pages")
    args = parser.parse_args()
    
    # Extract the relevant information from the JSON file
    os.listdir(Path(args.input))
    
    
    # ---
    # layout: default
    # title: "Alev Alatlı — En çok kullanılan kelimeler"
    # description: "Alev Alatlı eserlerinden kelime sıklığı grafiği."
    # author_slug: alev-alatli
    # ---
    # {% include author-top-words.html author_slug=page.author_slug top_n=30 hide_stopwords=true %}


# Main function call
if __name__ == "__main__":
    main()