import mido
from . import base_mode

class Shepard(base_mode.BaseMode):
    def __init__(self):
        submodes = [
            base_mode.BaseMode.Submode(
                name = 'montant',
                data = { 'increment': 1 }
            ),
            base_mode.BaseMode.Submode(
                name = 'descendant',
                data = { 'increment': -1 }
            ),
        ]
        super().__init__('shepard', submodes)

        self._pitch_classes = list(range(12)) # From C (0) to B (11)
        self._shepard_groups = []
        self._index = 0
        self._init_armed = True

        self._init_shepard_groups()
        self.nextSubmode()

    def _init_shepard_groups(self):
        for base in self._pitch_classes:
            # Play over 5 octaves (C2 -> C6) (TODO : make this parameterizable)
            group = [base + 12 * i for i in range(2, 7)]
            self._shepard_groups.append(group)

    def _shepard_volume(self, note):
        center = 60
        min_vol = 0.1
        max_vol = 1.0
        k = 0.00125
        distance = note - center
        attenuation = 1 - k * (distance ** 2)
        attenuation = max(0.0, min(1.0, attenuation))
        return min_vol + (max_vol - min_vol) * attenuation
    
    def _apply_increment(self):
        if self._init_armed:
            self._init_armed = False
            return
        
        self._index = self._index + self.data['increment']

        if self._index >= len(self._pitch_classes):
            self._index = self._index % len(self._pitch_classes)
        else:
            while self._index < 0:
                self._index += len(self._pitch_classes)

    def process(self, msg):
        msgs = []
        
        if msg.type == 'note_on':    
            self._apply_increment()
            group = self._shepard_groups[self._index]

            for n in group:
                msgs.append(mido.Message(
                    'note_on',
                    note = n,
                    velocity = int(self._shepard_volume(n) * 64),
                    channel = 0
                ))

        return msgs
