import os

from lxml import etree

from pos_tag import PosTag


class WordNet(object):
    """
    This class contains functionality to handle WordNets, which follow the structure of
    the german odenet, which is linked in the README.
    It can be used to find words with similar meaning. While synonyms can be retrieved,
    note that it is not guaranteed that the given word sense is as intended.

    Typical Usage:
        wordnet = WordNet()
        related_words = wordnet.find_related_concepts("FooBar", PosTag.VERB)
    """

    XPATH_EXPRESSIONS = {
        "members": "//Sense[@synset='{}']/preceding-sibling::*/@writtenForm",
        "synsets": "//Lemma[@writtenForm='{}']/following-sibling::*/@synset",
        "synsets_by_pos_tag": "//Lemma[@writtenForm='{}' and @partOfSpeech='{}']/following-sibling::*/@synset"
    }

    def __init__(self, path=None):
        if path is None:
            dir_name = os.path.dirname(__file__)
            path = os.path.join(dir_name, "deWordNet.xml")
        self._tree = etree.parse(path)

    def _find_synsets(self, word, pos_tag=None):
        """
        Retrieves all synsets for the given word from the underlying wordnet.
        A part-of-speech tag can be specified according to the enum PoSTags.

        Args:
            word: Word string.
        Returns:
            A list of string identifiers of synsets for the given word.
        """
        if not PosTag.is_valid(pos_tag):
            raise ValueError("The given Part-of-Speech tag is invalid.")

        if pos_tag is None:
            xpath_expr = self.XPATH_EXPRESSIONS["synsets"].format(word)
        else:
            xpath_expr = self.XPATH_EXPRESSIONS["synsets_by_pos_tag"].format(word, pos_tag.value)

        synsets = self._tree.xpath(xpath_expr)
        return set(synsets)

    def find_related_concepts(self, word, pos_tag=None):
        """Retrieves all words which share at least one concept with the given word.

        Args:
            word: Word string.
        Returns:
            A set of words sharing at least one concept with the given word.
        """
        synonym_candidates = set()
        synsets = self._find_synsets(word, pos_tag)

        for synset in synsets:
            members = self._tree.xpath(self.XPATH_EXPRESSIONS["members"].format(synset))
            synonym_candidates.update(set(members))

        return synonym_candidates
