import argparse
import os
import re
import ebooklib
import json
# from turktoken import Tokenizer
from charTokenizer import Tokenizer
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

def slugify(text):
    # Mapping for Turkish -> English chars
    replacements = {
        "ç": "c",
        "ğ": "g",
        "ı": "i",
        "ö": "o",
        "ş": "s",
        "ü": "u",
    }
    
    text = text.lower()
    for tr, en in replacements.items():
        text = text.replace(tr, en)
    
    # remove apostrophes
    text = re.sub(r"['’]", '', text)
    # spaces -> dash
    text = re.sub(r"\s+", '-', text.strip())
    # keep only english letters, digits and dash
    text = re.sub(r"[^a-z0-9-]", '', text)
    
    return text

def main() -> None:

    # Parameter parsing
    parser = argparse.ArgumentParser(description='turktoken tokenizer')
    parser.add_argument("--input", required=True, help="relative path for the source")
    parser.add_argument("--output", required=True, help="relative path for the processed file")
    parser.add_argument("--mode", required=True, help="tokenization mode")
    args = parser.parse_args()
    
    # Process parameters
    input = Path(args.input)
    output = Path(args.output)
    mode = args.mode
    
    # Tokenizer object
    tokenizer = Tokenizer()
    
    # All authors
    authors_list = os.listdir(input)
    
    # -------------------------
    # Loop over ech author
    # -------------------------
    for yazar in authors_list:
        files_list = list(set(os.listdir(Path(input,yazar))))
        print(f"\t\n Processing...{yazar}")
        print("----------")
    
        # -------------------------
        # Loop over each file
        # -------------------------
        data = {}
        for dosya in files_list:
            try:
                book = epub.read_epub(Path(args.input, yazar, dosya))
            except:
                print(f"❌ - {dosya}")
                continue
        
            # Extract metadata from the file name
            procname = re.split('--', dosya, maxsplit=1)
            if len(procname) == 2:
                author = procname[0].strip()
                title = re.sub(r'.epub', '', procname[1]).strip()
            else:
                raise ValueError("Unkown file naming convention.")
            
            metadata = {
                "title": title,
                "author": author,
                "processed_at": datetime.now().isoformat(timespec="seconds")
            }
            
            # -------------------------
            # Iterate through the sections of the book
            # -------------------------
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse the HTML content
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text = soup.get_text()
                    
                    # Preprocess text
                    txt = tokenizer.preprocess_text(text)
                    
                    # Tokenize the text
                    data = tokenizer.analyze_text(txt, data)
                    
            # Record the processed data
            stats = {
                "metadata": metadata,
                "data": sorted(data.items(), key=lambda item:item[1], reverse=True)
            }
            
            # Progress
            print(f"\t✅ Processed - {title}")

        # Save JSON per author
        with open(Path(output, mode + "_" + slugify(yazar) + ".json"), 'w') as json_file:
            json.dump(stats, json_file, indent=4)


# Main function call
if __name__ == "__main__":
    main()