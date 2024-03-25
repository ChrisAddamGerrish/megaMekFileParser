import pathlib
from pprint import pprint

from MegaMechFileParser.mechparser import MechParser

p = pathlib.Path('/Users/chris/Desktop/mmparser/static/megamexfiles/3050U/Black Hawk (Nova) A.mtf')

x = MechParser(p)

x.parse()
pprint(dict(x.mech))
