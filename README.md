## Setup

#### System Requirements

```
avconv
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

## Usage

Make sure youtube2pk3.py is chmod +x, `chmod +x youtube2pk3.py`, then run it as follows:


```
./youtube2pk3.py https://www.youtube.com/watch\?v\=dz24DgBUQbc
```

endpoint.txt output:


```
http://example.com/radio/packages/dz24DgBUQbc.pk3 276 Vanic X K.Flay - Make Me Fade
```

Your packages folder should contain a pk3 with an ogg file inside of it that matches the endpoint.txt
