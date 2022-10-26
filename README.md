# openmusicdata
open-source data project to connect music


## DEBUG IN VSCODE

path to Interpreter:
~/dev/.venvs/.omd/bin/python3

## Python3 / Venv setup notes

mkdir /dev/.virtualenv

sudo apt-get install python3-venv

python3 -m venv .omd


source path/to/.omd/bin/activate
(alias this to "use omd"

pip freeze


python3
>> import spotipy


/home/brian/dev/.virtualenvs/.omd/lib/python3.6/site-packages/spotipy

deactivate

pip install -r requirements.txt

docker - run+install from requirements.txt


POSTGRES
sudo apt-get install libpq-dev
sudo apt-get install python3-dev




data pipelines/transformation

jupyter notebooks

pip install jupyterlab
>> jupyter-lab

pip install notebook
>> jupyter notebook

## Python Debugging with PDB

python3
>> import pdb
>> import spotipy1

pdb.run(spotipy1.getData())

inline code:

import pdb
pdb.set_trace();

https://docs.python.org/3/library/pdb.html#debugger-commands

