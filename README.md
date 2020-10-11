[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=HE-Arc_social-audio-free-market&metric=alert_status)](https://sonarcloud.io/dashboard?id=HE-Arc_social-audio-free-market)

# social-audio-free-market

A place for audio samples sharing and common creations.

## Demo

You can visit the master version of the project [here](https://safmarket.srvz-webapp.he-arc.ch/).

## Installation

### Linux packages

```
sudo apt-get install libavcodec-dev libavformat-dev libavutil-dev libswresample-dev
sudo apt-get install sox
sudo apt-get install ffmpeg
sudo apt-get install mediainfo
```

### Backend

First, you need to add a file for your local settings in *src/safm/settings/local_settings.py*. This file is ignored by Git and allows you to overwrite some configurations for you development environment :

```
from safm.settings.common import *

SECRET_KEY = 'YOUR SECRET KEY'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
```

Depending on your development database, you can also overwrite its configuration in this file.

After that, create a virtual environment :

```
python3 -m venv venv
source venv/bin/activate
```

Then, install the dependencies :

```
pip install -r requirements.txt
```

Install pre-commit hooks:

```
pre-commit install
```

At last, apply the migrations and run the server :

```
python safm/manage.py migrate
python safm/manage.py runserver
```

### Frontend

Go to the frontend application :

```
cd safm/safm_nuxt
```

Once there, install the npm dependencies :

```
npm install
```

At last, run the application :

```
npm run dev
```
