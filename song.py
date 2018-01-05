from itertools import izip
from sample import Sample
from heuristics import assemble_samples


class Song(object):
    def __init__(self, name, slices, chunk_sizes):
        self.name = name
        self.slices = slices
        self.sizes = chunk_sizes

        # Associate each slice with this song
        for s in slices:
            if s is not None:
                s.song = self

        # Assemble the samples, stating with the smallest
        self.min_size = min(self.sizes)
        self.samples = {
            self.min_size: [Sample((s,), self, self.min_size, i) if s is not None else None
                            for i, s in enumerate(self.slices)]
        }

        # Create samples of larger chunk sizes
        for size, size_ in izip(self.sizes, self.sizes[1:]):
            self.samples[size_] = assemble_samples(self.samples[size])

    def __getitem__(self, size):
        return self.samples[size]

    def next_sample(self, prev_sample, size):
        nidx = (prev_sample.size / size * prev_sample.index) + 1
        if len(self[size]) <= nidx:
            return None
        else:
            return self[size][nidx]
