[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=HE-Arc_social-audio-free-market&metric=alert_status)](https://sonarcloud.io/dashboard?id=HE-Arc_social-audio-free-market)

# social-audio-free-market

A place for audio samples sharing and common creations.

## Demo

You can visit the master version of the project [here](https://safmarket.srvz-webapp.he-arc.ch/).

## Installation

### Backend

First, you need to add a file for your local settings in *safm_project/safm_project/settings/local_settings.py*. This file is ignored by Git and allows you to overwrite some configurations for you development environment :

```
from safm_project.settings.common import *

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

At last, apply the migrations and run the server :

```
python safm_project/manage.py migrate
python safm_project/manage.py runserver
```

### Frontend

Go to the frontend application :

```
cd safm_project/safm_frontend
```

Once there, install the npm dependencies :

```
npm install
```

At last, run the application :

```
npm run dev
```
