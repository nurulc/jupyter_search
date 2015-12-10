import os
import sys
import json
import shutil
import uuid
from setuptools import setup
from setuptools.command.install import install
from ipython_genutils.path import ensure_dir_exists
from notebook.nbextensions import install_nbextension
from notebook.services.config import ConfigManager
from jupyter_core.paths import jupyter_config_dir
from jupyter_core.application import JupyterApp


NB_DIR = os.path.join(os.path.expanduser('~'), '.ipython/nbextensions')
NB_EXT_DIR = os.path.join(os.path.dirname(__file__),
                          'stepsize/stepsize_nb-ext')
CUR_NB_EXT = os.path.join(NB_DIR, 'stepsize_nb-ext')

SERVER_DIR = os.path.join(os.path.expanduser('~'), '.ipython/extensions')
SERVER_EXT_DIR = os.path.join(os.path.dirname(__file__),
                              'stepsize/stepsize_server-ext')
CUR_SERVER_EXT = os.path.join(SERVER_DIR, 'stepsize_server-ext')
SERVER_EXT_CONFIG = [
    "c.NotebookApp.allow_credentials = True",
    "c.NotebookApp.allow_origin_pat = "
    "'(http\://localhost:[0-9]{4}.*|http\://127\.0\.0\.1:[0-9]{4}.*)'",
    "import os",
    "import sys",
    (
        "sys.path.append(os.path.join(os.path.expanduser('~'), "
        "'.ipython/extensions/stepsize_server-ext'))\n"
        "if isinstance(c.NotebookApp.server_extensions, list):\n"
        "    c.NotebookApp.server_extensions.append('server_ext')\n"
        "else:\n"
        "    c.NotebookApp.server_extensions = []\n"
        "    c.NotebookApp.server_extensions.append('server_ext')"
    )
]

UID_DIR = os.path.join(SERVER_DIR, 'stepsize_version-id')
UID = os.path.join(os.path.dirname(__file__), 'stepsize/stepsize_version-id')
CUR_UID = os.path.join(SERVER_DIR, 'stepsize_version-id/uid.json')


class InstallCommand(install):
    def run(self):
        install.run(self)
        self.setup_extensions(CUR_NB_EXT, NB_EXT_DIR, NB_DIR)
        self.setup_extensions(CUR_SERVER_EXT, SERVER_EXT_DIR, SERVER_DIR)
        self.setup_notebook_config()
        self.setup_server_config(SERVER_EXT_CONFIG)
        self.setup_uid(UID_DIR, CUR_UID, UID)
        self.write_uid(CUR_UID)
        print("Stepsize installation complete")

    def query(self, question, default="yes"):
        valid = {"yes": "yes",   "y": "yes",  "ye": "yes",
                 "no": "no",     "n": "no"}
        if not default:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while 1:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return default
            elif choice in valid.keys():
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")


    def setup_extensions(self, CUR_EXT, EXT_DIR, DIR):
        # Install the extensions to the required directories
        ensure_dir_exists(DIR)
        if os.path.exists(CUR_EXT):
            question = "ACTION: The Stepsize extension directory already " \
                       "exists, do you want to overwrite %s with the " \
                       "current installation?" % (CUR_EXT)
            prompt = self.query(question)
            if prompt == "yes":
                try:
                    install_nbextension(EXT_DIR, overwrite=True,
                                        nbextensions_dir=DIR)
                    print("OUTCOME: Added the extension to your " \
                          "%s directory" % (DIR))
                except:
                    print("WARNING: Unable to install the extension to your " \
                          "(nb)extensions folder")
                    print("ERROR: %s" % (sys.exc_info()[0]))
                    raise
            else:
                return
        else:
            try:
                install_nbextension(EXT_DIR, overwrite=True,
                                    nbextensions_dir=DIR)
                print("OUTCOME: Added the extension to your %s directory" \
                      % (DIR))
            except:
                print("WARNING: Unable to install the extension to your " \
                      "(nb)extensions folder")
                print("ERROR: %s" % (sys.exc_info()[0]))
                raise

    def setup_notebook_config(self):
        # Set the notebook extension to launch on startup by
        # modifying the notebook.json
        ensure_dir_exists(ConfigManager()._config_dir_default())
        # Elements to be added
        data_element = {'stepsize_nb-ext/main_v0-1': True}
        data = {'load_extensions': data_element}
        try:
            cm = ConfigManager()
            cm.update('notebook', data)
            print("OUTCOME: Added the Stepsize notebook extension " \
                  "configuration to the notebook.json")
        except:
            print("WARNING: An error occured when trying to add %s to the " \
                  "notebook.json" % (data))
            print("ERROR: %s" % (sys.exc_info()[0]))
            raise

    def setup_server_config(self, EXT_CONFIG):
        # Set the server extension to launch on startup by modifying the
        # jupyter_notebook_config.py
        CONFIG = os.path.join(jupyter_config_dir(), 'jupyter_config.py')
        ensure_dir_exists(jupyter_config_dir())
        if os.path.isfile(CONFIG):
            pass
        else:
            c = JupyterApp()
            c.write_default_config()
        with open(CONFIG, 'r+') as fh:
            lines = fh.read()
            for i in EXT_CONFIG:
                if i not in lines:
                    fh.seek(0, 2)
                    fh.write('\n')
                    fh.write(i)
        print("OUTCOME: Added the Stepsize server extension " \
              "configuration to the jupyter_config.py")

    def setup_uid(self, UID_DIR, CUR_UID, UID):
        if os.path.isfile(CUR_UID):
            pass
        else:
            shutil.copytree(UID, UID_DIR)
            print("OUTCOME: Added the Stepsize extension installation " \
                  "identifier to %s" % (os.path.join(os.path.expanduser('~'),
                                                     '.ipython/extensions')))

    def write_uid(self, CUR_UID):
        # Code to write the uuid to the users uuid.json in their directory
        with open(CUR_UID) as f:
            entry = json.load(f)
        if entry['uid'] == "xxxx":
            id = str(uuid.uuid4())
            entry['uid'] = id
            with open(CUR_UID, 'w') as outfile:
                json.dump(entry, outfile)
                print("OUTCOME: Set the Stepsize extension installation " \
                      "identifier")

setup(
    name='Stepsize',
    version='0.1',
    description='Search for Python code snippets directly from code cells',
    long_description='Search for code snippets with a library and function '
                     'name within code cells, the extension will return a '
                     'function signature with a link to the documentation as '
                     'well as a code snippet with a StackOverflow link.',
    platforms='Mac OS X, Windows',
    author='Stepsize',
    author_email='hello@stepsize.com',
    url='http://www.stepsize.com',
    licence='BSD 3-Clause',
    packages=['stepsize'],
    cmdclass={'install': InstallCommand}
)
