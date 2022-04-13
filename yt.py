#!/bin/env python3

import sys, os.path as path, os, json
from ytmusicapi import YTMusic

root = path.dirname(sys.argv[0])

with open(path.join(root, 'raw.json')) as f:
    data = json.load(f)

headers_auth = path.join(os.environ.get('HOME'), '.config', 'headers_auth.json')
yt = YTMusic(headers_auth)

for i, pl in enumerate(data['playlists'][:]):
    playlist = pl["name"]
    if playlist != 'kek':
        continue
    print(f'playlist {playlist}')
    videoIds = []
    for i, item in enumerate(pl['items']):
        track = item['track']
        name = track['trackName']
        artist = track['artistName']
        album = track['albumName']
        print(f'\x1b[33m{name} by {artist} from {album}:\x1b[0m')

        results = yt.search(f'{name} by {artist}')
        if len(results) == 0:
            print('===ERROR=== no results')
        for res in results:
            if res['resultType'] == 'song':
                title = res['title']
                artists = ', '.join((a['name'] for a in res['artists']))
                album = res['album']['name']
                id = res['videoId']
                print(f'\x1b[32madding "{title}" by ({artists}) from [{album}]\x1b[0m')
                if id not in videoIds:
                    videoIds.append(id)
                break

    plid = yt.create_playlist(playlist, f'ohno {playlist}')
    res = yt.add_playlist_items(plid, videoIds)
    if res['status'] != 'STATUS_SUCCEEDED':
        print('\x1b[31m===ERROR=== failed adding items to playlist\x1b[0m')
        print(res)
        print()
    else:
        print('\x1b[32m===OK===\x1b[0m')

