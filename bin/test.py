import pathlib

from mechparser import MechParser
p = pathlib.Path('/Users/chris/Desktop/mmparser/mechs/ToS/ToS Kaumberg/Phoenix PX-1KR.mtf')

x = MechParser(p)

x.parse()