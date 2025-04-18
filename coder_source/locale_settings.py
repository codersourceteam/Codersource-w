from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE / 'db.sqlite3',
    }
}

__all__ = ['ALLOWED_HOSTS',"DATABASES"]