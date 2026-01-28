import re
from nltk import FreqDist, ngrams, word_tokenize

# Download necessary NLTK data (only needs to be run once)
# import nltk
# nltk.download('all')

def get_word_suggestions(text_corpus, current_word, num_suggestions=5):
    """
    Generates word suggestions based on a given text corpus and the current word.
    """
    # Tokenize the corpus into words
    words = word_tokenize(text_corpus.lower())

    # Create bigrams (pairs of consecutive words)
    bigrams = list(ngrams(words, 2))

    # Filter bigrams to find those where the first word matches the current_word
    # and create a frequency distribution of the subsequent words
    next_word_freq = FreqDist([
        next_word for prev_word, next_word in bigrams
        if prev_word == current_word.lower()
    ])

    # Get the most common next words as suggestions
    suggestions = [word for word, _ in next_word_freq.most_common(num_suggestions)]
    return suggestions


if __name__ == "__main__":
    corpus = """
   hello my name is and i love you
    """

    # Get suggestions for "the"
    suggestions_for_the = get_word_suggestions(corpus, "hello")
    print(f"Suggestions for 'the': {suggestions_for_the}")

    # Get suggestions for "fox"
    suggestions_for_fox = get_word_suggestions(corpus, "fox")
    print(f"Suggestions for 'fox': {suggestions_for_fox}")

    # Get suggestions for a word not in the corpus
    suggestions_for_apple = get_word_suggestions(corpus, "apple")
    print(f"Suggestions for 'apple': {suggestions_for_apple}")