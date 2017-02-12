import os
import analysis
import random
import shutil
import manipulate
from glob import glob
from datetime import datetime


def preprocess(music_lib):
    files = []
    files += glob(os.path.join(music_lib, "*.mp3"))
    print "Preprocessing {} songs".format(len(files))
    for file in files:
        analysis.analyze(file)


def mix(music_lib, num_songs):
    # Make output directory
    output_dir = os.path.join('output', 'mix_{}'.format(
        datetime.now().strftime('%Y%m%d_%H%M%S')))
    sample_dir = os.path.join(output_dir, 'samples')
    if os.path.exists(output_dir) and os.listdir(output_dir):
        print "Output directory is not empty"
        return
    os.makedirs(sample_dir)

    # Shuffle songs in input directory
    tracks = []
    tracks += glob(os.path.join(music_lib, "*.mp3"))
    print "Working with library of length {}.".format(len(tracks))
    random.shuffle(tracks)

    # Pick a seed song to abse the mix around
    seed_track = tracks.pop()
    tracks = [t for t in tracks if t != seed_track]
    seed_bpm, seed_key = analysis.analyze(seed_track)
    print "Seed Track: {}".format(seed_track)
    print "Seed BPM: {}".format(seed_bpm)
    print "Seed Key: {}".format(seed_key.key)
    print "Seed scale: {}".format(seed_key.scale)

    # Search for songs that need comparatively small modifications to match
    # seed song
    assert seed_bpm is not None
    bpm_lo = 0.8 * seed_bpm
    bpm_hi = 1.20 * seed_bpm
    key_range = 6

    # Pick those songs
    selection = []
    while tracks and len(selection) < num_songs:
        track = tracks.pop()
        bpm, key = analysis.analyze(track)
        # print "Currently analyzing {}".format(track)
        if bpm_lo <= bpm <= bpm_hi and (seed_key.is_mixable(key) or abs(seed_key.distance(key)) <= key_range):
            print "Selected {}. BPM {}. Key {}{}".format(track, bpm, key.key, key.scale)
            selection.append((track, bpm, key))
        else:
            print "Skipped {}".format(track)

    # Mutate tracks + make samples
    print "Processing tracks"
    # slices = {}
    for song, bpm, key in selection + [(seed_track, seed_bpm, seed_key)]:
        filename = os.path.basename(song)
        name, ext = os.path.splitext(filename)
        print "Processing {}".format(filename)

        # Copy over files
        outfile = os.path.join(output_dir, filename)
        shutil.copy(song, outfile)
        tmpfile = os.path.join(output_dir, '{0}.tmp{1}'.format(name, ext))

        # Process as necessary
        if not seed_key.is_mixable(key):
            print "Manipulating key"
            manipulate.change_key(outfile, key, seed_key, tmpfile)
            shutil.move(tmpfile, outfile)

        if seed_bpm != bpm:
            print "Manipulating bpm"
            manipulate.change_bpm(outfile, bpm, seed_bpm, tmpfile)
            shutil.move(tmpfile, outfile)

        # Trim silence
        print "Removing silence"
        manipulate.remove_silence(outfile, tmpfile)
        shutil.move(tmpfile, outfile)

        # Slice track
        # print "Slicing"


if __name__ == '__main__':
    preprocess('input')
    mix('input', 15)
