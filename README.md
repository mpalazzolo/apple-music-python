# apple-music-python

A python wrapper for the Apple Music API. 

See the [Apple Music API documentation](https://developer.apple.com/documentation/applemusicapi/about_the_apple_music_api) for additional info.

NOTE: This does not support library resources.

## Getting Started

### Documentation
Find full documentation of the project here:
https://apple-music-python.readthedocs.io

### Prerequisites

You must have an Apple Developer Account and a MusicKit API Key. See instructions on how to obtain these here: [Getting Keys And Creating Tokens.](https://developer.apple.com/documentation/applemusicapi/getting_keys_and_creating_tokens)

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

am = applemusicpy.AppleMusic(secret_key=secret_key, key_id=key_id, team_id=team_id)
results = am.search('travis scott', types=['albums'], limit=5)
for item in results['results']['albums']['data']:
    print(item['attributes']['name'])
```

## Versioning

- v1.0.0 - Initial Release - 12/15/2018
- v1.0.1 - Updated package info on PyPI - 12/16/2018
- v1.0.2 - Added Windows search support - 01/21/2019
- v1.0.3 - Fixed error handling of HTTPError - 11/03/2019
- v1.0.4 - Fixed error with reading token - 01/24/2021
- v1.0.5 - Refresh token before request if token is expired - 05/09/2021

## Authors

* **Matt Palazzolo** - [GitHub Profile](https://github.com/mpalazzolo)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details


