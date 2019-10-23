import math
from abc import abstractmethod

import pycode_similar
from diff_match_patch import diff_match_patch


class Comparator:

    @abstractmethod
    def compare(self, a, b):
        pass


class PycodeComparison(Comparator):

    def compare(self, a, b):
        res = pycode_similar.detect(["\n".join(a), "\n".join(b)], diff_method=pycode_similar.UnifiedDiff)
        val = res[0][1][0].plagiarism_percent
        return val


class DiffComparator(Comparator):

    def __init__(self, base=None) -> None:
        super().__init__()

        self.H = None

        if base is not None:
            self.H = set()
            for e in base:
                self.H.add(e)

    def filter(self, s):
        return [e for e in s if e not in self.H]

    def compare(self, a, b):

        if self.H is not None:
            a, b = self.filter(a), self.filter(b)

        dmp = diff_match_patch()
        dmp.Diff_Timeout = math.inf
        ret = dmp.diff_linesToChars("\n".join(a), "\n".join(b))

        diff = dmp.diff_main(*ret)
        dmp.diff_charsToLines(diff, ret[2])
        #dmp.diff_cleanupSemantic(diff)

        perc = 1 - len([e for e in diff if e[0] != 0]) / (len(a) + len(b))

        #html = dmp.diff_prettyHtml(diff)
        #with open("test.html", "w") as f:
        #    f.write(html)

        return perc
