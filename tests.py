from applemusicpy import AppleMusic
import unittest, os

class UserTests(unittest.TestCase):
    def setUp(self):
        # albums
        self.born_to_run = '310730204'
        self.ready_to_die = '204669326'
        # songs
        self.xo_tour_life = '1274153124'
        self.new_patek = '1436530704'
        # artists
        self.lil_pump = '1129587661'
        self.smokepurpp = '1122104172'

    def test_album_retrieve(self):
        albums = am.current_user_saved_albums()
        self.assertIsNotNone(albums)
        # You can add more assertions here based on the expected behavior of the function

    def test_playlist_retrieve(self):
        playlists = am.current_user_playlists(limit=1)
        self.assertIsNotNone(playlists)
        # You can add more assertions here based on the expected behavior of the function

    def test_song_retrieve(self):
        songs = am.current_user_saved_tracks()
        self.assertIsNotNone(songs)
        # You can add more assertions here based on the expected behavior of the function

    def test_artist_retrieve(self):
        artists = am.current_user_followed_artists()
        self.assertIsNotNone(artists)
        # You can add more assertions here based on the expected behavior of the function

    def test_album_set(self):
        album_id = self.born_to_run
        response = am.current_user_saved_albums_add(album_id)
        self.assertTrue(response)  # Check if the album was added successfully
        # You can add more assertions here based on the expected behavior of the function

    def test_playlist_create(self):
        playlist_name = "Test Playlist"
        description = "apple-music-python test playlist!"
        tracks = self.xo_tour_life, self.new_patek  # Replace with actual track IDs
        response = am.user_playlist_create(playlist_name=playlist_name, tracks=tracks, description=description)
        self.assertTrue(response)  # Check if the playlist was added successfully
        # You can add more assertions here based on the expected behavior of the function

    def test_song_set(self):
        song_id = self.xo_tour_life
        response = am.current_user_saved_tracks_add(song_id)
        self.assertTrue(response)  # Check if the song was added successfully
        # You can add more assertions here based on the expected behavior of the function

    # It doesn't seem like you can like an artist through the API. (Maybe through MusicKit?)
    #def test_artist_set(self):
    #    artist_id = self.smokepurpp
    #    response = am.current_user_followed_artists_add(artist_id)
    #    self.assertTrue(response)  # Check if the artist was added successfully
    #    # You can add more assertions here based on the expected behavior of the function
    
