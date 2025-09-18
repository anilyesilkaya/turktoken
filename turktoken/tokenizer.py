import re
import unicodedata

class Tokenizer:
    """
    Simple tokenizer supporting 'char' and 'word' modes.
    'bpe' kept as a placeholder.
    """
    SUPPORTED_MODES = {"char", "word", "bpe"}
    
    # Constructor
    def __init__(self, mode="char", train=False):
        self.mode = mode.lower()
        self.train = train
        if self.mode in self.SUPPORTED_MODES:
            self.mode = mode
        else:
            raise ValueError(f"Invalid tokenization mode: '{self.mode}'. \
                            Supported modes are 'char', 'word', and 'bpe'.")

    # Methods    
    def encode(self, text: str):
        return [0, 0, 0]
    
    def decode(self, tokens):
        return "hello world"

    def increment_dict_value(self, d, k):
        if k in d.keys():
            d[k] += 1
        else:
            d[k] = 1
        return d
    
    def preprocess(self, text: str = []):
        # Unicode normalization (important for composed/decomposed chars)
        text = unicodedata.normalize("NFC", text)

        # Normalize newlines: Windows (\r\n), old Mac (\r) → Unix (\n)
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Collapse multiple whitespace into a single space
        text_clean = re.sub(r"[ \t]+", " ", text)

        return text_clean

    def analyze_char(self, text: str =[], chars: dict = {}, case_sensitive=False, include_space=False):        
        txt = text
        
        # Text preprocessing
        txt = self.preprocess(txt)

        # Lowercase
        if not case_sensitive:
            txt = txt.lower()

        # Processing loop
        proc = re.findall(r".", txt)
        for c in proc:
            if c != ' ' or c == ' ' and include_space:
                chars = self.increment_dict_value(chars, c)
        return chars
    
    def analyze_word(self, text: str = [], words: dict = {}, case_sensitive=False):
        # World-level text analysis        
        text = re.findall(r"\S+", text)
        
        if not case_sensitive:
            text = text.lower()
        
        for w in text:
            words = self.increment_dict_value(words, w)
        return words