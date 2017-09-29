import csv
import musicbrainzngs as mb
import requests
import pylast

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.conf import settings

from .models import Album, Artist, Song, Tag

spotifycharts = "https://spotifycharts.com/regional/global/daily/latest/download"
STREAMS_INPUT = settings.APP_STREAMS_CSV
mb.set_useragent('songs', '1.0', 'http://example.com')
network = pylast.LastFMNetwork(
    api_key=settings.LF_API_KEY, api_secret=settings.LF_API_SECRET,
    username=settings.LF_API_USERNAME,
    password_hash=pylast.md5(settings.LF_API_PASSWORD))


def request_stream_list():
    # save csv file
    r = requests.get(spotifycharts)
    if r.status_code == 200:
        with open(STREAMS_INPUT, 'w') as f:
            f.write(r.text)


def insert_from_csv():
    with open(STREAMS_INPUT, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            artist, _ = Artist.objects.get_or_create(
                name=row['Artist']
            )
            Song.objects.get_or_create(
                title=row['Track Name'],
                stream_count=row['Streams'],
                artist=artist
            )

def get_info_from_musicbrainz():
    for artist in Artist.objects.all():
        results = {}
        try:
            results = mb.search_artists(artist.name)
        except Exception as e:
            print e
        else:
            if results['artist-count'] > 0:
                # get the result with the highest lucene score
                result = max(
                        results['artist-list'],
                        key=lambda x: int(x['ext:score']))
                artist.gender = result.get('gender', '')
                artist.disambiguation = result.get('disambiguation', '')
                area = result.get('area', '')
                if area and 'name' in area:
                    artist.area = area['name']
                # tags = result.get('tag-list', [])
                # @NOTE what to do with tags
                artist.save()


def get_info_from_last_fm():
    for song in Song.objects.all():
        track = network.get_track(song.artist.name, song.title)
        if track:
            l_duration = track.get_duration()
            l_listener_count = track.get_listener_count()
            l_play_count = track.get_playcount()
            song.duration = l_duration
            song.listener_count = l_listener_count
            song.play_count = l_play_count

            try:
                l_album = track.get_album()
                album, _ = Album.objects.get_or_create(
                    title=l_album.title)
                if album:
                    album.release_date = l_album.get_release_date()
                    album.listener_count = l_album.get_listener_count()
                    album.play_count = l_album.get_playcount()
            except Exception as e:
                print e
            else:
                album.save()
                song.album = album
            song.save()

        l_artist = network.get_artist(song.artist.name)
        if l_artist:
            song.artist.bio = str(l_artist.get_bio_summary())
            song.artist.listener_count = l_artist.get_listener_count()
            song.artist.play_count = l_artist.get_playcount()
            song.artist.save()


def get_music():
    request_stream_list()
    insert_from_csv()
    get_info_from_musicbrainz()
    get_info_from_last_fm()


if __name__ == '__main__':
    main()
