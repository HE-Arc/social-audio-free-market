# social-audio-free-market

A place for audio samples sharing and common creations.

## Installation

### Backend

First, create a virtual environment :

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