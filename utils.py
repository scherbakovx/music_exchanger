from typing import Optional, Tuple
import requests


CHECK_AMOUNT_OF_SONGS_IN_PLAYLIST = False


def validate_playist_url(playlist_url: str, access_token: str = None) -> Tuple[bool, Optional[str]]:
    if playlist_url.startswith("https://open.spotify.com/playlist/"):
        if CHECK_AMOUNT_OF_SONGS_IN_PLAYLIST and access_token:
            url = "https://api.spotify.com/v1/playlists/%s/tracks" % playlist_url
            response = requests.get(
                url,
                headers={
                    'Authorization': 'Bearer %s' % access_token
                }
            )
            if response.status_code == 200:
                response_json = response.json()
                try:
                    assert len(response_json['items']) == 5
                    return True, None
                except AssertionError:
                    return False, "В плейлисте должно быть ровно 5 песен"
        else:
            return True, None
    else:
        return False, "Это не похоже на ссылку на Spotify..."
