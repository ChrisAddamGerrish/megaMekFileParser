import json
import pathlib
from MegaMechFileParser.mechparser import MechParser
import time
import uuid

cwd = pathlib.Path.cwd().joinpath('../static/megamexfiles')

print(cwd.parent)

p = pathlib.Path(cwd).rglob('*.mtf')

files = [x for x in p if x.is_file()]
i = 0
out = {}
failed = []

start = time.time()
for f in files:
    print(f.relative_to(cwd.parent))
    x = MechParser(f)

    try:
        x.parse()
    except Exception as e:
        failed.append(f'{f} ; {e}')

    y = dict(x.mech)

    y['file'] = str(f.relative_to(cwd.parent))

    i += 1
    print(i)
    objectId = uuid.uuid4().__str__()
    out.update({objectId : y})

with open('../static/all.json', 'w') as f:
    f.write(json.dumps(out, indent=4))

end = time.time()

with open('../static/failed.txt', 'w') as o:
    for i in failed:
        string = f'{i}\n'
        o.write(string)

print(end - start)



