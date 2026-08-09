"""
Text processing and NLP utility functions using strictly Python standard library.
"""
import re
import math
from collections import Counter

# Standard English stop words
STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being',
    'below', 'between', 'both', 'but', 'by', 'can', 'can\'t', 'cannot', 'could',
    'couldn\'t', 'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t',
    'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t',
    'has', 'hasn\'t', 'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s',
    'her', 'here', 'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how',
    'how\'s', 'i', 'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is',
    'isn\'t', 'it', 'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most',
    'mustn\'t', 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once',
    'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over',
    'own', 'same', 'shan\'t', 'she', 'she\'d', 'she\'ll', 'she\'s', 'should',
    'shouldn\'t', 'so', 'some', 'such', 'than', 'that', 'that\'s', 'the', 'their',
    'theirs', 'them', 'themselves', 'then', 'there', 'there\'s', 'these', 'they',
    'they\'d', 'they\'ll', 'they\'re', 'they\'ve', 'this', 'those', 'through',
    'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasn\'t', 'we', 'we\'d',
    'we\'ll', 'we\'re', 'we\'ve', 'were', 'weren\'t', 'what', 'what\'s', 'when',
    'when\'s', 'where', 'where\'s', 'which', 'while', 'who', 'who\'s', 'whom',
    'why', 'why\'s', 'with', 'won\'t', 'would', 'wouldn\'t', 'you', 'you\'d',
    'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours', 'yourself', 'yourselves',
    'will', 'shall', 'may', 'might', 'must', 'can', 'eg', 'ie', 'etc', 'also'
}


def normalize_text(text: str) -> str:
    """Clean and normalize raw text string."""
    if not text:
        return ""
    # Lowercase text
    text = text.lower()
    # Replace non-breaking spaces or tabs with regular space
    text = re.sub(r'[\t\r\n]+', ' ', text)
    # Strip excess spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def tokenize(text: str) -> list:
    """
    Tokenize text into lowercased words, keeping special developer tokens like C++, C#, .NET, Node.js.
    """
    if not text:
        return []
    # Clean text first but retain technical punctuation
    text_lower = text.lower()
    # Match technical terms or standard word characters
    pattern = r'[a-z0-9]+(?:\.[a-z0-9]+)*(?:\+\+|#)?'
    tokens = re.findall(pattern, text_lower)
    return tokens


def remove_stopwords(tokens: list) -> list:
    """Filter out standard English stop words."""
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def extract_ngrams(tokens: list, min_n: int = 1, max_n: int = 3) -> list:
    """Extract n-grams (unigrams, bigrams, trigrams) from token list."""
    ngrams = []
    num_tokens = len(tokens)
    for n in range(min_n, max_n + 1):
        for i in range(num_tokens - n + 1):
            ngram = " ".join(tokens[i:i + n])
            ngrams.append(ngram)
    return ngrams


def simple_stem(word: str) -> str:
    """Simple suffix stripping for light stemming without external NLP libs."""
    word = word.lower()
    suffixes = ('ing', 'ed', 'es', 's', 'ment', 'ation', 'ional', 'ly', 'er', 'ors')
    for suffix in suffixes:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[:-len(suffix)]
    return word


def calculate_term_frequencies(text: str) -> dict:
    """Calculate term frequencies for TF-IDF keyword overlap analysis."""
    tokens = remove_stopwords(tokenize(text))
    if not tokens:
        return {}
    counts = Counter(tokens)
    total = len(tokens)
    return {word: count / total for word, count in counts.items()}


def cosine_similarity(text1: str, text2: str) -> float:
    """
    Calculate TF-IDF inspired cosine similarity between two text strings using standard library.
    """
    tf1 = calculate_term_frequencies(text1)
    tf2 = calculate_term_frequencies(text2)
    
    if not tf1 or not tf2:
        return 0.0
    
    all_words = set(tf1.keys()).union(set(tf2.keys()))
    
    dot_product = sum(tf1.get(w, 0.0) * tf2.get(w, 0.0) for w in all_words)
    mag1 = math.sqrt(sum(v ** 2 for v in tf1.values()))
    mag2 = math.sqrt(sum(v ** 2 for v in tf2.values()))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
        
    return dot_product / (mag1 * mag2)
