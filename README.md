# apple-music-python

A python wrapper for the Apple Music API. 

See the [Apple Music API documentation](https://developer.apple.com/documentation/applemusicapi/about_the_apple_music_api) for additional info:

NOTE: This does not support library resources.

## Getting Started


### Prerequisites

You must have an Apple Developer Account and a MusicKit API Key. See instructions on how to obtain these here: [Getting Keys And Creating Tokens.](https://developer.apple.com/documentation/applemusicapi/getting_keys_and_creating_tokens)

### Dependencies

- [Requests](https://github.com/requests/requests) 
- [PyJWT](https://github.com/jpadilla/pyjwt)

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

v1.0.0 - Initial Release - 12/15/2018

## Authors

* **Matt Palazzolo** - [GitHub Profile](https://github.com/mpalazzolo)

## License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details

