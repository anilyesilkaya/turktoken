import unicodedata
import re
import regex

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
            -- <SPC>: Space
    """
    DEFAULT_SPECIALS = ["<PAD>", "<UNK>", "<BOS>", "<EOS>", "<SPC>"]
    
    # Constructor
    def __init__(self, max_length=64):
        self.max_length = max_length
    
    # Methods
    def normalize_text(self, text:str =[]):
        # Turkish text normalization
        # text = text.replace("İ", "i").replace("I", "ı").
        return text.lower()
    
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
        \u0131 → ı (dotless i, small i without dot)
        \u00fc → ü (u with diaeresis)
        \u011f → ğ (g with breve)
        \u015f → ş (s with cedilla)
        \u00e7 → ç (c with cedilla)
        \u00f6 → ö (o with diaeresis)
        \u0307 → ◌̇ (combining dot above – often appears in Turkish text normalization 
                        when separating i into ı + ̇)
        """
        
        # Preprocessing
        # Lower-case with Turkish i's in mind
        if not case_sensitive:
            text = self.normalize_text(text)

        proc_text = regex.findall(r"\X", text)
        
        # Tokenization
        for item in proc_text:
            if len(item) > 1:          
                for c in item:
                    data = self.add_token(data, c)
            else:
                if item == " ":
                    data = self.add_token(data, "<SPC>")
                else:
                    data = self.add_token(data, item)

        return data