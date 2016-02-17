#!/usr/bin/env python3
# z@xnz.me
import argparse, configparser, zipfile, subprocess, os, pafy


def main():

    # Config
    if not os.path.isfile('config.ini'):
        print('config.ini not found, please create one.')
        return 1

    config = configparser.ConfigParser()

    config.read('config.ini')

    site_url = config['default']['site_url']
    endpoint_file = config['default']['endpoint_file']
    package_path = config['default']['package_path']
    cache_path = config['default']['cache_path']

    # Parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("youtube_url", help="A youtube video URL",
                        type=str)
    args = parser.parse_args()

    # Setup vars
    youtube_url = args.youtube_url
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
    
    music_file = bestaudio.download(cache_path)

    ogg_file = cache_path + video.videoid + '.ogg'
    pk3_file = 'yt-' + video.videoid + '.pk3'

    # Convert whatever (hopefully m4a) to ogg -- this part is the most likely to break
    with open(music_file, 'r') as f:
        print('converting to ogg...')
        #subprocess.call(["ffmpeg", '-i', music_file, '-acodec', 'vorbis', '-strict', '-2', '-aq', '60', '-vn', '-ac', '2', cache_path + ogg_file])
        subprocess.call(['avconv', '-i', music_file, '-codec:a', 'libvorbis', '-qscale:a', '5', ogg_file])

    # Create a zip with the ogg inside of it
    with zipfile.ZipFile(package_path + pk3_file, 'w') as myzip:
        print('creating zip...')
        myzip.write(ogg_file, os.path.basename(ogg_file))
        myzip.close()

    # Write the meta info to the endpoint
    with open(endpoint_file, 'w') as f:
        print('writing endpoint file...')
        f.write(site_url + pk3_file + " " + str(duration) + " " + video.title)
        f.close()

    print('done.')

if __name__ == "__main__":
    main()

