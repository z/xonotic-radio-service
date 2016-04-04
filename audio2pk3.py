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


conf = {}
endpoints = {}


def main():

    global conf

    conf, endpoints = read_config('config/config.ini')
    args = parse_args()

    if args.target:
        if args.target in endpoints:
            target = endpoints[args.target]
        else:
            print('target doesn\'t exist')
            raise SystemExit
    else:
        target = endpoints['default']

    input_source = args.input_source

    if re.match('^http(s)?://(www\.|m\.)?(youtube\.com|youtu\.be)/.*', input_source):
        yt_info = get_audio_from_youtube(input_source)

        output_music_file = yt_info['music_file']
        duration = yt_info['duration']
        video = yt_info['video']
        name = video.videoid
        if args.title:
            title = args.title
        else:
            title = video.title
    else:

        if not args.title:
            print('title is required as a second parameter')
            raise SystemExit
        else:
            title = args.title

        extension = str(os.path.splitext(input_source)[1])
        name = str(uuid.uuid1())
        local_name = name + "_d"
        output_music_file = conf['cache_path'] + local_name + extension

        if re.match('^http(s)?://.*', input_source):
            urllib.request.urlretrieve(input_source, output_music_file, reporthook)
        else:
            copyfile(input_source, output_music_file)

        element = mutagen.File(output_music_file)

        if element:
            duration = "{0:.2f}".format(element.info.length)
        else:
            print('Invalid audio file.')
            raise SystemExit

    ogg_file = convert_to_ogg(output_music_file, name)

    pk3_file = create_pk3(ogg_file, name)

    write_to_endpoint_list(target, pk3_file, ogg_file, duration, title)

    print('done.')


def get_audio_from_youtube(youtube_url):

    global conf

    video = pafy.new(youtube_url)
    formatted_duration = video.duration

    ftr = [3600, 60, 1]

    duration = sum([a*b for a,b in zip(ftr, map(int,formatted_duration.split(':')))])

    print("processing: " + youtube_url)
    print("title: " + video.title)
    print("duration: " + formatted_duration)

    print("Available audio streams:")

    audiostreams = video.audiostreams

    for a in audiostreams:
        print(a.bitrate, a.extension, a.get_filesize())

    bestaudio = video.getbestaudio()
    
    music_file = bestaudio.download(conf['cache_path'])

    return {'music_file': music_file, 'video': video, 'duration': duration}


def convert_to_ogg(music_file, name):

    global conf

    ogg_file = name + '.ogg'

    # Convert whatever (hopefully m4a) to ogg -- this part is the most likely to break
    with open(music_file, 'r') as f:
        print('converting to ogg...')

        if conf['encoding_driver'] == 'avconv':
            subprocess.call(['avconv', '-i', music_file, '-codec:a', 'libvorbis', '-b:a', conf['bitrate'], '-vn', conf['cache_path'] + ogg_file])
        elif conf['encoding_driver'] == 'ffmpeg':
            subprocess.call(["ffmpeg", '-i', music_file, '-codec:a', 'libvorbis', '-b:a', conf['bitrate'], '-vn', conf['cache_path'] + ogg_file])
        else:
            print('/!\ No valid driver was chosen, please configure either avconv or ffmpeg. Exiting...')
            raise SystemExit

    return ogg_file


def create_pk3(ogg_file, name):

    global conf

    pk3_file = conf['package_prefix'] + name + '.pk3'

    # Create a zip with the ogg inside of it
    with zipfile.ZipFile(conf['package_path'] + pk3_file, 'w') as pk3:
        print('creating zip...')
        pk3.write(conf['cache_path'] + ogg_file, os.path.basename(ogg_file))
        pk3.close()

        return pk3_file


def write_to_endpoint_list(target, pk3_file, ogg_file, duration, title):

    global conf

    with open(target, 'a') as f:
        print('writing to endpoint list file...')
        f.write(conf['site_url'] + pk3_file + ' ' + ogg_file + ' ' + str(duration) + ' ' + title + '\n')
        f.close()


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
        print(config_file + ' not found, please create one.')
        raise SystemExit

    config = configparser.ConfigParser()

    config.read(config_file)

    return config['default'], config['endpoints']


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--target', '-t', nargs='?', help="target endpoint defined under [endpoints] in config", type=str)

    parser.add_argument("input_source", help="A URL of a youtube video, a remote audio file or local a audio file", type=str)
    parser.add_argument('title', nargs='?', help='title for the audio file', type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()
