class Key():
    g_keys_major = ['C', 'C#', 'D', 'D#', 'E',
                     'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    g_keys_minor = ['A', 'A#', 'B', 'C', 'C#',
                     'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    g_mixables = ['C', 'F', 'A#', 'D#', 'G#',
                  'C#', 'F#', 'B', 'E', 'A', 'D', 'G']
    g_note_count = 12

    def __init__(self, key, scale):
        if scale == 'major':
            self.id = self.g_keys_major.index(key)
        elif scale == 'minor':
            self.id = self.g_keys_minor.index(key)
        else:
            print "Note class initialized with the wrong scale"
            exit(1)
        self.key = key
        self.scale = scale

    def is_mixable(self, other_key):
        """
        Return True iff this key is mixable with the other key
        How? http://www.mixedinkey.com/HowTo
        """
        if self.id == other_key.id:
            return True
        if self.scale == other_key.scale:
            a = self.g_mixables.index(self.key)
            b = self.g_mixables.index(other_key.key)
            d = abs(self._shortest_distance(a, b))
            return d == 1
        return False

    def distance(self, other_key):
        """
        Returns shortest tonal distance between this key and the other keys
        """
        return self._shortest_distance(self.id, other_key.id)

    def _shortest_distance(self, this_id, that_id):
        d = that_id - this_id
        if abs(d) > self.g_note_count // 2:
            d = d - self.g_note_count if d > 0 else d + self.g_note_count
        return d
