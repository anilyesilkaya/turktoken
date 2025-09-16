class Tokenizer:
    # Constructor
    def __init__(self, mode="char"):
        self.mode = mode
        if self.mode == "char":
            return 0
        elif self.mode == "word":
            return 0
        elif self.mode == "bpe":
            return 0
        else:
            raise ValueError(f"Invalid tokenization mode: '{self.mode}'. \
                            Supported modes are 'char', 'word', and 'bpe'.")

    def encode(self, txt: str):
        return [0, 0, 0]
    
    def decode(self, tokens):
        return "hello world"