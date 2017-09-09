# xonotic-radio-service

Given a youtube video URL or an audio file URL, the audio will be transcoded to ogg, packaged as a pk3 and an endpoint generated.  This service was designed to support [modpack radio](https://github.com/MarioSMB/modpack/blob/master/mod/server/radio.qc).

## Setup

#### System Requirements

```
avconv or ffmpeg (fallback)
```

On Debian-based systems avconv can be installed with the following:

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
pip install -r requirements.in
```

## Configuration

Copy `example.config.ini` and edit `config.ini` to your server settings:

```bash
cp config/example.config.ini config/config.ini
```

The file should contain something similar to the following:

```
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

Paths can be either absolute, or relative. It would be good practice to have this repository live in a non-web accessible directory, but allow it to write the packages to a web-readable directory.

## Usage

Make sure `audio2pk3.py` is executable, `chmod +x audio2pk3.py`, then run it as follows:


**Minimal for a youtube video:**

```bash
./audio2pk3.py https://www.youtube.com/watch?v=dz24DgBUQbc
```

Packages will be written to `package_path` as defined in `config.ini`.


**Target an endpoint defined in config for a youtube video:**

```bash
./audio2pk3.py -t minsta https://www.youtube.com/watch?v=dz24DgBUQbc
```

**Target an endpoint defined in config for a youtube video and give it a title:**

```bash
./audio2pk3.py -t minsta https://www.youtube.com/watch?v=dz24DgBUQbc "[SMB] Excision and﻿ Datsik - Guess I Got My Swagger Back"
```

**If downloading an audio file from any site, you must specify a title:**
```bash
./audio2pk3.py https://dl.dropboxusercontent.com/u/xxxxxxxx/land.ogg "Super Mario Bros. Overworld Remix"
```

**A name for the package can also be specified to make it easier to find later (don't use spaces).**
```bash
./audio2pk3.py https://dl.dropboxusercontent.com/u/xxxxxxxx/land.ogg "Super Mario Bros. Overworld Remix" --name "smb-overworld-remix-land"
```

**If using a local audio file, you must specify a title:**
```bash
./audio2pk3.py my_cool_song.mp3 "Super Mario Bros. Overworld Remix"
```

**endpoint_list.txt output:**

```
http://example.com/radio/radio-5wkC8vWbFm8.pk3 5wkC8vWbFm8.ogg 420 Mord Fustang - Lick The Rainbow [Electro House | Plasmapool]
http://example.com/radio/radio-08c22c32-f9b9-11e5-a868-94de80b1b7df.pk3 08c22c32-f9b9-11e5-a868-94de80b1b7df.ogg 152.57 Nexuiz - Beast of Insanity
http://example.com/radio/radio-dz24DgBUQbc.pk3 dz24DgBUQbc.ogg 276 Vanic X K.Flay - Make Me Fade
```

Your packages directory should contain a pk3 with an ogg file inside of it that matches a line in `endpoint_list.txt`

To show a random line from a list whenever a request to the endpoint is made, see `endpoint.php` as an example.

**help:**

```
usage: audio2pk3.py [-h] [--target [TARGET]] [--name [NAME]]
                    input_source [title]

positional arguments:
  input_source          A URL of a youtube video, a remote audio file or local
                        a audio file
  title                 title for the audio file

optional arguments:
  -h, --help            show this help message and exit
  --target [TARGET], -t [TARGET]
                        target endpoint defined under [endpoints] in config
  --name [NAME], -n [NAME]
                        name your download
```

## License

MIT