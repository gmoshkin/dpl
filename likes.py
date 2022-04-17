#!/bin/env python3

import sys, os.path as path, os, json
from ytmusicapi import YTMusic

if len(sys.argv) < 1:
    print('need path/to/MyData/YourLibrary.json as first argument')

with open(sys.argv[1]) as f:
    data = json.load(f)

headers_auth = path.join(os.environ.get('HOME'), '.config', 'headers_auth.json')
yt = YTMusic(headers_auth)

for i, track in enumerate(data['tracks']):
    name = track['track']
    artist = track['artist']
    album = track['album']
    print(f'\x1b[33m{name} by {artist} from {album}:\x1b[0m')

    results = yt.search(f'{name} by {artist}')
    if len(results) == 0:
        print('===ERROR=== no results')
    for res in results:
        if res['resultType'] == 'song':
            title = res['title']
            artists = ', '.join((a['name'] for a in res['artists']))
            album = res['album']['name'] if res['album'] is not None else '<none>'
            videoId = res['videoId']
            print(f'liking "{title}" by ({artists}) from [{album}] ...', end = '')
            yt.rate_song(videoId, 'LIKE')
            print(' \x1b[32mok\x1b[0m')
            break

