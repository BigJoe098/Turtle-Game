# Turtle-Game
A simple video game built using turtle library in python as a pet project. Heavily inspired by the snake game but with my own twist.

# Getting Started

First clone the repository from Github and switch to the new directory:

    $ git clone https://github.com/BigJoe098/Turtle-Game
    $ cd {{ Path to directory with the project }}

Activate the virtualenv for your project if installed. To install the virtual follow the steps as below.
make sure you have turtle installed.

Then simply run the game:

    $ python Turtle-game.py

### Virtualenv

If you want to install the virtualenv then you will need to first create the virtual enviroment then follow along with the steps in no
virtual enviroment

FOR LINUX/MAC:

    $ sudo apt-get install python3.6-venv
    $ python3 -m venv env
    $ source env/bin/activate

FOR WINDOWS:

    $ py -m pip install --user virtualenv
    $ py -m venv env
    $ .\env\Scripts\activate

### No virtualenv

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid
for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have turtle installed for python 3 then run:

    $ pip install PythonTurtle

And then:

    $ python Turtle-game.py

### Existing virtualenv

If your project is already in an existing python3 virtualenv first install turtle by running

    $ pip install PythonTurtle

And then:

    $ python Turtle-game.py

Enjoy!!
