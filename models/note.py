import logging


class Note():
    g_notes_major = ['C', 'C#', 'D', 'D#', 'E',
                     'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    g_notes_minor = ['A', 'A#', 'B', 'C', 'C#',
                     'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    g_mixables = ['C', 'F', 'A#', 'D#', 'G#',
                  'C#', 'F#', 'B', 'E', 'A', 'D', 'G']
    g_note_count = 12

    def __init__(self, note, scale):
        if scale == 'major':
            self.id = self.g_notes_major.index(note)
        elif scale == 'minor':
            self.id = self.g_notes_minor.index(note)
        else:
            print "Note class initialized with the wrong scale"
            exit(1)
        self.note = note
        self.scale = scale

    def is_mixable(self, other_note):
        """
        Return True iff this note is mixable with the other note
        How? http://www.mixedinkey.com/HowTo
        """
        if self.id == other_note.id:
            return True
        if self.scale == other_note.scale:
            a = self.g_mixables.index(self.note)
            b = self.g_mixables.index(other_note.note)
            d = abs(self._shortest_distance(a, b))
            return d == 1
        return False

    def distance(self, other_note):
        """
        Returns shortest tonal distance between this note and the other notes
        """
        return self._shortest_distance(self.id, other_note.id)

    def _shortest_distance(self, this_id, that_id):
        d = that_id - this_id
        if abs(d) > self.g_note_count // 2:
            d = d - self.g_note_count if d > 0 else d + self.g_note_count
        return d
