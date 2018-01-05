class Sample(object):
    def __init__(self, slices, song, size, index):
        self.slices = slices
        self.song = song
        self.size = size
        self.index = index


class Slice(object):
    def __init__(self, file):
        self.file = file
