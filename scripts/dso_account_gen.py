import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FILE_NAME = Path(__file__).stem


def generate_dso_account():
    from accounts.models import User, UserRecord
    from agent.models import DSO

    for dso in DSO.objects.all():
        pass_pattern = f'Siddiquee{dso.mobile[-2:]}'
        user = User.objects.create(username=dso.mobile)
        user.set_password(pass_pattern)
        user.save()

        UserRecord.objects.create(mobile=dso.mobile, password=pass_pattern)


def attach_dso_account():
    from accounts.models import User
    from agent.models import DSO

    for dso in DSO.objects.all():
        user = User.objects.get(username=dso.mobile)
        dso.account = user
        dso.save()


def _setup_django():
    sys.path.append(BASE_DIR.as_posix())
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agent_tracker.settings')

    import django
    django.setup()


if __name__ == '__main__':
    _setup_django()

    # generate_dso_account()
    attach_dso_account()
