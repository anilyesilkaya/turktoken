import re

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