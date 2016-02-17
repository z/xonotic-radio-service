## Setup

#### System Requirements

```
avconv
```

On Debian based systems avconv can be installed with the following:

```
sudo apt-get install libav-tools
```


#### Setup local packages

Clone from git

```
git clone https://github.com/z/xonotic-radio-service.git
```

Setup a venv and install the requirements

```
virtualenv -p /usr/bin/python3 venv
ln -s venv/bin/activate
source activate
pip install -r requirements.txt
```

## Configuration

Copy `example.config.ini` and edit `config.ini` to your server settings:

`cp example.config.ini config.ini`

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
```

Paths can be either absolute or relative. It would be good practice to have this live in a non-web accessible, but allow it to write the packages to a web facing folder.

## Usage

Make sure youtube2pk3.py is chmod +x, `chmod +x youtube2pk3.py`, then run it as follows:


```
./youtube2pk3.py "https://www.youtube.com/watch?v=dz24DgBUQbc"
```

endpoint.txt output:


```
http://example.com/radio/packages/dz24DgBUQbc.pk3 276 Vanic X K.Flay - Make Me Fade
```

Your packages folder should contain a pk3 with an ogg file inside of it that matches the endpoint.txt
