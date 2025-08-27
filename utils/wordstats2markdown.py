import os 
import argparse
import json
import re
import yaml
from pathlib import Path
from datetime import datetime
from helpers import slugify


def to_md(data) -> str:
    ''' Build the Markdown text (front matter + trailing ---) for each author.'''
    author_slug = slugify(data['metadata']['author'])
    front_matter = {
        "layout" : "yazar",
        "title" : data['metadata']['author'] + " — En çok kullanılan kelimeler",
        "description" : data['metadata']['author'] + " eserlerinin kelime sıklığı grafiği.",
        "author" : data['metadata']['author'],
        "author_slug" : author_slug,
        "permalink" : "/yazar/" + author_slug + "-en-cok-kullanilan-kelimeler/",
        "lang" : "tr",
        "titles" : data['metadata']['titles']
        }
    
    yaml_text = yaml.safe_dump(
        front_matter,
        allow_unicode=True,
        sort_keys=False,
        width=10_000, # do not wrap long lines
    )
    
    return f"---\n{yaml_text}---"

def main() -> None:
    # Function argument parsing
    parser = argparse.ArgumentParser(description="Process author statistics and generate markdown")
    parser.add_argument("--input", required=True, help="Relative path to the author JSON statistic files")
    parser.add_argument("--output", required=True, help="Relative path the the markdown author pages")
    args = parser.parse_args()
    
    # Extract the relevant information from the JSON file
    all_files = os.listdir(Path(args.input))
    
    for fname in all_files:
        out_fname = re.sub(".json", "", fname) + "-en-cok-kullanilan-kelimeler" + ".md"

        # Open the input JSON file
        with open(Path(args.input, fname), "r", encoding="utf-8") as f:
            data = json.load(f)

        # Write the data into the output JSON file
        # Example:
        #
        # ---
        # layout: default
        # title: "Ahmet Ümit — En çok kullanılan kelimeler"
        # description: "Ahmet Ümit eserlerinin kelime sıklığı grafiği."
        # author: "Ahmet Ümit"
        # author_slug: "ahmet-umit"
        # permalink: "/yazar/ahmet-umit-top-kelimeler/"
        # lang: tr
        # titles:
        # - "Sultanı Öldürmek"
        # - "Agatha'nın Anahtarı"
        # - "Patasana"
        # - "Sis ve Gece"
        # - "Beyoğlu'nun En Güzel Abisi"
        # - "İstanbul Hatırası"
        # - "Kar Kokusu"
        # - "İnsan Ruhunun Haritası"
        # - "Beyoğlu Rapsodisi"
        # ---
        # {% include author-top-words.html author_slug=page.author_slug top_n=30 hide_stopwords=true %}

        #
        out_path = Path(args.output) / out_fname
        out_path.write_text(to_md(data))
        
        # Display the progress
        print(f"    ✔ Processed {out_fname}")

# Main function call
if __name__ == "__main__":
    main()