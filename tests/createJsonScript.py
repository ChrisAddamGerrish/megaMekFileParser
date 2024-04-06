import json
import pathlib
from pprint import pprint

from src.megamekfileparser.mekparser import MekParser
import time
import uuid

cwd = pathlib.Path.cwd().joinpath('../megamekfiles')

print(cwd.parent)

p = pathlib.Path(cwd).rglob('*.mtf')

files = [x for x in p if x.is_file()]
i = 0
out = {}
failed = []

start = time.time()

for f in files:
    print(f.relative_to(cwd.parent))
    mech = MekParser()

    try:
        mech_out = mech.parse(f)
    except Exception as e:
        failed.append(f'{f} ; {e}')

    y = dict()

    y['file'] = str(f.relative_to(cwd.parent))

    i += 1
    print(i)
    objectId = uuid.uuid4().__str__()
    out.update({objectId: y})
    #print(out.items())
    out.update({objectId: mech_out})

with open('../tests/all.json', 'w') as f:
    f.write(json.dumps(out, indent=4))

end = time.time()

with open('../tests/failed.txt', 'w') as o:
    for i in failed:
        string = f'{i}\n'
        o.write(string)

print(end - start)
