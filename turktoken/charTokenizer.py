import unicodedata
import re

class Tokenizer:
    """
    Simple character-level tokenizer with:
        - Unicode normalization (NFC by default)
        - Newline normalization: \r\n, \r -> \n
        - NBSP -> space
        - Optional lowercasing
        - Collapse runs of spaces/tabs (keeps newlines)
        - Special tokens: <PAD>, <UNK>, <BOS>, <EOS>
            -- <PAD>: Padding
            -- <UNK>: Unknown
            -- <BOS>: Beginning of a sequence
            -- <EOS>: End of a sequence
    """
    DEFAULT_SPECIALS = ["<PAD>", "<UNK>", "<BOS>", "<EOS>"]
    
    # Constructor
    def __init__(self, max_length=64):
        self.max_length = max_length
    
    # Methods
    def preprocess_text(self, text:str = []):
        """
        Preprocesses text for character-level tokenization.
        
        Performs the following operations:
            - Unicode normalization (NFC format)
            - Newline normalization (converts \r\n and \r to \n)
            - Collapses multiple spaces and tabs into a single space
        """
        # Unicode normalization (important for composed/decomposed chars)
        text = unicodedata.normalize("NFC", text)

        # Normalize newlines: Windows (\r\n), old Mac (\r) → Unix (\n)
        text = text.replace("\r\n", " ").replace("\r", "\n")
        text = text.replace("\n", " ")

        # Collapse multiple whitespace into a single space
        text = re.sub(r"\n{2,}|\xa0{2,}|\s{2,}"," ", text).strip()

        return text
        
    def add_token(self, dic:dict = {}, k:str = []):
        if k in dic.keys():
            dic[k] += 1
        else:
            dic[k] = 1

        return dic
    
    def analyze_text(self, text:str = [], data:dict = {}, case_sensitive=False):
        """
        Tokenize the text
        """
        
        # Preprocessing
        TOKEN_PATTERN = re.compile(r'''
                                \u2026|\.{3}            # ellipsis (… or '...')
                            | —                       # em dash
                            | ’                       # curly apostrophe
                            | [-=_~\[\]/\\¬]          # single-character symbols
                            | [.!?,;:()\[\]{}'"“”‘’]  # other punctuation (includes " and ')
                            | [^\s.!?,;:()\[\]{}'"]+  # everything else (words, numbers, etc.)
                            ''', re.VERBOSE)

        if not case_sensitive:
            text = text.lower()
        
        proc_text = re.findall(TOKEN_PATTERN, text)
        
        # Tokenization
        for item in proc_text:
            if len(item) > 1:                
                for c in item:
                    data = self.add_token(data, c)
            else:
                data = self.add_token(data, item)

        return data