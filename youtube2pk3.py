#!/usr/bin/env python3
# z@xnz.me
import argparse, zipfile, subprocess, os, pafy


def main():

    # Config
    site_url = 'http://example.com/radio/'
    endpoint_file = 'endpoint.txt'
    package_path = 'packages/'
    cache_path = 'cache/'

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

    ogg_file = video.videoid + '.ogg'
    pk3_file = 'yt-' + video.videoid + '.pk3'

    # Convert whatever (hopefully m4a) to ogg -- this part is the most likely to break
    with open(music_file, 'r') as f:
        #subprocess.call(["ffmpeg", '-i', music_file, '-acodec', 'vorbis', '-strict', '-2', '-aq', '60', '-vn', '-ac', '2', cache_path + ogg_file])
        subprocess.call(['avconv', '-i', music_file, '-codec:a', 'libvorbis', '-qscale:a', '5', ogg_file])

    # Create a zip with the ogg inside of it
    with zipfile.ZipFile(package_path + pk3_file, 'w') as myzip:
        myzip.write(ogg_file, os.path.basename(ogg_file))
        myzip.close()

    # Write the meta info to the endpoint
    with open(endpoint_file, 'w') as f:
        f.write(site_url + pk3_file + " " + str(duration) + " " + video.title)
        f.close()

if __name__ == "__main__":
    main()