class BaseTests(unittest.TestCase):

    def setUp(self):
        # albums
        self.born_to_run = '310730204'
        self.ready_to_die = '204669326'
        # music videos
        self.rubber_soul = '401135199'
        self.sgt_pepper = '401147268'
        # ISRC
        self.gods_plan_isrc = 'USCM51800004'
        # playlists
        self.janet_jackson = 'pl.acc464c750b94302b8806e5fcbe56e17'
        self.eighties_pop = 'pl.97c6f95b0b884bedbcce117f9ea5d54b'
        # songs
        self.xo_tour_life = '1274153124'
        self.new_patek = '1436530704'
        # artists
        self.lil_pump = '1129587661'
        self.smokepurpp = '1122104172'
        # stations
        self.alt = 'ra.985484166'
        self.pure_pop = 'ra.686227433'
        # curators
        self.large_up = '1107687517'
        self.grand_ole_opry = '976439448'
        # apple curators
        self.apple_alt = '976439526'
        self.live_nation_tv = '1017168810'
        # genres
        self.pop = '14'
        self.rock = '21'
        # storefronts
        self.us = 'us'
        self.jp = 'jp'
        # search
        self.search_term = 'nice for what'

    def test_album(self):
        results = am.album(self.born_to_run)
        expected_name = 'Born to Run'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_album_relationship(self):
        results = am.album_relationship(self.born_to_run, 'artists')
        expected_name = 'Bruce Springsteen'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_albums(self):
        results = am.albums([self.born_to_run, self.ready_to_die])
        expected_count = 2
        expected_type = 'albums'
        actual_count = len(results['data'])
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_music_video(self):
        results = am.music_video(self.rubber_soul)
        expected_name = 'Rubber Soul (Documentary)'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_music_video_relationship(self):
        results = am.music_video_relationship(self.rubber_soul, 'artists')
        expected_name = 'The Beatles'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_music_videos(self):
        results = am.music_videos([self.rubber_soul, self.sgt_pepper])
        expected_count = 2
        expected_type = 'music-videos'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")
    
    # ISRCs don't seem to work for music videos
    # def test_music_videos_by_isrc(self):

    def test_playlist(self):
        results = am.playlist(self.janet_jackson)
        expected_name = 'Janet Jackson: No.1 Songs'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_playlist_relationship(self):
        results = am.playlist_relationship(self.eighties_pop, 'tracks')  # playlist have 'tracks', artists have 'songs'
        expected_type = 'songs'
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_playlists(self):
        results = am.playlists([self.janet_jackson, self.eighties_pop])
        expected_count = 2
        expected_type = 'playlists'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_song(self):
        results = am.song(self.xo_tour_life)
        expected_name = 'XO TOUR Llif3'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_song_relationship(self):
        results = am.song_relationship(self.xo_tour_life, 'artists')
        expected_name = 'Lil Uzi Vert'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_songs(self):
        results = am.songs([self.xo_tour_life, self.new_patek])
        expected_count = 2
        expected_type = 'songs'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_songs_by_isrc(self):
        results = am.songs_by_isrc([self.gods_plan_isrc])
        expected_name = "God's Plan"
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_artist(self):
        results = am.artist(self.lil_pump)
        expected_name = 'Lil Pump'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_artist_relationship(self):
        results = am.artist_relationship(self.lil_pump, 'songs')
        expected_type = 'songs'
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_artists(self):
        results = am.artists([self.lil_pump, self.smokepurpp])
        expected_count = 2
        expected_type = 'artists'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_station(self):
        results = am.station(self.alt)
        expected_name = 'Alternative Station'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_stations(self):
        results = am.stations([self.alt, self.pure_pop])
        expected_count = 2
        expected_type = 'stations'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_curator(self):
        results = am.curator(self.large_up)
        expected_name = 'LargeUp'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_curator_relationship(self):
        results = am.curator_relationship(self.grand_ole_opry, 'playlists')
        expected_type = 'playlists'
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_curators(self):
        results = am.curators([self.large_up, self.grand_ole_opry])
        expected_count = 2
        expected_type = 'curators'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_apple_curator(self):
        results = am.apple_curator(self.apple_alt)
        expected_name = 'Apple Music Alternative'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_apple_curator_relationship(self):
        results = am.apple_curator_relationship(self.apple_alt, 'playlists')
        expected_type = 'playlists'
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_apple_curators(self):
        results = am.apple_curators([self.apple_alt, self.live_nation_tv])
        expected_count = 2
        expected_type = 'apple-curators'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_genre(self):
        results = am.genre(self.pop)
        expected_name = 'Pop'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_genres(self):
        results = am.genres([self.pop, self.rock])
        expected_count = 2
        expected_type = 'genres'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_genres_all(self):
        results = am.genres_all()
        expected_id = '34'
        actual_id = results['data'][0]['id']
        self.assertTrue(expected_id == actual_id, f"Expected ID: {expected_id}, Actual ID: {actual_id}")

    def test_storefront(self):
        results = am.storefront(self.us)
        expected_name = 'United States'
        actual_name = results['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_storefronts(self):
        results = am.storefronts([self.us, self.jp])
        expected_count = 2
        expected_type = 'storefronts'
        actual_count = len(results['data'])
        actual_type = results['data'][0]['type']
        self.assertTrue(expected_count == actual_count, f"Expected Count: {expected_count}, Actual Count: {actual_count}")
        self.assertTrue(expected_type == actual_type, f"Expected Type: {expected_type}, Actual Type: {actual_type}")

    def test_storefronts_all(self):
        results = am.storefronts_all()
        expected_id = 'dz'
        actual_id = results['data'][0]['id']
        self.assertTrue(expected_id == actual_id, f"Expected ID: {expected_id}, Actual ID: {actual_id}")

    def test_search(self):
        results = am.search(self.search_term, types=['songs'])
        expected_name = 'Nice For What'
        actual_name = results['results']['songs']['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}, Actual Results: {results}")

    def test_search_windows(self):
        results = am.search(self.search_term, types=['songs'], os='windows')
        expected_name = 'Nice For What'
        actual_name = results['results']['songs']['data'][0]['attributes']['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

    def test_charts(self):
        results = am.charts(types=['songs'], genre=self.pop)
        expected_name = 'Top Songs'
        actual_name = results['results']['songs'][0]['name']
        self.assertTrue(expected_name == actual_name, f"Expected: {expected_name}, Actual: {actual_name}")

if __name__ == '__main__':
    # These tests require API authorization, so need to read in keys and user token
    keys = {}

    with open('private_key.p8', 'r') as f:
        keys['secret'] = f.read()

    with open('keys.txt') as f:
        for line in f:
            name, val = line.partition('=')[::2]
            keys[name.strip()] = val.strip()

    test_loader = unittest.TestLoader()

    user_token_file = 'music_user_token.txt'
    if os.path.exists(user_token_file):
        with open(user_token_file, 'r') as f:
            music_user_token = f.read().strip()
            am = AppleMusic(secret_key=keys['secret'], key_id=keys['keyID'], team_id=keys['teamID'], music_user_token=music_user_token)

        print("Running tests with user token...")
        user_test_suite = test_loader.loadTestsFromTestCase(UserTests)
    else:
        print("No music_user_token.txt found. Running normal tests...")
        am = AppleMusic(secret_key=keys['secret'], key_id=keys['keyID'], team_id=keys['teamID'])

    base_test_suite = test_loader.loadTestsFromTestCase(BaseTests)

    all_tests = unittest.TestSuite()
    all_tests.addTests(base_test_suite)
    if 'user_test_suite' in locals():
        all_tests.addTests(user_test_suite)

    unittest.TextTestRunner(verbosity=2).run(all_tests)