from clldutils.misc import slug
from clldutils.path import Path
from lingpy import *
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import pb
from pylexibank.dataset import Concept, Language
import attr


@attr.s
class HLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    ChineseName = attr.ib(default=None)
    SubGroup = attr.ib(default='Chin')
    Family = attr.ib(default='Sino-Tibetan')
    DialectGroup = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "sohartmannchin"
    language_class = HLanguage

    def cmd_install(self, **kw):

        with self.cldf as ds:
            ds.add_sources()
            languages = {l['Name']: l['ID'] for l in self.languages}
            ds.add_languages()
            for concept in self.conceptlist.concepts.values():
                ds.add_concept(
                    ID=slug(concept.english),
                    Name=concept.english,
                    Concepticon_ID=concept.concepticon_id,
                    Concepticon_Gloss=concept.concepticon_gloss
                )
            # add lexemes
            wl = Wordlist(self.raw.posix("HSH-SCL.csv"))
            for idx in pb(wl, desc="cldfify"):
                ds.add_lexemes(
                    Language_ID=languages[wl[idx, "language"]],
                    Value=wl[idx, "reflex"],
                    Source="SoHartmann1988",
                    Parameter_ID=slug(wl[idx, "concept"]),
                )
