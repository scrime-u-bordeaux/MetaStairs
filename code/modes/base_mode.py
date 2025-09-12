class BaseMode:
    class Submode:
        def __init__(self, name = 'None', data = None):
            self.name = name
            self.data = data

    def __init__(self, name = 'None', submodes = []):
        self._name = name
        self._submodes = submodes
        self._currentSubmode = None
        self._currentSubmodeIndex = -1
        self._minNoteIn = 1
        self._maxNoteIn = 9
        self._minNoteOut = 21
        self._maxNoteOut = 108
        self.data = None

    def nextSubmode(self):
        if len(self._submodes) > 0:
            tmpi = (self._currentSubmodeIndex + 1) % len(self._submodes)
            self._currentSubmodeIndex = tmpi
            self._updateSubmode()
    
    def prevSubmode(self):
        if len(self._submodes) > 0:
            tmpi = self._currentSubmodeIndex - 1
            if tmpi < 0: tmpi = len(self._submodes) - 1
            self._currentSubmodeIndex = tmpi
            self._updateSubmode()

    def setSubmode(self, index):
        if index in range(0, len(self._submodes)):
            self._currentSubmodeIndex = index
            self._updateSubmode()        
    
    def _updateSubmode(self):
        if self._currentSubmodeIndex in range(0, len(self._submodes)):
            currentSubmode = self._submodes[self._currentSubmodeIndex]
            if isinstance(currentSubmode, BaseMode.Submode):
                self._currentSubmode = currentSubmode
                self.data = self._currentSubmode.data

    def getName(self):
        #print('getting current mode name : {0}'.format(self._name))
        return self._name
    
    def getSubmodeName(self):
        #print('getting current mode name : {0}'.format(self._currentSubmode.name))
        if not self._currentSubmode is None:
            return self._currentSubmode.name
        return self._name
    
    def process(self, msg):
        return [ msg ]
