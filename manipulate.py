import subprocess


def change_bpm(file_in, from_bpm, to_bpm, file_out):
    ratio = to_bpm / from_bpm
    subprocess.call([
        'sox',
        file_in,
        file_out,
        'tempo',
        '-m',
        '--with-flac',
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
