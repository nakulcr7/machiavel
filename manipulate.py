import subprocess
import os
from collections import defaultdict
from analysis import duration


def change_bpm(file_in, from_bpm, to_bpm, file_out):
    ratio = to_bpm / from_bpm
    subprocess.call([
        'sox',
        file_in,
        file_out,
        'tempo',
        '-m',
        # '--with-flac',
        str(ratio)
    ])
    return file_out


def change_key(file_in, from_key, to_key, file_out):
    semitones = from_key.distance(to_key)
    cents = semitones * 100
    subprocess.call([
        'sox',
        file_in,
        file_out,
        'pitch',
        str(cents)
    ])
    return file_out


def remove_silence(file_in, file_out):
    """
    Trim silence from the song's beginning
    <http://digitalcardboard.com/blog/2009/08/25/the-sox-of-silence/>
    """
    subprocess.call([
        'sox',
        file_in,
        file_out,
        'silence',
        '1',
        '0.1',
        '1%'
    ])
    return file_out


def _slice(file_in, t_start, t_end, file_out):
    subprocess.call([
        'ffmpeg',
        '-i',
        file_in,
        '-ss',
        str(t_start),
        '-to',
        str(t_end),
        file_out
    ])
    return file_out


def slice_track(file_in, beats, slice_size, dir_out, prefix=''):
    files_out = []
    slices = [beats[i:i + slice_size]
              for i in range(0, len(beats), slice_size)]
    slice_ranges = [(s[0], s[-1]) for s in slices]

    for i, (t_start, t_end) in enumerate(slice_ranges):
        file_out = "{0}{1}.{2}".format(prefix, i, 'flac')
        file_out = os.path.join(dir_out, file_out)
        file_out = _slice(file_in, t_start, t_end, file_out)

        if os.path.exists(file_out):
            files_out.append(file_out)
    return files_out


def filter_slices(slices_dict):
    durations_dict = defaultdict(list)
    for track, slices in slices_dict.items():
        for s in slices:
            d = duration(s.file)
            durations_dict[d].append(s)

    d_with_max_slices = max(durations_dict.keys(),
                            key=lambda k: len(durations_dict[k]))

    for track, slices in slices_dict.iteritems():
        slices_dict[track] = [s if s in durations_dict[
            d_with_max_slices] else None for s in slices]

    return slices_dict
