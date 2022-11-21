from datetime import datetime, timedelta
import jwt
import requests
from requests.exceptions import HTTPError
import time
import re


class AppleMusic:
    """
    This class is used to connect to the Apple Music API and make requests for catalog resources
    """

    def __init__(self, secret_key, key_id, team_id, proxies=None,
                 requests_session=True, max_retries=10, requests_timeout=None, session_length=12):
        """
        :param proxies: A dictionary of proxies, if needed
        :param secret_key: Secret Key provided by Apple
        :param key_id: Key ID provided by Apple
        :param team_id: Team ID provided by Apple
        :param requests_session: Use request Sessions class. Speeds up API calls significantly when set to True
        :param max_retries: Maximum amount of times to retry an API call before stopping
        :param requests_timeout: Number of seconds requests should wait before timing out
        :param session_length: Length Apple Music token is valid, in hours
        """

        self.proxies = proxies
        self._secret_key = secret_key
        self._key_id = key_id
        self._team_id = team_id
        self._alg = 'ES256'  # encryption algo that Apple requires
        self.token_str = ""  # encrypted api token
        self.session_length = session_length
        self.token_valid_until = None
        self.generate_token(session_length)
        self.root = 'https://api.music.apple.com/v1/'
        self.max_retries = max_retries
        self.requests_timeout = requests_timeout
        if requests_session:
            self._session = requests.Session()
        else:
            self._session = requests.api  # individual calls, slower

    def token_is_valid(self):
        return datetime.now() <= self.token_valid_until if self.token_valid_until is not None else False

    def generate_token(self, session_length):
        """
        Generate encrypted token to be used by in API requests.
        Set the class token parameter.

        :param session_length: Length Apple Music token is valid, in hours
        """
        token_exp_time = datetime.now() + timedelta(hours=session_length)
        headers = {
            'alg': self._alg,
            'kid': self._key_id
        }
        payload = {
            'iss': self._team_id,  # issuer
            'iat': int(datetime.now().timestamp()),  # issued at
            'exp': int(token_exp_time.timestamp())  # expiration time
        }
        self.token_valid_until = token_exp_time
        token = jwt.encode(payload, self._secret_key, algorithm=self._alg, headers=headers)
        self.token_str = token if type(token) is not bytes else token.decode()


    def _auth_headers(self):
        """
        Get header for API request

        :return: header in dictionary format
        """
        if self.token_str:
            return {'Authorization': 'Bearer {}'.format(self.token_str)}
        else:
            return {}

    def _call(self, method, url, params):
        """
        Make a call to the API

        :param method: 'GET', 'POST', 'DELETE', or 'PUT'
        :param url: URL of API endpoint
        :param params: API paramaters

        :return: JSON data from the API
        """
        if not url.startswith('http'):
            url = self.root + url

        if not self.token_is_valid():
            self.generate_token(self.session_length)

        headers = self._auth_headers()
        headers['Content-Type'] = 'application/json'

        r = self._session.request(method, url,
                                  headers=headers,
                                  proxies=self.proxies,
                                  params=params,
                                  timeout=self.requests_timeout)
        r.raise_for_status()  # Check for error
        return r.json()

    def _get(self, url, **kwargs):
        """
        GET request from the API

        :param url: URL for API endpoint

        :return: JSON data from the API
        """
        retries = self.max_retries
        delay = 1
        while retries > 0:
            try:
                return self._call('GET', url, kwargs)
            except HTTPError as e:  # Retry for some known issues
                retries -= 1
                status = e.response.status_code
                if status == 429 or (500 <= status < 600):
                    if retries < 0:
                        raise
                    else:
                        print('retrying ...' + str(delay) + ' secs')
                        time.sleep(delay + 1)
                        delay += 1
                else:
                    raise
            except Exception as e:
                print('exception', str(e))
                retries -= 1
                if retries >= 0:
                    print('retrying ...' + str(delay) + 'secs')
                    time.sleep(delay + 1)
                    delay += 1
                else:
                    raise

    def _post(self, url, **kwargs):
        return self._call('POST', url, kwargs)

    def _delete(self, url, **kwargs):
        return self._call('DELETE', url, kwargs)

    def _put(self, url, **kwargs):
        return self._call('PUT', url, kwargs)

    def _get_resource(self, resource_id, resource_type, storefront='us', **kwargs):
        """
        Get an Apple Music catalog resource (song, artist, album, etc.)

        :param resource_id: ID of resource, from API
        :param resource_type: Resource type, (e.g. "songs")
        :param storefront: Apple Music Storefront

        :return: JSON data from API
        """
        url = self.root + 'catalog/{0}/{1}/{2}'.format(storefront, resource_type, str(resource_id))
        return self._get(url, **kwargs)

    def _get_resource_relationship(self, resource_id, resource_type, relationship, storefront='us', **kwargs):
        """
        Get an Apple Music catalog resource relationship (e.g. a song's artist)

        :param resource_id: ID of resource
        :param resource_type: Resource type (e.g. "songs")
        :param relationship: Relationship type (e.g. "artists")
        :param storefront: Apple Music Storefont

        :return: JSON data from API
        """
        url = self.root + 'catalog/{0}/{1}/{2}/{3}'.format(storefront, resource_type, str(resource_id),
                                                           relationship)
        return self._get(url, **kwargs)

    def _get_resource_relationship_view(self, resource_id, resource_type, relationship_view, storefront='us', **kwargs):
        """
        Get an Apple Music catalog resource relationship view (e.g. a song's artist)

        :param resource_id: ID of resource
        :param resource_type: Resource type (e.g. "songs")
        :param relationship_view: Relationship view type (e.g. "related-albums")
        :param storefront: Apple Music Storefont

        :return: JSON data from API
        """
        url = self.root + 'catalog/{0}/{1}/{2}/view/{3}'.format(storefront, resource_type, str(resource_id),
                                                                relationship_view)
        return self._get(url, **kwargs)

    def _get_multiple_resources(self, resource_ids, resource_type, storefront='us', **kwargs):
        """
        Get multiple Apple Music catalog resources

        :param resource_ids: List of resource IDs
        :param resource_type: Resource type
        :param storefront: Apple Music storefront

        :return: JSON data from API
        """
        url = self.root + 'catalog/{0}/{1}'.format(storefront, resource_type)
        id_string = ','.join(resource_ids)  # API format is a string with IDs seperated by commas
        return self._get(url, ids=id_string, **kwargs)

    def _get_resource_by_filter(self, filter_type, filter_list, resource_type, resource_ids=None,
                                storefront='us', **kwargs):
        """
        Get mutiple catalog resources using filters

        :param filter_type: Type of filter (e.g. "isrc")
        :param filter_list: List of values to filter on
        :param resource_type: Resource type
        :param resource_ids: List of resource IDs to use in conjunction for additional filtering
        :param storefront: Apple Music storefront

        :return: JSON data from API
        """
        url = self.root + 'catalog/{0}/{1}'.format(storefront, resource_type)
        if resource_ids:
            id_string = ','.join(resource_ids)
        else:
            id_string = None
        filter_string = ','.join(filter_list)
        filter_param = 'filter[{}]'.format(filter_type)
        filter_arg = {filter_param: filter_string}
        kwargs.update(filter_arg)
        results = self._get(url, ids=id_string, **kwargs)
        return results

    # Resources
    def album(self, album_id, storefront='us', l=None, include=None):
        """
        Get a catalog Album by ID

        :param album_id: Album ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Album data in JSON format
        """
        return self._get_resource(album_id, 'albums', storefront=storefront, l=l, include=include)

    def album_relationship(self, album_id, relationship, storefront='us', l=None, limit=None, offset=None):
        """
        Get an Album's relationship (e.g. list of tracks, or list of artists)

        :param album_id: Album ID
        :param relationship: Relationship type (e.g. "artists")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(album_id, 'albums', relationship, storefront=storefront, l=l,
                                               limit=limit, offset=offset)

    def album_relationship_view(self, album_id, relationship_view, storefront='us', l=None, limit=None, offset=None):
        """
        Get an Album's relationship (e.g. list of tracks, or list of artists)

        :param album_id: Album ID
        :param relationship_view: Relationship view type (e.g. "related-albums")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship view data in JSON format
        """
        return self._get_resource_relationship_view(album_id, 'albums', relationship_view, storefront=storefront, l=l,
                                                    limit=limit, offset=offset)

    def albums(self, album_ids, storefront='us', l=None, include=None):
        """
        Get all catalog album data associated with the IDs provided

        :param album_ids: a list of album IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog album data in JSON format
        """
        return self._get_multiple_resources(album_ids, 'albums', storefront=storefront, l=l, include=include)

    def music_video(self, music_video_id, storefront='us', l=None, include=None):
        """
        Get a catalog Music Video by ID

        :param music_video_id: Music Video ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Music Video data in JSON format
        """
        return self._get_resource(music_video_id, 'music-videos', storefront=storefront, l=l, include=include)

    def music_video_relationship(self, music_video_id, relationship, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Music Videos's relationship (e.g. list of artists)

        :param music_video_id: Music Video ID
        :param relationship: Relationship type (e.g. "artists")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(music_video_id, 'music-videos', relationship,
                                               storefront=storefront, l=l, limit=limit, offset=offset)

    def music_video_relationship_view(self, music_video_id, relationship_view,
                                      storefront='us', l=None, limit=None, offset=None):
        """
        Get a Music Videos's relationship view(e.g. list of artists)

        :param music_video_id: Music Video ID
        :param relationship_view: Relationship view type (e.g. "more-by-artist")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship view data in JSON format
        """
        return self._get_resource_relationship_view(music_video_id, 'music-videos', relationship_view,
                                                    storefront=storefront, l=l, limit=limit, offset=offset)

    def music_videos(self, music_video_ids, storefront='us', l=None, include=None):
        """
        Get all catalog music video data associated with the IDs provided

        :param music_video_ids: a list of music video IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog music video data in JSON format
        """
        return self._get_multiple_resources(music_video_ids, 'music-videos', storefront=storefront, l=l,
                                            include=include)

    def music_videos_by_isrc(self, isrcs, music_video_ids=None, storefront='us', l=None, include=None):
        """
        Get all catalog music videos associated with the ISRCs provided

        :param isrcs: list of ISRCs
        :param music_video_ids: IDs of music videos for additional filtering in conjunction with ISRC
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog music video data in JSON format
        """
        return self._get_resource_by_filter('isrc', isrcs, 'music-videos', resource_ids=music_video_ids,
                                            storefront=storefront, l=l, include=include)

    def playlist(self, playlist_id, storefront='us', l=None, include=None):
        """
        Get a catalog Playlist by ID

        :param playlist_id: Playlist ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Playlist data in JSON format
        """
        return self._get_resource(playlist_id, 'playlists', storefront=storefront, l=l, include=include)

    def playlist_relationship(self, playlist_id, relationship, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Playlists's relationship (e.g. list of tracks)

        :param playlist_id: Playlist ID
        :param relationship: Relationship type (e.g. "tracks")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(playlist_id, 'playlists', relationship, storefront=storefront,
                                               l=l, limit=limit, offset=offset)

    def playlist_relationship_view(self, playlist_id, relationship_view, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Playlists's relationship view(e.g. list of tracks)

        :param playlist_id: Playlist ID
        :param relationship: Relationship view type (e.g. "featured-artists")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship view data in JSON format
        """
        return self._get_resource_relationship_view(playlist_id, 'playlists', relationship_view, storefront=storefront,
                                                    l=l, limit=limit, offset=offset)

    def playlists(self, playlist_ids, storefront='us', l=None, include=None):
        """
        Get all catalog album data associated with the IDs provided

        :param playlist_ids: a list of playlist IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog playlist data in JSON format
        """
        return self._get_multiple_resources(playlist_ids, 'playlists', storefront=storefront, l=l,
                                            include=include)

    def song(self, song_id, storefront='us', l=None, include=None):
        """
        Get a catalog Song by ID

        :param song_id: Song ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Song data in JSON format
        """
        return self._get_resource(song_id, 'songs', storefront=storefront, l=l, include=include)

    def song_relationship(self, song_id, relationship, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Song's relationship (e.g. artist)

        :param song_id: Song ID
        :param relationship: Relationship type (e.g. "artists")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(song_id, 'songs', relationship, storefront=storefront, l=l,
                                               limit=limit, offset=offset)

    def songs(self, song_ids, storefront='us', l=None, include=None):
        """
        Get all catalog song data associated with the IDs provided

        :param song_ids: a list of song IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog song data in JSON format
        """
        return self._get_multiple_resources(song_ids, 'songs', storefront=storefront, l=l, include=include)

    def songs_by_isrc(self, isrcs, song_ids=None, storefront='us', l=None, include=None):
        """
        Get all catalog songs associated with the ISRCs provided

        :param isrcs: list of ISRCs
        :param song_ids: IDs of songs for additional filtering in conjunction with ISRC
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog song data in JSON format
        """
        return self._get_resource_by_filter('isrc', isrcs, 'songs', resource_ids=song_ids,
                                            storefront=storefront, l=l, include=include)

    def artist(self, artist_id, storefront='us', l=None, include=None):
        """
        Get a catalog Artist by ID

        :param artist_id: Artist ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Artist data in JSON format
        """
        return self._get_resource(artist_id, 'artists', storefront=storefront, l=l, include=include)

    def artist_relationship(self, artist_id, relationship, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Artist's relationship (e.g. song)

        :param artist_id: Artist ID
        :param relationship: Relationship type (e.g. "songs")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(artist_id, 'artists', relationship, storefront=storefront,
                                               l=l, limit=limit, offset=offset)

    def artist_relationship_view(self, artist_id, relationship_view, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Artist's relationship (e.g. song)

        :param artist_id: Artist ID
        :param relationship_view: Relationship view type (e.g. "top-songs")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship_view(artist_id, 'artists', relationship_view, storefront=storefront,
                                                    l=l, limit=limit, offset=offset)

    def artists(self, artist_ids, storefront='us', l=None, include=None):
        """
        Get all catalog artist data associated with the IDs provided

        :param artist_ids: a list of artist IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog artist data in JSON format
        """
        return self._get_multiple_resources(artist_ids, 'artists', storefront=storefront, l=l, include=include)

    def station(self, station_id, storefront='us', l=None, include=None):
        """
        Get a catalog Station by ID

        :param station_id: Station ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Station data in JSON format
        """
        return self._get_resource(station_id, 'stations', storefront=storefront, l=l, include=include)

    def stations(self, station_ids, storefront='us', l=None, include=None):
        """
        Get all catalog station data associated with the IDs provided

        :param station_ids: a list of station IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog station data in JSON format
        """
        return self._get_multiple_resources(station_ids, 'stations', storefront=storefront,
                                            l=l, include=include)

    def curator(self, curator_id, storefront='us', l=None, include=None):
        """
        Get a catalog Curator by ID

        :param curator_id: Curator ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Curator data in JSON format
        """
        return self._get_resource(curator_id, 'curators', storefront=storefront, l=l, include=include)

    def curator_relationship(self, curator_id, relationship, storefront='us', l=None, limit=None, offset=None):
        """
        Get a Curator's relationship (e.g. playlists)

        :param curator_id: Curator ID
        :param relationship: Relationship type (e.g. "playlists")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(curator_id, 'curators', relationship, storefront=storefront,
                                               l=l, limit=limit, offset=offset)

    def curators(self, curator_ids, storefront='us', l=None, include=None):
        """
        Get all curator album data associated with the IDs provided

        :param curator_ids: a list of curator IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog curator data in JSON format
        """
        return self._get_multiple_resources(curator_ids, 'curators', storefront=storefront, l=l,
                                            include=include)

    def activity(self, activity_id, storefront='us', l=None, include=None):
        """
        Get a catalog Activity by ID

        :param activity_id: Activity ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Activity data in JSON format
        """
        return self._get_resource(activity_id, 'activities', storefront=storefront, l=l, include=include)

    def activity_relationship(self, activity_id, relationship, storefront='us', limit=None, offset=None):
        """
        Get an Activity's relationship (e.g. playlists)

        :param activity_id: Activity ID
        :param relationship: Relationship type (e.g. "playlists")
        :param storefront: Apple Music store front
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(activity_id, 'activities', relationship, storefront=storefront,
                                               limit=limit, offset=offset)

    def activities(self, activity_ids, storefront='us', l=None, include=None):
        """
        Get all catalog activity data associated with the IDs provided

        :param activity_ids: a list of activity IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog activity data in JSON format
        """
        return self._get_multiple_resources(activity_ids, 'activities', storefront=storefront, l=l,
                                            include=include)

    def apple_curator(self, apple_curator_id, storefront='us', l=None, include=None):
        """
        Get a catalog Apple Curator by ID

        :param apple_curator_id: Apple Curator ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: Apple Curator data in JSON format
        """
        return self._get_resource(apple_curator_id, 'apple-curators', storefront=storefront, l=l,
                                  include=include)

    def apple_curator_relationship(self, apple_curator_id, relationship, storefront='us', l=None, limit=None,
                                   offset=None):
        """
        Get an Apple Curator's relationship (e.g. playlists)

        :param apple_curator_id: Apple Curator ID
        :param relationship: Relationship type (e.g. "playlists")
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A List of relationship data in JSON format
        """
        return self._get_resource_relationship(apple_curator_id, 'apple-curators', relationship,
                                               storefront=storefront, l=l, limit=limit, offset=offset)

    def apple_curators(self, apple_curator_ids, storefront='us', l=None, include=None):
        """
        Get all catalog apple curator data associated with the IDs provided

        :param apple_curator_ids: a list of apple curator IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param include: Additional relationships to include in the fetch. Check API documentation.

        :return: A list of catalog apple curator data in JSON format
        """
        return self._get_multiple_resources(apple_curator_ids, 'apple-curators', storefront=storefront, l=l,
                                            include=include)

    def genre(self, genre_id, storefront='us', l=None):
        """
        Get a catalog Genre by ID

        :param genre_id: Genre ID
        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.

        :return: Genre data in JSON format
        """
        return self._get_resource(genre_id, 'genres', storefront=storefront, l=l)

    # THIS IS LISTED IN APPLE API, BUT DOESN'T SEEM TO WORK
    # def genre_relationship(self, genre_id, relationship, storefront='us', l=None, limit=None, offset=None):
    #     return self._get_resource_relationship(genre_id, 'genres', relationship, storefront=storefront,
    #                                            l=l, limit=limit, offset=offset)

    def genres(self, genre_ids, storefront='us', l=None):
        """
        Get all catalog genre data associated with the IDs provided

        :param genre_ids: a list of genre IDs
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.

        :return: A list of catalog genre data in JSON format
        """
        return self._get_multiple_resources(genre_ids, 'genres', storefront=storefront, l=l)

    def genres_all(self, storefront='us', l=None, limit=None, offset=None):
        """
        Get all genres

        :param storefront: Apple Music Storefront
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A list of genre data in JSON format
        """
        url = self.root + 'catalog/{}/genres'.format(storefront)
        return self._get(url, l=l, limit=limit, offset=offset)

    # Storefronts
    def storefront(self, storefront_id, l=None):
        """
        Get a Storefront by ID

        :param storefront_id: Storefont ID
        :param l: The localization to use, specified by a language tag. Check API documentation.

        :return: Storefront data in JSON format
        """
        url = self.root + 'storefronts/{}'.format(storefront_id)
        return self._get(url, l=l)

    def storefronts(self, storefront_ids, l=None):
        """
        Get all storefront data associated with the IDs provided

        :param storefront_ids: a list of storefront IDs
        :param l: The localization to use, specified by a language tag. Check API documentation.

        :return: A list of storefront data in JSON format
        """
        url = self.root + 'storefronts'
        id_string = ','.join(storefront_ids)
        return self._get(url, ids=id_string, l=l)

    def storefronts_all(self, l=None, limit=None, offset=None):
        """
        Get all storefronts

        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A list of storefront data in JSON format
        """
        url = self.root + 'storefronts'
        return self._get(url, l=l, limit=limit, offset=offset)

    # Search
    def search(self, term, storefront='us', l=None, limit=None, offset=None, types=None, hints=False, os='linux'):
        """
        Query the Apple Music API based on a search term

        :param term: Search term
        :param storefront: Apple Music store front
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned
        :param types: A list of resource types to return (e.g. songs, artists, etc.)
        :param hints: Include search hints
        :param os: Operating System being used. If search isn't working on Windows, try os='windows'.

        :return: The search results in JSON format
        """
        url = self.root + 'catalog/{}/search'.format(storefront)
        if hints:
            url += '/hints'
        term = re.sub(' +', '+', term)
        if types:
            type_str = ','.join(types)
        else:
            type_str = None

        if os == 'linux':
            return self._get(url, term=term, l=l, limit=limit, offset=offset, types=type_str)
        elif os == 'windows':
            params = {
                'term': term,
                'limit': limit,
                'offset': offset,
                'types': type_str
            }

            # The params parameter in requests converts '+' to '%2b'
            # On some Windows computers, this breaks the API request, so generate full URL instead
            param_string = '?'
            for param, value in params.items():
                if value is None:
                    continue
                param_string = param_string + str(param) + '=' + str(value) + '&'
            param_string = param_string[:len(param_string) - 1]  # This removes the last trailing '&'

            return self._get(url + param_string)
        else:
            return None



    # Charts
    def charts(self, storefront='us', chart=None, types=None, l=None, genre=None, limit=None, offset=None):
        """
        Get Apple Music Chart data

        :param storefront: Apple Music store front
        :param chart: Chart ID
        :param types: List of resource types (e.g. songs, albums, etc.)
        :param l: The localization to use, specified by a language tag. Check API documentation.
        :param genre: The genre of the chart
        :param limit: The maximum amount of items to return
        :param offset: The index of the first item returned

        :return: A list of chart data in JSON format
        """
        url = self.root + 'catalog/{}/charts'.format(storefront)
        if types:
            type_str = ','.join(types)
        else:
            type_str = None
        return self._get(url, types=type_str, chart=chart, l=l, genre=genre, limit=limit, offset=offset)
