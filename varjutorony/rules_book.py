"""A Varjútorony ura – szabályok: a tárgylista, és a régiófájlok szabályai (a build.py --book használja)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(1, os.path.join(HERE, '..'))
import rules as G
import konyv, kv

doc = konyv.build()
json.dump(doc, open(os.path.join(HERE, 'book.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

G.ITEMS[:] = [
    ('ezusttor', 'Ezüsttőr'), ('kotel', 'Kötél'), ('lampas', 'Lámpás'), ('szenteltviz', 'Szentelt víz'),
    ('ezustkulcs', 'Ezüstkulcs'), ('napko', 'Napkő'), ('tolvajkulcs', 'Tolvajkulcs'), ('vaskulcs', 'Vaskulcs'),
    ('bronzkulcs', 'Bronzkulcs'), ('varjutoll', 'Varjútoll'), ('tukor', 'Ezüsttükör'), ('amulett', 'Ábris amulettje'),
    ('hus', 'Füstölt hús'), ('holdvirag', 'Holdvirág'), ('terkep', 'A torony térképe'), ('ezustrog', 'Ezüströg'),
    ('csengo', 'Rézcsengő'), ('kenyer', 'Elemózsia'), ('gyuru', 'Pecsétgyűrű'), ('level', 'Bodor levele'),
    ('sip', 'Fűzfasíp'), ('olaj', 'Lámpaolaj'), ('fahej', 'Kőfaragó véső'), ('meregital', 'Zöld üvegcse'),
    ('nev', ''), ('bence', ''), ('pecset', ''), ('kocka', ''), ('sas', ''), ('banya', ''), ('dometor', ''),
    ('temeto', ''), ('borcsa', ''), ('troll', ''), ('kiralyno', ''), ('rablo', ''), ('abris', ''),
    ('demon', ''), ('kelemen', ''),
]
G.ITEM_ID.clear(); G.ITEM_ID.update({k: i for i, (k, _) in enumerate(G.ITEMS)})
assert len(G.ITEMS) <= 64
G.KEY_ITEMS[:] = []
G.NO_RANDOM_LOSS.clear(); G.NO_RANDOM_LOSS.update({'ezustkulcs', 'amulett'})
G.START_ITEMS[:] = ['kenyer']
G.START_GOLD = 10
G.R.clear()
for name, (text, ops) in kv.S.items():
    if ops:
        G.r(konyv.NUM[name], *konyv.resolve(ops))
