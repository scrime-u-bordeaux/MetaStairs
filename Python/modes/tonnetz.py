import random
from . import base_mode

class Tonnetz(base_mode.BaseMode):
    def __init__(self, channel):
        super().__init__('tonnetz', [], channel)
        random.seed()

        self._counter = 0
        self._maxCounter = 12
        self._patterns = [
            [ 4, 3, 5 ],
            [ 3, 4, 5 ]
        ]
        self._root = 0
        self._major = True

        self._transitions = [
            'p', # parallel, picarde
            'r', # relative
            'l', # leittonwechsel, leading tone exchange
            'minus1', # -1 halftone transposition
        ]

        self._previousTransition = 'p'
        self._noteArray = self._makeNoteArray()
    
        chunkSize = len(self._noteArray) // 9
        # print(f'noteArray length : {len(self._noteArray)}')
        # print(f'chunkSize : {chunkSize}')
        # remainder = len(self._noteArray) % 9
        self._chunks = []
        for i in range(8):
            self._chunks.append([ i * chunkSize, (i + 1) * chunkSize])
        self._chunks.append([ 8 * chunkSize, len(self._noteArray)])

    def _makeNoteArray(self):
        pattern = self._patterns[0]
        if not self._major:
            pattern = self._patterns[1]

        n = self._root - 12
        i = 0
        res = []
        
        while n < self._maxNoteOut:
            if n >= self._minNoteOut:
                res.append(n)
            n += pattern[i]
            i = (i + 1) % 3

        return res

    def _transition(self, t):
        offset = 0

        if t == 'p':
            pass
        elif t == 'r':
            if self._major: offset = 9
            else: offset = 3
        elif t == 'l':
            if self._major: offset = 4
            else: offset = 8
        elif t == 'minus1':
            offset = 11
        else:
            return

        self._root += offset
        self._root %= 12
        self._major = not self._major
        self._previousTransition = t
        self._noteArray = self._makeNoteArray()
         
    def _getRandomNote(self, chunk = -1):
        if chunk in range(9):
            min, max = self._chunks[chunk]
            # print(min, max)
            return self._noteArray[random.randrange(min, max)]
        return self._noteArray[random.choice(self._noteArray)]

    def process(self, msg):
        msgs = []
        if msg.type == 'note_on':
            if self._counter >= self._maxCounter:
                self._counter = 0
                self._transition(self._transitions[random.randrange(len(self._transitions) - 1)])
            note_in = msg.note
            msg.note = self._getRandomNote(note_in - self._minNoteIn)
            msg.channel = self._channel
            self._counter += 1
            msgs = [ msg ]
        return msgs
