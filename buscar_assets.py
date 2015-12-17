import json
import os

data = json.loads(open('data/megamente.json', 'r').read())

for coso in data:
    for r in coso.get('respuesta'):
        if coso.get('objeto'):
            nombre = 'assets/img/deduccion/%s-%s.png' % (coso['objeto'], r)
        else:
            nombre = 'assets/img/deduccion/%s.png' % r

        if not os.path.exists(nombre):
            print 'FALTA: %s' % nombre.split('/')[3]
