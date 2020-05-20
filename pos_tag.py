from enum import Enum


class PosTag(Enum):
    """
    This class contains an enumeration of Part-of-Speech tags, which map the
    NLTK wordnet interface (https://github.com/nltk/nltk/blob/develop/nltk/corpus/reader/wordnet.py)
    to the odenet.
    """

    ADJ = "a"
    ADJ_SAT = "a"
    ADV = "a"
    NOUN = "n"
    VERB = "v"

    @classmethod
    def get_names(cls):
        return [tag.name for tag in cls]

    @classmethod
    def get_values(cls):
        return [tag.value for tag in cls]

    @classmethod
    def is_valid(cls, pos_tag):
        return pos_tag in cls or pos_tag is None

    @classmethod
    def to_dict(cls):
        return dict(zip(cls.get_names(), cls.get_values()))
