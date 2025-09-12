from . import base_mode

class Scales(base_mode.BaseMode):
    def __init__(self):
        submodes = [
            base_mode.BaseMode.Submode(
                name = 'diatonique',
                data = {
                    'scale': [0, 2, 4, 5, 7, 9, 11, 12, 14],
                    'offset': 60,
                }
            ),
            base_mode.BaseMode.Submode(
                name = 'chromatique',
                data = {
                    'scale': [0, 1, 2, 3, 4, 5, 6, 7, 8],
                    'offset': 60,
                }
            ),
            base_mode.BaseMode.Submode(
                name = 'gamme par ton',
                data = {
                    'scale': [0, 2, 4, 6, 8, 10, 12, 14, 16],
                    'offset': 60,
                }
            ),
        ]
        super().__init__('gammes', submodes)

        self.nextSubmode()

    def process(self, msg):
        if msg.type == 'note_on' or msg.type == 'note_off':
            scale = self.data['scale']
            offset = self.data['offset']
            msg.note = scale[msg.note - self._minNoteIn] + offset
            return [ msg ]
        return []
