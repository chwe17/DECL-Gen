from typing import Tuple, Dict
from Bio.Seq import Seq

class AlignmentResult():
    """ Represents the result of codon alignment. """
    _result = None
    _key_annotations = {
        "reads_processed": ("Processed Reads", "both"),
        "reads_useful": ("Useful Reads", "both"),
        "valid_pairs": ("Valid Pairs", "paired"),
        "invalid_pairs": ("Invalid Pairs", "paired"),
        "low_quality_skips": ("Low Quality skips", "single"),
        "both_low_quality_skips": ("Low Quality skips (both)", "paired"),
        "r1_low_quality_skips": ("Low Quality skips (r1)", "paired"),
        "r2_low_quality_skips": ("Low Quality skips (r2)", "paired"),
    }
    paired = False
    _codons = None

    def __init__(self, paired=True):
        self._result = {key: 0 for key in self._key_annotations}
        self._codons = {}
        self._paired = paired
        self._failed_reads = []

    def __getitem__(self, item):
        if item not in self._result:
            raise ValueError(
                "Result only supports a set amount of keys: {}, but {} given".format(
                    ", ".join(self._result.keys()),
                    item
                )
            )

        return self._result[item]

    def __setitem__(self, item, value):
        if item not in self._result:
            raise ValueError(
                "Result only supports a set amount of keys: {}, but {} given".format(
                    ", ".join(self._result.keys()),
                    item
                )
            )

        self._result[item] = value

    def __add__(self, othr: "AlignmentResult"):
        r = self.__class__()
        # Add result meta
        for key in self._result:
            r[key] = self[key] + othr[key]

        # Merge codon lists
        self_codons = self.get_codons()
        othr_codons = othr.get_codons()

        for codon in self_codons:
            r.increase_codon(codon, self_codons[codon])
        for codon in othr_codons:
            r.increase_codon(codon, othr_codons[codon])

        # Merge failed reads
        r._failed_reads = self._failed_reads + othr._failed_reads

        return r

    def __str__(self):
        ret = []

        for key in self._result:
            annotation = self._key_annotations[key]
            value = self._result[key]

            if self._paired is True and annotation[1] in ["both", "paired"]:
                ret.append("{0:<30} {1}".format(annotation[0], value))
            elif self._paired is False and annotation[1] in ["both", "single"]:
                ret.append("{0:<30} {1}".format(annotation[0], value))

        return "\n".join(ret)

    def init_codon(self, codon: Tuple) -> None:
        """
        Initializes a given codon set by adding it to the dictionary and setting it to 0. If already existing, this
        method does nothing.
        :param codon: A tuple of codons
        :return:
        """
        if codon not in self._codons:
            self._codons[codon] = 0

    def increase_codon(self, codon: Tuple, increase: int = 1) -> None:
        """
        Increases the counts of a given codon by the given amount. If the amount is not given, it increases the codon by 1.
        :param codon:
        :param increase:
        :return:
        """
        self.init_codon(codon)
        self._codons[codon] += increase

    def get_codons(self) -> Dict[Tuple, int]:
        """
        Returns the dictionary of codons.
        :return: A dictionary where keys are tuples of codons and values the corresponding integer.
        """
        return self._codons

    def add_failed_read(self, read1, read2):
        self._failed_reads.append((read1, read2))