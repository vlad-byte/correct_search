import json
import re
from itertools import chain


class Word:

    __slots__ = ["slices", "word", "alphabet"]

    def __init__(self, word):
        slice_range = range(len(word) + 1)
        self.slices = tuple((word[:i], word[i:]) for i in slice_range)
        self.word = word
        self.alphabet = "шиюынжсяплзухтвкйеобмцьёгдщэарчфъ"

    def _deletes(self):
        """th"""
        for a, b in self.slices[:-1]:
            yield "".join((a, b[1:]))

    def _transposes(self):
        """teh"""
        for a, b in self.slices[:-2]:
            yield "".join((a, b[1], b[0], b[2:]))

    def _replaces(self):
        """tge"""
        for a, b in self.slices[:-1]:
            for c in self.alphabet:
                yield "".join((a, c, b[1:]))

    def _inserts(self):
        """thwe"""
        for a, b in self.slices:
            for c in self.alphabet:
                yield "".join((a, c, b))

    def typos(self):
        return chain(
                self._deletes(), self._transposes(), self._replaces(), self._inserts()
            )

    def double_typos(self):
        return chain.from_iterable(
            Word(e1).typos()
            for e1 in self.typos()
        )


def load_from_tar():
    with open("result.json") as file:
        return json.load(file)


class Speller:
    __slots__ = ["nlp_data"]

    def __init__(self, nlp_data=None):
        self.nlp_data = load_from_tar() if nlp_data is None else nlp_data

    def existing(self, words):
        return {word for word in words if word in self.nlp_data}

    def get_candidates(self, word):
        w = Word(word)
        candidates = (
                self.existing([word])
                or self.existing(w.typos())
                or self.existing(w.double_typos())
                or [word])
        return [(self.nlp_data.get(c, 0), c) for c in candidates]

    def autocorrect_word(self, word):
        if word == "":
            return ""

        word = word.lower()
        candidates = self.get_candidates(word)
        best_word = max(candidates)[1]

        return best_word

    def autocorrect_sentence(self, sentence):
        word_regex = r"[АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя0123456789]+"
        return re.sub(
            word_regex,
            lambda match: self.autocorrect_word(match.group(0)),
            sentence)

    __call__ = autocorrect_sentence
