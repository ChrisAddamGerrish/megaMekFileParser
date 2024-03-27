import pathlib
from pprint import pprint

from src.megamekfileparser.mekparser import MekParser

p = pathlib.Path('/misc/static/megamexfiles/3050U/Black Hawk (Nova) A.mtf')

x = MekParser(p)

x.parse()
pprint(dict(x.mech))
