from datetime import date
import csv
import re

class Word:
    WORDS_CSV = "words.csv"

    def __init__(self, word, added=None, learned=None):
        self.added = added
        self.learned = learned
        if isinstance(word, dict):
            self._from_dictionary(word)
        else:
            self.word = word
 
    def __str__(self):
        return self.word
    
    def _from_dictionary(self, data: dict) -> 'Word':
        keys = list(data.keys())
        if "word" in keys:
            self.word = data["word"]
        else:
            self.word = data[keys[0]]
        if "added" in keys:
            self.added = data["added"]
        if "learned" in keys:
            self.learned = data["learned"]
        return self

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
        if isinstance(added, date):
            self._added = added
        elif not isinstance(added, str) or added.strip() == "":
            self._added = date.today()
        else:
            try:
                self._added = date.fromisoformat(added.strip())
            except ValueError:
                self._added = date.today()
        
    @property
    def learned(self):
        return self._learned
    @learned.setter
    def learned(self, learned):
        if isinstance(learned, date):
            self._learned = learned
        elif not isinstance(learned, str) or learned.strip() == "":
            self._learned = None
        else:
            try:
                self._learned = date.fromisoformat(learned.strip())
            except ValueError:
                self._learned = date.today()

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
        # cut length to 50 characters
        text = text[:50]
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
                result = []
                for word in words:
                    try:
                        result.append(Word(word))
                    # skip invalid words
                    except ValueError:
                        pass
                return result
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