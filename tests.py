from applemusicpy import AppleMusic
import unittest


class TestApple(unittest.TestCase):

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
        # activity
        self.party = '976439514'
        self.chill = '976439503'
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
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Born To Run')

    def test_album_relationship(self):
        results = am.album_relationship(self.born_to_run, 'artists')
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Bruce Springsteen')

    def test_albums(self):
        results = am.albums([self.born_to_run, self.ready_to_die])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'albums')

    def test_music_video(self):
        results = am.music_video(self.rubber_soul)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Rubber Soul (Documentary)')

    def test_music_video_relationship(self):
        results = am.music_video_relationship(self.rubber_soul, 'artists')
        self.assertTrue(results['data'][0]['attributes']['name'] == 'The Beatles')

    def test_music_videos(self):
        results = am.music_videos([self.rubber_soul, self.sgt_pepper])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'music-videos')

    # ISRCs don't seem to work for music videos
    # def test_music_videos_by_isrc(self):

    def test_playlist(self):
        results = am.playlist(self.janet_jackson)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Janet Jackson: No.1 Songs')

    def test_playlist_relationship(self):
        results = am.playlist_relationship(self.eighties_pop, 'tracks')  # playlist have 'tracks', artists have 'songs'
        self.assertTrue(results['data'][0]['type'] == 'songs')

    def test_playlists(self):
        results = am.playlists([self.janet_jackson, self.eighties_pop])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'playlists')

    def test_song(self):
        results = am.song(self.xo_tour_life)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'XO TOUR Llif3')

    def test_song_relationship(self):
        results = am.song_relationship(self.xo_tour_life, 'artists')
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Lil Uzi Vert')

    def test_songs(self):
        results = am.songs([self.xo_tour_life, self.new_patek])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'songs')

    def test_songs_by_isrc(self):
        results = am.songs_by_isrc([self.gods_plan_isrc])
        self.assertTrue(results['data'][0]['attributes']['name'] == 'God\'s Plan')

    def test_artist(self):
        results = am.artist(self.lil_pump)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Lil Pump')

    def test_artist_relationship(self):
        results = am.artist_relationship(self.lil_pump, 'songs')
        self.assertTrue(results['data'][0]['type'] == 'songs')

    def test_artists(self):
        results = am.artists([self.lil_pump, self.smokepurpp])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'artists')

    def test_station(self):
        results = am.station(self.alt)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Alternative')

    def test_stations(self):
        results = am.stations([self.alt, self.pure_pop])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'stations')

    def test_curator(self):
        results = am.curator(self.large_up)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'LargeUp')

    def test_curator_relationship(self):
        results = am.curator_relationship(self.grand_ole_opry, 'playlists')
        self.assertTrue(results['data'][0]['type'] == 'playlists')

    def test_curators(self):
        results = am.curators([self.large_up, self.grand_ole_opry])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'curators')

    def test_activity(self):
        results = am.activity(self.party)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Party')

    def test_activity_relationship(self):
        results = am.activity_relationship(self.party, 'playlists')
        self.assertTrue(results['data'][0]['type'] == 'playlists')

    def test_activities(self):
        results = am.activities([self.party, self.chill])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'activities')

    def test_apple_curator(self):
        results = am.apple_curator(self.apple_alt)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Apple Music Alternative')

    def test_apple_curator_relationship(self):
        results = am.apple_curator_relationship(self.apple_alt, 'playlists')
        self.assertTrue(results['data'][0]['type'] == 'playlists')

    def test_apple_curators(self):
        results = am.apple_curators([self.apple_alt, self.live_nation_tv])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'apple-curators')

    def test_genre(self):
        results = am.genre(self.pop)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'Pop')

    def test_genres(self):
        results = am.genres([self.pop, self.rock])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'genres')

    def test_genres_all(self):
        results = am.genres_all()
        self.assertTrue(results['data'][0]['id'] == '34')

    def test_storefront(self):
        results = am.storefront(self.us)
        self.assertTrue(results['data'][0]['attributes']['name'] == 'United States')

    def test_storefronts(self):
        results = am.storefronts([self.us, self.jp])
        self.assertTrue(len(results['data']) == 2)
        self.assertTrue(results['data'][0]['type'] == 'storefronts')

    def test_storefronts_all(self):
        results = am.storefronts_all()
        self.assertTrue(results['data'][0]['id'] == 'dz')

    def test_search(self):
        results = am.search(self.search_term, types=['songs'])
        self.assertTrue(results['results']['songs']['data'][0]['attributes']['name'] == 'Nice For What')

    def test_search_windows(self):
        results = am.search(self.search_term, types=['songs'], os='windows')
        self.assertTrue(results['results']['songs']['data'][0]['attributes']['name'] == 'Nice For What')

    def test_charts(self):
        results = am.charts(types=['songs'], genre=self.pop)
        self.assertTrue(results['results']['songs'][0]['name'] == 'Top Songs')


if __name__ == '__main__':
    # These tests require API authorization, so need to read in keys
    keys = {}

    with open('private_key.p8', 'r') as f:
        keys['secret'] = f.read()

    with open('keys.txt') as f:
        for line in f:
            name, val = line.partition('=')[::2]
            keys[name.strip()] = val.strip()

    am = AppleMusic(secret_key=keys['secret'], key_id=keys['keyID'], team_id=keys['teamID'])

    unittest.main()
