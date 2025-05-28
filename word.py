from datetime import date
import csv
import re

class Word:
    WORDS_CSV = "words.csv"

    def __init__(self, word, added=None, learned=None):
        if isinstance(word, dict):
            keys = list(word.keys())
            if "added" in keys:
                added = word["added"]
            if "learned" in keys:
                learned = word["learned"]
            if "word" in keys:
                word = word["word"]
            else:
                word = word[keys[0]]
        self.word = word
        self.added = added
        self.learned = learned

    def __str__(self):
        return self.word
    
    def dictionary(self) -> dict:
        return {
            "word": self.word,
            "added": self.added.isoformat() if self.added else None,
            "learned": self.learned.isoformat() if self.learned else None
        }
    
    def learn(self) -> 'Word':
        if not self.is_known:
            self.learned = date.today()
        return self

    def forget(self) -> 'Word':
        if self.is_known:
            self.learned = None
            self.added = date.today()
        return self
    
    @property
    def word(self):
        return self._word
    @word.setter
    def word(self, word):
        word = Word.sanitize(word)
        if word.strip() == "":
            raise ValueError("Word must be a non-empty string")
        self._word = word.strip()

    @property
    def added(self):
        return self._added
    @added.setter
    def added(self, added):
        if added is None or (isinstance(added, str) and added.strip() == ""):
            self._added = date.today()
        else:
            self._added = parse_date(added)
        
    @property
    def learned(self):
        return self._learned
    @learned.setter
    def learned(self, learned):
        if learned is None or (isinstance(learned, str) and learned.strip() == ""):
            self._learned = None
        else:
            self._learned = parse_date(learned)

    @property
    def is_known(self) -> bool:
        return self.learned is not None
    
    @property
    def learning_period(self) -> str:
        from_date = self.added
        to_date = self.learned if self.learned else date.today()
        days = abs((to_date - from_date).days)
        if days == 1:
            return "1 day"
        if days < 30 * 3:
            return f"{days} days"
        if days < 365 * 3:
            months = days // 30
            return f"{months} months"
        years = days // 365
        return f"{years} years"

    @classmethod
    def sanitize(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        # remove unsupported characters
        text = re.sub(r"[^a-zA-Z' -]", "", text)
        # remove multiple spaces
        text = re.sub(r"\s{2,}", " ", text)
        # remove multiple apostrophes
        text = re.sub(r"'{2,}", "'", text)
        # remove multiple hyphens
        text = re.sub(r"-{2,}", "-", text)
        # remove leading and trailing apostrophes and hyphens
        text = re.sub(r"^[ '-]+|[ '-]+$", "", text)
        return text.strip().lower()

    @classmethod
    def read_from_csv(cls) -> list:
        try:
            with open(cls.WORDS_CSV, "r") as file:
                words = csv.DictReader(file)
                return [Word(word) for word in words]
        except FileNotFoundError:
            return []

    @classmethod
    def save_to_csv(cls, words: list):
        words = [word.dictionary() for word in words]
        with open(cls.WORDS_CSV, "w") as file:
            writer = csv.DictWriter(file, fieldnames=["word", "added", "learned"])
            writer.writeheader()
            for word in words:
                writer.writerow(word)

def parse_date(d) -> date:
    if isinstance(d, date):
        return d
    try:
        return date.fromisoformat(d.strip())
    except ValueError:
        raise ValueError("Date must be in ISO format (YYYY-MM-DD)")