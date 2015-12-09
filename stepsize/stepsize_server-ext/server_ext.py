import os
import json
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

try:
    from urllib2 import urlopen, Request
except ImportError:
    from urllib.request import urlopen, Request

SERVER_DIR = os.path.join(os.path.expanduser('~'), '.ipython/extensions')
CUR_UID = os.path.join(SERVER_DIR, 'stepsize_version-id/uid.json')
STEPSIZE_URL = 'http://search.stepsize.com/api/v0.1/user-activity/'


class uidHandler(IPythonHandler):
    def get(self):
        output = self.read_id(CUR_UID)
        self.finish(output)

    def read_id(self, CONFIG):
        if os.path.isfile(CONFIG):
            with open(CONFIG) as f:
                entries = json.load(f)
        else:
            entries = {'uid': 'uid-missing'}
        return entries


def load_jupyter_server_extension(nbapp):
    if os.path.isfile(CUR_UID):
        with open(CUR_UID) as f:
            entries = json.load(f)
        uid = entries.get('uid', 'uid-missing')
    else:
        uid = 'uid-missing'
    nbapp.log.info('Stepsize extension loaded')
    try:
        values = {'ori': 'jupyter_v0.1', 'uid': uid, 'event': 'session_start'}
        data = urlencode(values)
        binary_data = data.encode('utf-8')
        req = Request(STEPSIZE_URL, binary_data)
        response = urlopen(req)
    except:
        nbapp.log.info('Warning: Could not connect to Stepsize. '
                       'Please check your internet connection.')
    web_app = nbapp.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/uid')
    web_app.add_handlers(host_pattern, [(route_pattern, uidHandler)])
