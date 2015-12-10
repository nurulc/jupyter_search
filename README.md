Jupyter Search (Python)
-------------------------------

This Jupyter Notebook extension allows you to quickly find information relating to a class, function, etc. The extension returns the class/function signature (including a link to the documentation) and an example code snippet from StackOverflow or the documentation.

![Stepsize Search Demo](http://imgur.com/UgS7rr0.gif)

Usage
-----

In any code cell, just type `library_name function_name`, and press `alt` + `/`. The search result will be printed in the cell's output area.

Alternatively, select some text in any code cell, and press `alt` + `/`.

When you actually run the cell, the search result is overwritten with the output of your code.

Note:

 - On Mac, the search shortcut is `⌥` + `/`.

 - Supports both Python 2.7 and Python 3.

 - The extension only works on Jupyter versions 4.x. Do not try to install the extension if you're not using Jupyter 4.x.

 - The extension currently only supports Python-related searches.


You can manage all your extensions from the `notebook.json` which is located in `~/.jupyter/nbconfig/notebook.json`. For more information on how notebook extensions work please see [Notebook extensions|Jupyter](https://carreau.gitbooks.io/jupyter-book/content/notebook-extensions.html)

Installation
------------

#### Jupyter Notebook Installation/Upgrade

First, make sure your version of Jupyter is up-to-date.

 - To install Jupyter Notebook, run `pip install jupyter` (see [How to install Jupyter Notebook](http://jupyter.readthedocs.org/en/latest/install.html#how-to-install-jupyter-notebook)).

 - To update Jupyter Notebook, run `pip install -U jupyter` (see [Upgrading to Jupyter](http://jupyter.readthedocs.org/en/latest/install.html#upgrading-to-jupyter-experienced-users)).

#### Jupyter Search Extension Installation

To install the Jupyter Search extension, run the commands below.

```
git clone https://github.com/Stepsize/jupyter_search.git
cd jupyter_search
python setup.py install
```

After installation, when you boot up Jupyter Notebook (`jupyter notebook`) you'll see "Stepsize extension loaded" printed in your terminal.

You can delete the `jupyter_search` cloned repo after installation, but you'll have to clone it again if you want to uninstall the extension.


#### Remote Jupyter Notebook Servers

If you do not run your Jupyter Notebook server locally, you will need to make a small modification to the configuration settings after installing the extension with `setup.py`.

The current configuration (v0.1) only allows localhost cross-origin requests to the Jupyter Notebook server, this is defined in the `jupyter_config.py` which is located (in the user directory) `~/.jupyter/jupyter_config.py`.

To allow the extension to work for remote Jupyter Notebook servers, add the following line of code to the `jupyter_config.py`.

```
c.NotebookApp.allow_origin = "*"
```
This will allow all cross-origin requests, and will override any regular expression set on `c.NotebookApp.allow_origin_pat` (this is where we have set it to allow cross-origin request from the localhost with any port).

Uninstaller
-----------

If you no longer have the cloned repo, first run `git clone https://github.com/Stepsize/jupyter_search.git`.

```
cd /path/to/jupyter_search
python uninstall.py main
```
