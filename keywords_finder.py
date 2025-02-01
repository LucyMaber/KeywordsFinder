import logging
import re
import unicodedata
from typing import List, Tuple, Dict
import ahocorasick

# Set up logging with DEBUG level for detailed output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class KeywordFinder:
    def __init__(self, keywords: List[str]):
        self.keywords = [kw.lower() for kw in keywords]
        self.automaton = self._build_automaton()
    
    def _build_automaton(self):
        automaton = ahocorasick.Automaton()
        for idx, word in enumerate(self.keywords):
            automaton.add_word(word, (idx, word))
        automaton.make_automaton()
        logger.info("Aho-Corasick automaton built with %d words.", len(self.keywords))
        return automaton
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text by removing accents, punctuation, and extra spaces."""
        if not text:
            return ""
        text = unicodedata.normalize("NFKD", text)
        text = ''.join(c for c in text if not unicodedata.combining(c))
        text = re.sub(r"[^\w\s-]", "", text)
        return re.sub(r"\s+", " ", text).strip().lower()
    
    def find_keywords(self, text: str) -> List[Tuple[str, int, int]]:
        """Find keyword occurrences in text and return matched phrases with positions."""
        matches = []
        text_lower = text.lower()
        
        for end_index, (idx, word) in self.automaton.iter(text_lower):
            start_index = end_index - len(word) + 1
            
            # Check word boundaries
            if (start_index > 0 and text_lower[start_index - 1].isalnum()) or \
               (end_index < len(text_lower) - 1 and text_lower[end_index + 1].isalnum()):
                continue
            
            matches.append((word, start_index, end_index))
            logger.debug(f"Matched '{word}' at {start_index}-{end_index}")
        
        logger.info("Total keywords found: %d", len(matches))
        return matches
    
    def keyword_stats(self, text: str) -> Tuple[int, List[str], List[Tuple[str, int, int]], int]:
        """Compute keyword statistics: unique count, matched keywords, occurrences, and total count."""
        normalized_text = self.normalize_text(text)
        matches = self.find_keywords(normalized_text)
        unique_keywords = list(set(word for word, _, _ in matches))
        return len(unique_keywords), unique_keywords, matches, len(matches)

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
