import nltk
from nltk.stem.lancaster import LancasterStemmer

_TAG_LIST = ['JJ', 'JJR ', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def filter_text(text: str) -> str:
    st = LancasterStemmer()  # Normalize the words
    filtered_text = ''  # Initialize the string

    # Filter all words based in their types using the list _TAG_LIST
    for token in nltk.pos_tag(text.lower().split()):
        if token[1] in _TAG_LIST:
            filtered_text = filtered_text + ' ' + st.stem(token[0])

    return filtered_text
