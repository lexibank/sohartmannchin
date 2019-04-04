# coding=utf-8
from __future__ import unicode_literals, print_function

from clldutils.path import Path
from clldutils.misc import slug
from pylexibank.dataset import Metadata
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import getEvoBibAsBibtex, pb
from lingpy import *


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'sohartmannchin'

    def cmd_install(self, **kw):

        with self.cldf as ds:
            ds.add_sources()
            ds.add_languages(id_factory=lambda l: slug(l['Name']))
            concepts = {c['ENGLISH']: slug(c['ENGLISH']) for c in
                    self.concepts}
            for concept in self.concepts:
                ds.add_concept(
                        ID=slug(concept['ENGLISH']),
                        Name=concept['ENGLISH'],
                        Concepticon_ID=concept['CONCEPTICON_ID']
                        )

            # add lexemes
            wl = Wordlist(self.raw.posix('HSH-SCL.csv'))
            for idx in pb(wl, desc='cldfify'):
                ds.add_lexemes(
                        Language_ID=slug(wl[idx, 'language']),
                        Value=wl[idx, 'reflex'],
                        Source='SoHartmann1988',
                        Parameter_ID=slug(wl[idx, 'concept'])
                        )

