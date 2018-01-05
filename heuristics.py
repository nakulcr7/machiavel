import random
from itertools import izip
from sample import Sample


def build_tracks(songs, length, n_tracks, coherent=True):
    # Build the first track
    track = build_bar(songs, length, coherent=coherent)

    # Convert to a flattened list of slices
    track = sum([s.slices for s in track], ())

    tracks = [track]
    for i in range(n_tracks - 1):
        track_ = build_bar(songs, length, coherent=coherent, tracks=tracks)
        track_ = sum([s.slices for s in track_], ())
        tracks.append(track_)

    return tracks


def build_bar(songs, n, prev_sample=None, coherent=True, tracks=[], bar_position=0, recur=0):
    """
    Builds a bar of n beats in length,
    where n >= the shortest sample length.
        e.g. if the samples are cut into bars of 8, 16, 32,
        then n must be >= 8.
    Bars are constructed by selecting a sample of length n
    or by placing two adjacent bars of length n/2. This structure
    *should* produce more coherent (less spastic) tracks.
        e.g a bar of length 16 can be created by two samples of length 8
        or one sample of length 16, if available.
    A bar is returned as a list of samples.
    If `coherent=True`, Machiavel will try to build _coherent_ bars:
        - higher probability that the same sample will be re-played
        - higher probability that the next sample in the sequence will be played
        - lower probability that the next sample will be from a different song
    This assumes that the samples are in their chronological sequence.
    That is, that samples i and i+1 for a song are temporally adjacent.
    Returns a list of Samples.
    """
    if len(tracks) > len(songs):
        raise Exception('Must have more songs available than overlaid tracks')

    # Remove any songs which are simultaneously playing in other tracks
    # over the length of this bar
    min_size = min(s.min_size for s in songs)
    invalid_songs = []
    for track in tracks:
        for i in range(n / min_size):
            invalid_songs.append(track[bar_position + i].song)
    valid_songs = [s for s in songs if s not in invalid_songs]

    # ugh, well we can overlap songs, I _guess_...
    if not valid_songs:
        valid_songs = [random.choice(songs)]

    # Find samples of length n
    full_bar_samples = {}
    for song in valid_songs:
        if n in song.sizes:
            full_bar_samples[song.name] = [s for s in song[n] if s is not None]

    min_size = min(s.min_size for s in valid_songs)

    if n < min_size:
        raise Exception('Can\'t create a bar shorter than the shortest sample')

    # If this is the smallest sample size,
    # we can only return full bars.
    # Otherwise, slightly favor complete bars, if available
    if n == min_size or (full_bar_samples and random.random() <= 0.6):
        if coherent:
            return _select_sample(full_bar_samples, n, prev_sample)
        else:
            song = random.choice(full_bar_samples.keys())
            return random.choice(full_bar_samples[song])

    # Otherwise, assemble the bar from sub-bars
    bar = []
    length = 0
    while length < n:
        n_ = n / 2
        bar += build_bar(songs, n_, prev_sample=prev_sample, bar_position=bar_position, tracks=tracks)
        bar_position += n_ / min_size
        length += n_
        prev_sample = bar[-1]

    return bar


def _select_sample(samples, length, prev_sample):
    """
    Selects a sample via a markov chain
    Samples should be in the form:
        {
            'song_name': [ ... samples ... ],
            ...
        }
    """
    if prev_sample is not None:
        song = prev_sample.song

        # Repeat the sample (if it is of the needed length)
        if prev_sample.size == length and random.random() <= 0.3:
            return [prev_sample]

        # Play the next chronological sample from the song (if available)
        if random.random() <= 0.75:
            next_sample = song.next_sample(prev_sample, length)
            if next_sample is not None:
                return [next_sample]

    # Otherwise, return a random sample from a random song
    # It's possible that some songs don't have samples to choose from
    song = random.choice([k for k in samples.keys() if samples[k]])
    return [random.choice(samples[song])]


def assemble_samples(samples):
    # Assuming samples are of the same length
    # and from the same song (they should be)
    samp = next((s for s in samples if s is not None), None)

    # If this is None, that means no slices
    # successfully made it through filtering
    if samp is None:
        return [None for _ in samples]

    n = samp.size * 2
    song = samp.song

    larger_samples = []
    for i, (s1, s2) in enumerate(izip(samples[::2], samples[1::2])):
        if s1 is None or s2 is None:
            larger_samples.append(None)
        else:
            sample = Sample(s1.slices + s2.slices, song, n, i)
            larger_samples.append(sample)
    return larger_samples
