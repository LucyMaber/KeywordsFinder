# KeywordsFinder

A Python package for efficiently finding and analyzing keyword occurrences in text using the **Aho-Corasick algorithm**.

## Features

- **Fast keyword searching** with the Aho-Corasick trie-based algorithm.
- **Text normalization** to improve accuracy by removing accents, punctuation, and extra spaces.
- **Word boundary checking** to ensure only whole-word matches.
- **Detailed keyword statistics**, including:
  - Number of unique matched keywords
  - List of unique keywords found
  - Total occurrences with start and end positions

## Installation

Ensure you have Python 3.7+ installed. Install dependencies with:

```bash
pip install -r requirements.txt
```

Or install `ahocorasick` separately:

```bash
pip install pyahocorasick
```

## Usage

### Example Script

```python
from keywords_finder import KeywordFinder

# Define keywords
KEYWORDS = ["trans", "transphobia", "anti-trans", "trans rights"]

# Initialize finder
finder = KeywordFinder(KEYWORDS)

# Sample text
sample_text = """
The transgender community is fighting for trans rights and against transphobia.
However, some individuals express anti-trans sentiments and support trans exclusionary policies.
It's important to support trans people and ensure gender-affirming care is accessible.
"""

# Get keyword statistics
unique_count, unique_keywords, occurrences, total_count = finder.keyword_stats(sample_text)

print(f"Unique Keywords Count: {unique_count}")
print(f"Unique Keywords: {unique_keywords}")
print(f"Total Occurrences: {total_count}")
print("Occurrences with Positions:")
for phrase, start, end in occurrences:
    print(f" - '{phrase}' found at positions {start}-{end}")
```

### Output Example

```
Unique Keywords Count: 3
Unique Keywords: ['trans rights', 'transphobia', 'anti-trans']
Total Occurrences: 4
Occurrences with Positions:
 - 'trans rights' found at positions 40-51
 - 'transphobia' found at positions 66-76
 - 'anti-trans' found at positions 120-129
 - 'trans' found at positions 163-167
```

## API Reference

### `KeywordFinder(keywords: List[str])`
Initializes a keyword finder with a given list of keywords.

### `.find_keywords(text: str) -> List[Tuple[str, int, int]]`
Finds all keyword occurrences in the given text.

### `.keyword_stats(text: str) -> Tuple[int, List[str], List[Tuple[str, int, int]], int]`
Returns statistics:
- Unique keyword count
- List of unique matched keywords
- List of occurrences with positions
- Total keyword occurrences count


