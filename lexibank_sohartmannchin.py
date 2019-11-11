from pathlib import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from pylexibank import Concept, Language

from clldutils.misc import slug
import attr
from lingpy import *


@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default="Chin")
    Family = attr.ib(default="Sino-Tibetan")
    DialectGroup = attr.ib(default=None)


@attr.s
class CustomConcept(Concept):
    SrcID = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "sohartmannchin"
    language_class = CustomLanguage

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        language_lookup = args.writer.add_languages(lookup_factory="Name")
        concept_lookup = args.writer.add_concepts(
            id_factory=lambda x: x.id.split("-")[-1] + "_" + slug(x.english), lookup_factory="Name"
        )
        wl = Wordlist(self.raw_dir.joinpath("HSH-SCL.csv").as_posix())
        for idx in progressbar(wl):
            args.writer.add_forms_from_value(
                Language_ID=language_lookup[wl[idx, "language"]],
                Value=wl[idx, "reflex"],
                Source=["SoHartmann1988"],
                Parameter_ID=concept_lookup[wl[idx, "concept"]],
            )
