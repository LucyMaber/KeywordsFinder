import logging
import re
import unicodedata
from typing import List, Tuple
import ahocorasick

# Precompile regex patterns to avoid repeated compilation.
_NON_WORD_REGEX = re.compile(r"[^\w\s-]")
_WHITESPACE_REGEX = re.compile(r"\s+")


class KeywordFinder:
    def __init__(self, keywords: List[str]):
        # Store keywords in lower-case for consistency.
        self.keywords = [kw.lower() for kw in keywords]
        self.automaton = self._build_automaton()
    
    def _build_automaton(self):
        automaton = ahocorasick.Automaton()
        for idx, word in enumerate(self.keywords):
            automaton.add_word(word, (idx, word))
        automaton.make_automaton()
        return automaton
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text by:
          - Converting to NFKD form
          - Removing accents (combining characters)
          - Removing punctuation (except word characters, spaces, and hyphens)
          - Replacing multiple spaces with a single space
          - Lowercasing the result
        """
        if not text:
            return ""
        # Normalize and remove diacritics
        text = unicodedata.normalize("NFKD", text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        # Remove punctuation using precompiled regex
        text = _NON_WORD_REGEX.sub("", text)
        # Replace multiple whitespace with a single space and lower-case the text
        return _WHITESPACE_REGEX.sub(" ", text).strip().lower()
    
    def find_keywords(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Find keyword occurrences in text and return matched phrases with positions.
        Assumes that the input text is already normalized (i.e. lower-case).
        """
        matches = []
        # Since normalize_text returns lower-case text, no need to call .lower() here.
        text_lower = text
        for end_index, (idx, word) in self.automaton.iter(text_lower):
            start_index = end_index - len(word) + 1
            
            # Check word boundaries to ensure we have full word matches.
            if (start_index > 0 and text_lower[start_index - 1].isalnum()) or \
               (end_index < len(text_lower) - 1 and text_lower[end_index + 1].isalnum()):
                continue
            
            matches.append((word, start_index, end_index))
        
        return matches
    
    def keyword_stats(self, text: str) -> Tuple[int, List[str], List[Tuple[str, int, int]], int]:
        """
        Compute keyword statistics:
          - The number of unique keywords found.
          - A list of unique keywords found.
          - A list of all occurrences with their positions.
          - The total number of occurrences.
        """
        normalized_text = self.normalize_text(text)
        matches = self.find_keywords(normalized_text)
        unique_keywords = list({word for word, _, _ in matches})
        return len(unique_keywords), unique_keywords, matches, len(matches)


# Example usage:
if __name__ == "__main__":
    KEYWORDS = ["trans", "transphobia", "anti-trans", "trans rights"]
    finder = KeywordFinder(KEYWORDS)
    
    sample_text = """
    The transgender community is fighting for trans rights and against transphobia.
    However, some individuals express anti-trans sentiments and support trans exclusionary policies.
    It's important to support trans people and ensure gender-affirming care is accessible.
    """
    
    unique_count, unique_keywords, occurrences, total_count = finder.keyword_stats(sample_text)
    
    print(f"Unique Keywords Count: {unique_count}")
    print(f"Unique Keywords: {unique_keywords}")
    print(f"Total Occurrences: {total_count}")
    print("Occurrences with Positions:")
    for phrase, start, end in occurrences:
        print(f" - '{phrase}' found at positions {start}-{end}")
