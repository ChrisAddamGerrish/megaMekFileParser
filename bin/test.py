import pathlib
from pprint import pprint

from MegaMechFileParser.mechparser import MechParser

p = pathlib.Path('/Users/chris/Desktop/mmparser/static/megamexfiles/3050U/Vindicator VND-5L.mtf')

x = MechParser(p)

x.parse()
pprint(dict(x.mech))
