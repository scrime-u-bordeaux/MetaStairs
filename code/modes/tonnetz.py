import random
from . import base_mode

class Tonnetz(base_mode.BaseMode):
    def __init__(self):
        super().__init__('tonnetz')
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
        ]

        self._previousTransition = 'p'
        self._noteArray = self._makeNoteArray()

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
        else:
            return

        self._root += offset
        self._root %= 12
        self._major = not self._major
        self._previousTransition = t
        self._noteArray = self._makeNoteArray()
         
    def _getRandomNote(self):
        return self._noteArray[random.randrange(len(self._noteArray) - 1)]

    def process(self, msg):
        msgs = []
        if msg.type == 'note_on':
            if self._counter >= self._maxCounter:
                self._counter = 0
                self._transition(self._transitions[random.randrange(len(self._transitions) - 1)])
            msg.note = self._getRandomNote()
            self._counter += 1
            msgs = [ msg ]
        return msgs
