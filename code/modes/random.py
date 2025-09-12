import random
from . import base_mode

class Random(base_mode.BaseMode):
    def __init__(self):
        super().__init__('aleatoire')
        random.seed()

    def process(self, msg):
        if msg.type == 'note_on':
            msg.note = random.randrange(21, 108, 1)
            return [ msg ]
        return []