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
cp example.config.ini config.ini
```

The file should contain something similar to the following:

```
[default]
# URL for where the radio pk3s live
site_url = http://example.com/radio/

# absolute or relative path to an endpoint file
endpoint_file = /home/radio/web/html/endpoint.txt

# absolute or relative path to where the packages live
package_path = /home/radio/web/html/radio/

# absolute or relative path for cached media files
cache_path = cache/

# what to use to convert the audio format to ogg
encoding_driver = ffmpeg
```

Paths can be either absolute or relative. It would be good practice to have this live in a non-web accessible, but allow it to write the packages to a web facing folder.

## Usage

Make sure youtube2pk3.py is executable, `chmod +x youtube2pk3.py`, then run it as follows:


```bash
./youtube2pk3.py "https://www.youtube.com/watch?v=dz24DgBUQbc"
```

endpoint.txt output:


```
http://example.com/radio/yt-dz24DgBUQbc.pk3 dz24DgBUQbc.ogg 276 Vanic X K.Flay - Make Me Fade
```

Your packages folder should contain a pk3 with an ogg file inside of it that matches the endpoint.txt
