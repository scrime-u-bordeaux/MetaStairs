# MIDI Stairs engine

### A multi-mode MIDI note events processor for the MIDI Stairs project

## instructions

NB : you might need to replace `python` with `python3` in the below commands.

* `cd` into this folder
* create `venv` : `python -m venv .venv`
* activate `venv` : `source .venv/bin/activate` on mac
* install requirements : `python -m pip install -r requirements.txt`
* start script : `python meta_stairs.py`

When the script starts, it will prompt you to select various MIDI inputs and outputs.  
On mac, we used several IAC busses (you create more than the default one from the *Audio and MIDI configuration* app). 

TODO : replace initial prompt screenshot with the MIDI Stairs Controller appearing as input
TODO : add instructions for what to connect on the auxiliary busses

![initial prompt](../pics/initial-prompt.png)

Once the MIDI inputs and outputs selected, a window opens and allows to select different modes from keyboard shortcuts :

TODO : add a screenshot of the pygame window.
TODO : explain how it works