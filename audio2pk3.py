#!/usr/bin/env python3
# z@xnz.me
import argparse
import configparser
import zipfile
import subprocess
import os
import re
import pafy
import sys
import time
import uuid
import urllib.request
import mutagen
from shutil import copyfile


def main():

    global conf

    conf, endpoints = read_config('config/config.ini')
    args = parse_args()

    if args.target:
        if args.target in endpoints:
            target = endpoints[args.target]
        else:
            raise SystemExit('target doesn\'t exist')
    else:
        target = endpoints['default']

    input_source = args.input_source

    if re.match('^http(s)?://(www\.|m\.)?(youtube\.com|youtu\.be)/.*', input_source):
        track = Track(youtube_url=input_source)
    else:

        if not args.title:
            raise SystemExit('title is required as a second parameter')
        else:
            title = args.title

        if re.match('^http(s)?://.*', input_source):
            track = Track(source_url=input_source, title=title)
        else:
            track = Track(source_file=input_source, title=title)

    if args.name:
        name = args.name
    else:
        name = str(uuid.uuid1())

    track.convert_to_ogg(name)
    track.create_pk3(name)
    track.write_to_endpoint_list(target)

    print('done.')


class Track(object):
    """A rainbow object that can be applied to a string"""

    def __init__(self, pk3_file=None, youtube_url=None, source_url=None, source_file=None, title=None):

        if not youtube_url and title is None:
            raise SystemExit('title required for url or local files')

        self.local_file = None
        self.duration = None
        self.ogg_file = None
        self.pk3_file = None
        self.youtube_url = youtube_url
        self.source_url = source_url
        self.source_file = source_file

        if youtube_url:
            self.get_audio_from_youtube(youtube_url)
        elif source_url:
            self.download_track(source_url)
        elif source_file:
            self.copy_track(source_file)
        else:
            raise SystemExit('youtube_url, source_url or source_file is required!')

        if title:
            self.title = title

    def get_audio_from_youtube(self, youtube_url):

        if not re.match('^http(s)?://(www\.|m\.)?(youtube\.com|youtu\.be)/.*', youtube_url):
            raise SystemExit('URL for youtube did not match pattern.')

        video = pafy.new(youtube_url)
        formatted_duration = video.duration

        ftr = [3600, 60, 1]

        duration = sum([a * b for a, b in zip(ftr, map(int, formatted_duration.split(':')))])

        print("processing: " + youtube_url)
        print("title: " + video.title)
        print("duration: " + formatted_duration)

        print("Available audio streams:")

        audio_streams = video.audiostreams

        for a in audio_streams:
            print(a.bitrate, a.extension, a.get_filesize())

        best_audio = video.getbestaudio()

        music_file = best_audio.download(conf['cache_path'])

        audio_info = {'local_file': music_file, 'video': video, 'duration': duration, 'title': video.title}

        self.youtube_url = youtube_url
        self.local_file = audio_info['local_file']
        self.duration = audio_info['duration']
        self.title = audio_info['title']

        return audio_info

    def download_track(self, source_url):

        extension = str(os.path.splitext(source_url)[1])
        name = str(uuid.uuid1())
        local_name = name + "_d"
        local_file = conf['cache_path'] + local_name + extension

        urllib.request.urlretrieve(source_url, local_file, reporthook)

        duration = self.get_duration(local_file)

        audio_info = {'duration': duration, 'local_file': local_file}

        self.source_url = source_url
        self.local_file = audio_info['local_file']
        self.duration = audio_info['duration']

        return audio_info

    def copy_track(self, source_file):

        extension = str(os.path.splitext(source_file)[1])
        name = str(uuid.uuid1())
        local_name = name + "_d"
        local_file = conf['cache_path'] + local_name + extension

        copyfile(source_file, local_file)

        duration = self.get_duration(source_file)

        audio_info = {'duration': duration, 'local_file': local_file}

        self.local_file = audio_info['local_file']
        self.duration = audio_info['duration']

        return audio_info

    def convert_to_ogg(self, name):

        ogg_file = name + '.ogg'

        # Convert whatever (hopefully m4a) to ogg -- this part is the most likely to break
        with open(self.local_file, 'r') as f:
            print('converting to ogg...')

            if conf['encoding_driver'] == 'avconv' or conf['encoding_driver'] == 'ffmpeg':
                subprocess.call(
                    [conf['encoding_driver'], '-i', self.local_file, '-codec:a', 'libvorbis', '-b:a', conf['bitrate'],
                     '-vn',
                     conf['cache_path'] + ogg_file])
            else:
                raise SystemExit('/!\ No valid driver was chosen, please configure either avconv or ffmpeg. Exiting...')

        self.ogg_file = ogg_file

        return ogg_file

    def create_pk3(self, name):

        pk3_file = conf['package_prefix'] + name + '.pk3'

        # Create a zip with the ogg inside of it
        with zipfile.ZipFile(conf['package_path'] + pk3_file, 'w') as pk3:
            print('creating zip...')
            pk3.write(conf['cache_path'] + self.ogg_file, os.path.basename(self.ogg_file))
            pk3.close()

            self.pk3_file = pk3_file

            return pk3_file

    def write_to_endpoint_list(self, target):

        with open(target, 'a') as f:
            print('writing to endpoint list file...')
            f.write(conf['site_url'] + self.pk3_file + ' ' + self.ogg_file + ' ' + str(self.duration) + ' ' + self.title + '\n')
            f.close()

    @staticmethod
    def get_duration(local_file):

        element = mutagen.File(local_file)

        if element:
            duration = "{0:.2f}".format(element.info.length)
        else:
            raise SystemExit('Invalid audio file.')

        return duration


def reporthook(count, block_size, total_size):

    global start_time

    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed. " %
                    (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


def read_config(config_file):

    if not os.path.isfile(config_file):
        raise SystemExit(config_file + ' not found, please create one.')

    config = configparser.ConfigParser()

    config.read(config_file)

    return config['default'], config['endpoints']


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--target', '-t', nargs='?', help="target endpoint defined under [endpoints] in config", type=str)
    parser.add_argument('--name', '-n', nargs='?', help="name your download", type=str)

    parser.add_argument("input_source", help="A URL of a youtube video, a remote audio file or local a audio file", type=str)
    parser.add_argument('title', nargs='?', help='title for the audio file', type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()
