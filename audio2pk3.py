#!/usr/bin/env python3
# z@xnz.me
import argparse
import re
import uuid
from xonotic_radio.objects import Track
from xonotic_radio.util import *


def main():

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


def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--target', '-t', nargs='?', help="target endpoint defined under [endpoints] in config", type=str)
    parser.add_argument('--name', '-n', nargs='?', help="name your download", type=str)

    parser.add_argument("input_source", help="A URL of a youtube video, a remote audio file or local a audio file", type=str)
    parser.add_argument('title', nargs='?', help='title for the audio file', type=str)

    return parser.parse_args()


if __name__ == "__main__":
    main()
