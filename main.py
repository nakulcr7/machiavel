import os
import analysis
import random
from glob import glob


def preprocess(music_lib):
    files = []
    files += glob(os.path.join(music_lib, "*.flac"))
    print "Preprocessing {} songs".format(len(files))
    exit(0)
    # for file in files:
    # analysis.analyze(file)


def mix(music_lib):
    # Make output directory

    # Shuffle songs in input directory
    tracks = []
    tracks += glob(os.path.join(music_lib, "*.flac"))
    print "Working with library of length {}.".format(len(tracks))
    random.shuffle(tracks)

    # Pick a seed song to abse the mix around
    seed_track = tracks.pop()
    tracks = [t for t in tracks if t != seed_track]
    seed_bpm, seed_key = analysis.analyze(seed_track)
    print "Seed Track: {}".format(seed_track)
    print "Seed BPM: {}".format(seed_bpm)
    print "Seed Key: {}".format(seed_key)

    # Search for songs that need comparatively small modifications to match
    # seed song
    bpm_lo = 0.8 * seed_bpm
    bpm_hi = 1.20 * seed_bpm
    key_range = 6

    # Pick those songs
    selection = []
    while tracks and len(selections) < n:
        track = tracks.pop()
        bpm, key = analysis.analyze(track)
        print "Currently analyzing {}".format(track)
        if bpm_lo <= bpm <= bpm_hi and (seed_key.mixable(key) or abs(seed_key.distance(key)) <= key_range):
            print "Selected"
            selection.append((track, bpm, key))
        else:
            print "Skipped"


if __name__ == '__main__':
    preprocess('input')
