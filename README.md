# xonotic-radio-service

Given a youtube video URL or an audio file URL, the audio will be transcoded to ogg, packaged as a pk3 and an endpoint generated.

## Setup

#### System Requirements

```
avconv or ffmpeg (fallback)
```

On Debian based systems avconv can be installed with the following:

```
sudo apt-get install libav-tools
```


#### Setup local packages

Clone from git

```bash
git clone https://github.com/z/xonotic-radio-service.git
```

Setup a venv and install the requirements

```bash
virtualenv -p /usr/bin/python3 venv
ln -s venv/bin/activate
source activate
pip install -r requirements.txt
```

## Configuration

Copy `example.config.ini` and edit `config.ini` to your server settings:

```bash
cp config/example.config.ini config/config.ini
```

The file should contain something similar to the following:

```ini
[default]
# URL for where the radio pk3s live
site_url = http://example.com/radio/

# Prefix for the generated pk3 file
package_prefix = radio-

# absolute or relative path to where the packages live
package_path = packages/

# absolute or relative path for cached media files
cache_path = cache/

# what to use to convert the audio format to ogg
encoding_driver = avconv

# what bitrate for the audio
bitrate = 64k

[endpoints]
default = web/default_list.txt
minsta = web/minsta_list.txt
```

Paths can be either absolute or relative. It would be good practice to have this live in a non-web accessible, but allow it to write the packages to a web facing folder.

## Usage

Make sure audio2pk3.py is executable, `chmod +x audio2pk3.py`, then run it as follows:


Minimal for a youtube video:

```bash
./audio2pk3.py https://www.youtube.com/watch?v=dz24DgBUQbc
```


Target an endpoint defined in config for a youtube video:

```bash
./audio2pk3.py -t minsta https://www.youtube.com/watch?v=dz24DgBUQbc
```

Target an endpoint defined in config for a youtube video and give it a title:

```bash
./audio2pk3.py -t minsta https://www.youtube.com/watch?v=dz24DgBUQbc "[SMB] Excision and﻿ Datsik - Guess I Got My Swagger Back"
```

If downloading an audio file from any site, you must specify a title:
```bash
./audio2pk3.py https://dl.dropboxusercontent.com/u/xxxxxxxx/land.ogg "Super Mario Bros. Overworld Remix"
```


If using a local audio file, you must specify a title:
```bash
./audio2pk3.py my_cool_song.mp3 "Super Mario Bros. Overworld Remix"
```

endpoint_list.txt output:

```
http://example.com/radio/radio-5wkC8vWbFm8.pk3 5wkC8vWbFm8.ogg 420 Mord Fustang - Lick The Rainbow [Electro House | Plasmapool]
http://example.com/radio/radio-08c22c32-f9b9-11e5-a868-94de80b1b7df.pk3 08c22c32-f9b9-11e5-a868-94de80b1b7df.ogg 152.57 Nexuiz - Beast of Insanity
http://example.com/radio/radio-dz24DgBUQbc.pk3 dz24DgBUQbc.ogg 276 Vanic X K.Flay - Make Me Fade
```

Your packages folder should contain a pk3 with an ogg file inside of it that matches a line in endpoint_list.txt

To show a random line from a list whenever a request to the endpoint is made, see `endpoint.php` as an example.
