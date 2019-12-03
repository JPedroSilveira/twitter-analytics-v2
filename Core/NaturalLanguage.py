import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer

_TAG_LIST = ['JJ', 'JJR ', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
# Changes in this value implies in BTree changes, some BTree that uses this function are adapted for 50 chars
_WORD_MAX_SIZE = 50


def filter_text(text: str) -> str:
    try:
        text = re.sub('[^a-z0-9- ]+', '', text.lower().rstrip())

        sw = set(stopwords.words('english'))
        result = ''
        words = list(filter(lambda x: x != '', text.split(' ')))

        st = LancasterStemmer()  # Normalize the words

        # Filter all words based in their types using the list _TAG_LIST
        for token in nltk.pos_tag(words):
            text = token[0]
            if len(text) <= _WORD_MAX_SIZE:
                text = text[:_WORD_MAX_SIZE]

            if token[1] in _TAG_LIST and token[0] not in sw:
                if result == '':
                    result = st.stem(text)
                else:
                    result = result + ' ' + st.stem(token[0])

        return result

    except LookupError:
        nltk.download('stopwords')
        nltk.download('punkt')
        return filter_text(text)
