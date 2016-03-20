#!/usr/bin/env python3
# z@xnz.me
import argparse
import configparser
import zipfile
import subprocess
import os
import pafy


conf = {}


def main():

    global conf

    conf = read_config('config/config.ini')
    args = parse_args()

    yt_info = get_audio_from_youtube(args.youtube_url)
    
    music_file = yt_info['music_file']
    duration = yt_info['duration']
    video = yt_info['video']
    name = video.videoid
    title = video.title

    ogg_file = convert_to_ogg(music_file, name)

    pk3_file = create_pk3(ogg_file, name)

    if conf['use_endpoint_file'] == 'True':
        write_to_endpoint(pk3_file, ogg_file, duration, title)

    if conf['use_endpoint_list_file'] == 'True':
        write_to_endpoint_list(pk3_file, ogg_file, duration, title)

    print('done.')


def get_audio_from_youtube(youtube_url):

    global conf

    video = pafy.new(youtube_url)
    formatted_duration = video.duration

    ftr = [3600,60,1]

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

    return { 'music_file': music_file, 'video': video, 'duration': duration }


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
            return 1

    return ogg_file


def create_pk3(ogg_file, name):

    global conf

    pk3_file = 'yt-' + name + '.pk3'

    # Create a zip with the ogg inside of it
    with zipfile.ZipFile(conf['package_path'] + pk3_file, 'w') as pk3:
        print('creating zip...')
        pk3.write(conf['cache_path'] + ogg_file, os.path.basename(ogg_file))
        pk3.close()

        return pk3_file


def write_to_endpoint(pk3_file, ogg_file, duration, title):

    global conf

    with open(conf['endpoint_file'], 'w') as f:
        print('writing endpoint file...')
        f.write(conf['site_url'] + pk3_file + ' ' + ogg_file + ' ' + str(duration) + ' ' + title)
        f.close()


def write_to_endpoint_list(pk3_file, ogg_file, duration, title):

    global conf

    with open(conf['endpoint_list_file'], 'a') as f:
        print('writing to endpoint list file...')
        f.write(conf['site_url'] + pk3_file + ' ' + ogg_file + ' ' + str(duration) + ' ' + title + '\n')
        f.close()


def read_config(config_file):

    if not os.path.isfile(config_file):
        print(config_file + ' not found, please create one.')
        return 1

    config = configparser.ConfigParser()

    config.read(config_file)

    return config['default']


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("youtube_url", help="A youtube video URL",
                        type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()

