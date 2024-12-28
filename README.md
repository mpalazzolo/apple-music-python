# apple-music-python

A python wrapper for the Apple Music API. 

See the [Apple Music API documentation](https://developer.apple.com/documentation/applemusicapi) for additional info.

## Getting Started

### Documentation
Find more documentation of the project here:
https://apple-music-python.readthedocs.io

### Prerequisites

You must have an Apple Developer Account and a MusicKit API Key. See instructions on how to obtain these here: [Getting Keys And Creating Tokens.](https://developer.apple.com/documentation/applemusicapi/getting_keys_and_creating_tokens)

To access a user's library, you need to have a music_user_token. See MusicKit for instructions: [User Authentication for MusicKit.](https://developer.apple.com/documentation/applemusicapi/user_authentication_for_musickit)

### Dependencies

- [Requests](https://github.com/requests/requests) 
- [PyJWT](https://github.com/jpadilla/pyjwt)
- [Cryptography](https://github.com/pyca/cryptography)

### Installing

```
python setup.py install
```

or

```
pip install apple-music-python
```

### Example

```python
import applemusicpy

secret_key = 'x'
key_id = 'y'
team_id = 'z'
music_user_token = 'm'

am = applemusicpy.AppleMusic(secret_key=secret_key, key_id=key_id, team_id=team_id, music_user_token=music_user_token)

results = am.search('travis scott', types=['albums'], limit=5)
for item in results['results']['albums']['data']:
    print(item['attributes']['name'])

user_results = am.current_user_saved_tracks(limit=5, offset=0)
for song in user_results['data']:
    print(song['attributes']['name'])
```

## Versioning

- v1.0.0 - Initial Release - 12/15/2018
- v1.0.1 - Updated package info on PyPI - 12/16/2018
- v1.0.2 - Added Windows search support - 01/21/2019
- v1.0.3 - Fixed error handling of HTTPError - 11/03/2019
- v1.0.4 - Fixed error with reading token - 01/24/2021
- v1.0.5 - Refresh token before request if token is expired - 05/09/2021
- v2.0.0 - Added Enhanced User Library Functions - 08/16/2023

## Authors

* **Matt Palazzolo** - [GitHub Profile](https://github.com/mpalazzolo)
* **Jonathan Jacobson** - [GitHub Profile](https://github.com/j-jacobson)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details


