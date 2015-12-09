import os
import sys
import json
import shutil
import datetime
from notebook.services.config import ConfigManager
from jupyter_core.paths import jupyter_config_dir

NB_EXT_DIR = os.path.join(os.path.expanduser('~'), '.ipython/nbextensions')
CUR_NB_EXT = os.path.join(NB_EXT_DIR, 'stepsize_nb-ext')
NB_CONFIG = os.path.join(ConfigManager()._config_dir_default(),
                         'notebook.json')

SERVER_EXT_DIR = os.path.join(os.path.expanduser('~'), '.ipython/extensions')
CUR_SERVER_EXT = os.path.join(SERVER_EXT_DIR, 'stepsize_server-ext')
SERVER_CONFIG = os.path.join(jupyter_config_dir(), 'jupyter_config.py')
SERVER_EXT_CONFIG = [
    "c.NotebookApp.allow_credentials = True",
    "c.NotebookApp.allow_origin_pat = "
    "'(http\://localhost:[0-9]{4}.*|http\://127\.0\.0\.1:[0-9]{4}.*)'",
    "sys.path.append(os.path.join(os.path.expanduser('~'), "
    "'.ipython/extensions/stepsize_server-ext'))",
    "if isinstance(c.NotebookApp.server_extensions, list):",
    "    c.NotebookApp.server_extensions.append('server_ext')",
    "else:",
    "    c.NotebookApp.server_extensions = []",
    "    c.NotebookApp.server_extensions.append('server_ext')"
]


def main():
    remove_extension(NB_EXT_DIR, CUR_NB_EXT)
    remove_extension(SERVER_EXT_DIR, CUR_SERVER_EXT)
    remove_notebook_config(NB_CONFIG)
    remove_server_config(SERVER_CONFIG, SERVER_EXT_CONFIG)
    remove_egg()
    print "Stepsize uninstallation complete"


def remove_extension(DIR, CUR_EXT):
    # Removes the installed stepsize extension
    if os.path.exists(CUR_EXT):
        try:
            shutil.rmtree(CUR_EXT)
            print "OUTCOME: Removed the Stepsize extension from your " \
                  "%s directory" % (DIR)
        except:
            print "WARNING: Unable to uninstall the extension in your " \
                  "%s directory" % (DIR)
            print "ERROR: %s, at line %d" % (sys.exc_info()[0],
                                             sys.exc_traceback.tb_lineno)
    else:
        print "WARNING: Unable to uninstall the Stepsize extension since it " \
              "does not exist in %s" % (DIR)


def remove_notebook_config(CONFIG):
    # Removes the config in the notebook json
    if os.path.isfile(CONFIG):
        # Creates a backup file
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_T%H-%M-%S")
        title = ('backup_notebook_' + timestamp + '.json')
        BACKUP = os.path.join(ConfigManager()._config_dir_default(), title)
        print "ACTION: Creating a backup notebook.json, %s" % (BACKUP)
        shutil.copyfile(CONFIG, BACKUP)
        # Element to be removed
        data_element = {'stepsize_nb-ext/main_v0-1': True}
        # Counter
        count = 0
        try:
            if open(CONFIG).read() != "":
                with open(CONFIG) as f:
                    entries = json.load(f)
                if 'stepsize_nb-ext/main_v0-1' in entries['load_extensions']:
                    entries['load_extensions'].pop('stepsize_nb-ext/main_v0-1',
                                                   None)
                    count += 1
                    with open(CONFIG, 'w') as outfile:
                        json.dump(entries, outfile)
                if count > 0:
                    print "OUTCOME: Removed the Stepsize extension " \
                          "configuration from the notebook.json"
        except:
            print "WARNING: An error occured when trying to remove %s from " \
                  "the notebook.json" % (data_element)
            print "ERROR: %s, at line %d" % (sys.exc_info()[0],
                                             sys.exc_traceback.tb_lineno)
    else:
        print "WARNING: Unable to remove the Stepsize extension " \
              "configuration since the notebook.json does not exist in %s"\
              % (ConfigManager()._config_dir_default())


def remove_server_config(CONFIG, EXT_CONFIG):
    # Removes the config in the jupyter_config.py
    if os.path.isfile(CONFIG):
        # Creates a backup file
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y_T%H-%M-%S")
        title = ('backup_config_' + timestamp + '.py')
        BACKUP = os.path.join(jupyter_config_dir(), title)
        print "ACTION: Creating a backup jupter_config.py, %s" % (BACKUP)
        shutil.copyfile(CONFIG, BACKUP)
        # Counter
        count = 0
        try:
            f = open(CONFIG, 'r')
            lines = f.readlines()
            f.close()
            f = open(CONFIG, 'w')
            for line in lines:
                if any(i in line for i in EXT_CONFIG):
                    pass
                    count += 1
                else:
                    f.write(line)
            f.truncate()
            f.close()
            if count > 0:
                print "OUTCOME: Removed the Stepsize extension " \
                      "configuration from the jupyter_config.py"
        except:
            print "WARNING: An error occured when trying to remove the " \
                  "Stepsize server configuration from the jupyter_config.py"
            print "ERROR: %s, at line %d" % (sys.exc_info()[0],
                                             sys.exc_traceback.tb_lineno)
    else:
        print "WARNING: Unable to remove the Stepsize extension " \
              "configuration since the jupyter_config.py does not exist in " \
              "%s" % (jupyter_config_dir())


def remove_egg():
    # Removes the Stepsize.egg-info
    EGG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           'Stepsize.egg-info')
    if os.path.exists(EGG_DIR):
        try:
            shutil.rmtree(EGG_DIR)
            print "OUTCOME: Removed the Stepsize.egg-info"
        except:
            print "WARNING: Unable to remove the Stepsize.egg-info"
            print "ERROR: %s, at line %d" % (sys.exc_info()[0],
                                             sys.exc_traceback.tb_lineno)
    else:
        print "WARNING: Unable to remove the Stepsize.egg-info since it " \
              "does not exist in the directory"


if __name__ == '__main__':
    main()
