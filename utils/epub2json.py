import os
import re
import argparse
import ebooklib
import json

from helpers import slugify
from ebooklib import epub
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime

def remove_all_punct(text):
        
    # Punctionation rules
    punct_pattern = r"[.,!?;:\"“”‘’«»()\[\]{}…—–\-–_/\%&*@#^+=<>\\'\u00AD]"
    text = re.sub(punct_pattern, " ", text)
    
    # Suffixes (In future releases)
    # This portion will remove the suffixes which don't provide much information
    # about the book for instance, "de", "da" in Turkish
    # 
    # suffix_pattern = r"\s(?:de|da)\s"
    # text = re.sub(suffix_pattern, " ", text)
    
    # Normalze spaces and lowercase characters
    text = re.sub(r"\s+", " ", text.lower()).strip()
    return text

def calculate_word_stats(chapters):
    vocab = {}
    for c in chapters:
        for word in c.split():
            if word in vocab:
                vocab[word] += 1
            else:
                vocab[word] = 1

    # Sort the word frequencies in descending order and save
    word_freq = dict(sorted(vocab.items(), key=lambda item: item[1], reverse=True))    
    return word_freq


def main() -> None:
    parser = argparse.ArgumentParser(description="Read EPUB content")
    parser.add_argument("--input", required=True, help="EPUB file path containing the book")
    parser.add_argument("--output", required=True, help="Processed file path")
    args = parser.parse_args()

    # Loop over the folders in the target folder
    authors = os.listdir(Path(args.input))
    
    total_freq = {}
    for i, yazar in enumerate(authors):
        print(f"({100*i/len(authors):.3f}%) : {yazar}")
        books = os.listdir(Path(args.input).joinpath(yazar))
        
        # -------------------------
        # Process each book
        # -------------------------
        for kitap in books:
            metadata = {}
            book = epub.read_epub(Path(args.input).joinpath(yazar).joinpath(kitap))

            # -------------------------
            # Iterate through the sections of the book
            # -------------------------
            id = 0
            chapters = []
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse HTML content
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    text = soup.get_text()

                    # Process extracted text to remove punctuations
                    clean_text = remove_all_punct(text)
                
                    # Record the results
                    chapters.append(clean_text)
                        
                    # Increase the section index
                    id += 1
            
            # -------------------------
            # Process each chapter to calculate word statistics
            # -------------------------
            baslik = re.split("--",re.sub(".epub","",kitap))[-1].strip()
            book_id = f"{slugify(yazar)}--{slugify(baslik)}"

            # Check if the book exists in the dictionary
            if book_id in total_freq.keys():
                raise Exception("Repetition of the author-book combination in the data.")
            else:
                total_freq[book_id] = calculate_word_stats(chapters)
                print(f"    ✔ Processed {kitap}")
            
            # Create a JSON file to record the word frequencies
            tokens = total_freq[book_id].keys()
            freq = total_freq[book_id].values()
            
            # Zip into dictionary
            data = dict(zip(tokens, freq))
            
            # Metadata
            metadata = {
                "title": baslik,
                "author": yazar,
                "processed_at": datetime.now().isoformat(timespec="seconds")
            }
            
            # Lump the metadata into the statistics
            book_data = {
                "metadata": metadata,
                "token_stats": data
            }
            
            # Save as JSON
            with open(Path(args.output,book_id+'.json'), "w+", encoding="utf-8") as f:
                json.dump(book_data, f, ensure_ascii=False, indent=2)

# Main function call
if __name__ == "__main__":
    main()