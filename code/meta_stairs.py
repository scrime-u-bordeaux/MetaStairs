import mido
from utils import gui, userInput
from modes import orchestrator

# MIDI ports selection #########################################################

mido.set_backend('mido.backends.rtmidi')

# default ports #################################
# defaultInputPortName = 'MIDI Stairs Controller'
# defaultOutputPortName = 'Gestionnaire IAC Bus 1'
# defaultOutputPortName2 = 'Gestionnaire IAC Bus 2'
# defaultOutputPortName2 = 'Gestionnaire IAC Bus 3'
defaultInputPortName = None
defaultOutputPortName = None
defaultOutputPortName2 = None
defaultOutputPortName3 = None

inputPortsList = mido.get_input_names()
outputPortsList = mido.get_output_names()

# prompt user if no default ports ###############
inputPortName = userInput.promptWithDefaultValue(
    defaultInputPortName,
    inputPortsList,
    'select MIDI input port:'
)

outputPortName = userInput.promptWithDefaultValue(
    defaultOutputPortName,
    outputPortsList,
    'select main MIDI output port:'
)

outputPortName2 = userInput.promptWithDefaultValue(
    defaultOutputPortName2,
    outputPortsList,
    'select auxiliary MIDI output port 1:'
)

outputPortName3 = userInput.promptWithDefaultValue(
    defaultOutputPortName3,
    outputPortsList,
    'select auxiliary MIDI output port 2:'
)

# notify selected ports #########################
print('now starting program whith:')
print(' * MIDI input port: {ip}'.format(ip = inputPortName))
print(' * main MIDI output port: {op}'.format(op = outputPortName))
print(' * auxiliary MIDI output port 1: {op}'.format(op = outputPortName2))
print(' * auxiliary MIDI output port 2: {op}'.format(op = outputPortName3))

# gui stuff (mostly pygame) ####################################################

def handle_keyboard_input(keyName):
    if keyName in [ 'left', 'down' ]:
        orchestrator.prevSubmode()
    elif keyName in [ 'right', 'up' ]:
        orchestrator.nextSubmode()
    elif keyName in orchestrator.getModeKeys():
        orchestrator.setMode(keyName)
    else:
        return

    lines = orchestrator.text_to_display.format(
        mode = orchestrator.getModeName(),
        submode = orchestrator.getSubmodeName()
    ).splitlines()
    gui.display_multiline_text(lines)

gui.init()

# MIDI initialization (set callback and open ports) ############################

# MIDI callback #################################
def midiInputCallback(msg):
    if msg.type == 'note_on' or msg.type == 'note_off':
        # print('midi callback triggered by {0} event'.format(msg.type))
        (port, msgs) = orchestrator.process(msg)
        # print(port)
        # print(msgs)
        for m in msgs:
            outputPorts[port].send(m)

# open ports ####################################
try:
    outputPort = mido.open_output(outputPortName)
except:
    print('could not open MIDI output port, now exiting program')
    exit()

# if not outputPortName2 in [ outputPortName, outputPortName3 ]:
try:
    outputPort2 = mido.open_output(outputPortName2)
except:
    print('could not open MIDI output port 2, now exiting program')
    exit()
# else:
    # if outputPortName2 == outputPortName:
        # outputPort2 = outputPort
    # else:
try:
    outputPort3 = mido.open_output(outputPortName3)
except:
    print('could not open MIDI output port 3, now exiting program')
    exit()
        

outputPorts = {
    'main': outputPort,
    'aux1': outputPort2,
    'aux2': outputPort3,
}

try:
    inputPort = mido.open_input(inputPortName, callback=midiInputCallback)
except:
    print("could not open MIDI input port, now exiting program")
    exit()

# MAIN LOOP ####################################################################

handle_keyboard_input('g')

try:
    while True:
        keys = gui.check_keyboard_events()
        for k in keys:
            handle_keyboard_input(k)
except KeyboardInterrupt:
    print("\nManual stop")
finally:
    print("Closing MIDI ports")
    inputPort.close()
    outputPort.close()