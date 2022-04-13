#!/bin/env python3

import sys, os.path as path, json
root = path.dirname(sys.argv[0])

with open(path.join(root, 'raw.json')) as f:
    data = json.load(f)

def prep(s):
    return s.strip().replace('<', '&lt;').replace('>', '&gt;')

with open(path.join(root, 'data.md'), 'w') as f:
    put = lambda *args, **kwargs: print(*args, **kwargs, file = f)
    put('# Playlists')
    put('')
    for p in data['playlists']:
        put(f'## {p["name"]}')
        for i, item in enumerate(p['items']):
            track = item['track']
            name = prep(track['trackName'])
            artist = prep(track['artistName'])
            album = prep(track['albumName'])
            put(f'{i + 1}. **{name}** by *{artist}*', end = '')
            if album and name != album:
                put(f' (album {album})', end='')
            put('')
        put('')
