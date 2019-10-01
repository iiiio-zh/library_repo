import requests
import json
import sys

from django.conf import settings

from library.library import settings

DJANGO_SETTINGS_MODULE = settings


def main():
    SUCCESS = 'OK'
    WARNING = 'WARN'
    ERROR = 'ERROR'
    NONE = 'NONE'

    data = {'projectKey': settings.SONAR_PROJECTKEY}
    url = settings.SONAR_URL + '/api/qualitygates/project_status'
    request = requests.get(url=url, params=data)

    print(request.status_code)
    if request.status_code == 200:
        print(request.content)
        data = json.loads(request.content)
        project_status = data.get('projectStatus', {})
        status = project_status.get('status', '')

        if status == SUCCESS:
            sys.exit(0)
        elif status == WARNING or status == ERROR or status == NONE:
            sys.exit(1)
        else:
            sys.exit(1)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()