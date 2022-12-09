import MusicCapture

class Search:
    def __init__(self, _Name):
        self.name = _Name

    def SearchAll(self):
        DATA = []
        for value in MusicCapture.GetMusic163.GetMusic163Music(self.name).Search().values():
            DATA.append(value)
        for value in MusicCapture.GetKuwo.Kuwo(self.name).Search().values():
            DATA.append(value)
        return DATA