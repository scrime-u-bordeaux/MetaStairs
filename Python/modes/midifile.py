################################################################################
#TODO : convert to a child class of BaseMode !!!!
################################################################################

import mido

midifilesPrefix = '../fichiers_midi/'

# midifile parsing function ####################################################

def parseMidifile(fileName):
    midi = mido.MidiFile(midifilesPrefix + fileName)
    events = []
    absolute_time = 0.0

    for msg in midi:
        absolute_time += msg.time
        if msg.type == "note_on" and msg.velocity > 0:
            events.append((absolute_time, msg.note))

    note_groups = []
    group = []
    last_time = events[0][0]
    group_threshold = 0.02

    for t, note in events:
        if (t - last_time) <= group_threshold:
            group.append(note)
        else:
            if group:
                note_groups.append(group)
            group = [note]
            last_time = t

    # append last group
    if group:
        note_groups.append(group)
    return note_groups

# prepare midifiles ############################################################

midifileNames = [
    # 'Beethoven-Moonlight-Sonata.mid',
    # 'MoonlightSonataLoop.mid',
    'BachPreludeInCLoop.mid',
]

sequences = { k: parseMidifile(k) for k in midifileNames }

sequence = sequences[midifileNames[0]]

index = 0

# process function #############################################################

def process(msg):
    global index
    msgs = []

    if msg.type == 'note_on':
        for n in sequence[index]:
            msgs.append(mido.Message('note_on', note=n, velocity=msg.velocity, channel=0))
        index = (index + 1) % len(sequence)
    
    return msgs