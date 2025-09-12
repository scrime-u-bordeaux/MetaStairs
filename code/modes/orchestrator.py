import mido
from . import base_mode, scales, shepard, midifile, random, tonnetz

# do not use 'm' and 'i' (reserved for external processes mfp and metaimpro)
text_to_display = """Modes :
 * gammes (g)
 * shepard (s)
 * aléatoire (a)
 * tonnetz (t)
 * midifile performer (m)
 * meta impro (i)

Current mode : {mode}
Current submode : {submode}
"""

modes = {
  'g': scales.Scales(),
  's': shepard.Shepard(),
  # 'f': midifile,
  'a': random.Random(),
  't': tonnetz.Tonnetz(),
}

def getModeKeys():
    res = ['m', 'i']
    res.extend(modes.keys())
    return res

outputPort = 'main'

def setMode(keyName):
    global currentMode
    global outputPort

    if keyName in modes.keys():
        outputPort = 'main'
        currentMode = modes[keyName]
    elif keyName == 'm': # midifile performer
        outputPort = 'aux1'
        currentMode = 'midifile performer'
    elif keyName == 'i': # meta impro
        outputPort = 'aux2'
        currentMode = 'meta impro'

def currentModeIsMode():
    return isinstance(currentMode, base_mode.BaseMode)

def nextSubmode():
    if currentModeIsMode():
        currentMode.nextSubmode()

def prevSubmode():
    if currentModeIsMode():
        currentMode.prevSubmode()

def setSubmode(index):
    if currentModeIsMode():
        currentMode.setSubmode(index)

def getModeName():
    if currentModeIsMode():
        return currentMode.getName()
    return currentMode

def getSubmodeName():
    if currentModeIsMode():
        return currentMode.getSubmodeName()
    return currentMode

activeNotes = {}

# TODO : keep track of active stair steps
# inputNotes = { i: False for i in range(1,10) }

# TODO : keep track of recently played notes to smooth mode transitions
# lastPlayedNotes = []

def noteOffFromNoteOn(m):
    return mido.Message('note_off', note=m.note, velocity=0, channel=m.channel)

def process(msg):
    global channel

    if msg.type == 'note_on' or msg.type == 'note_off':
        if not outputPort == 'main':
            return (outputPort, [ msg ])
        
        msgs = currentMode.process(msg)

        noteOffs = []
        for m in msgs:
            
            if m.type == 'note_on':
                # send note_off before sending note_on if note is active
                if m.note in activeNotes.keys() and activeNotes[m.note] == True:
                    m2 = noteOffFromNoteOn(m)
                    noteOffs.append(m2)
                else:
                    activeNotes[m.note] = True
            elif m.type == 'note_off':
                activeNotes[m.note] = False
        noteOffs.extend(msgs)
        return (outputPort, noteOffs)
