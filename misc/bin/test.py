import pathlib
from pprint import pprint

from src.megamekfileparser.mekparser import MekParser

p = pathlib.Path('/Users/chris/Desktop/megamekparser/misc/static/megamexfiles/3039u/Grand Dragon DRG-1G.mtf')

x = MekParser(p)

x.parse()
pprint(dict(x.mech))
