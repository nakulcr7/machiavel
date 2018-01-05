import os
import math
import analysis
import random
import shutil
import manipulate
from glob import glob
from datetime import datetime
from song import Song
from sample import Slice
import producer


def preprocess(music_lib):
    files = []
    files += glob(os.path.join(music_lib, "*.flac"))
    print "Preprocessing {} songs".format(len(files))
    for file in files:
        analysis.analyze(file)


def mix(music_lib, num_songs, min_sample_size=16, max_sample_size=32):
    n_l = math.log(min_sample_size, 2)
    n_u = math.log(max_sample_size, 2)
    sample_sizes = [2**n for n in range(int(n_l), int(n_u) + 1)]

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
    tracks += glob(os.path.join(music_lib, "*.flac"))
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
            # print "Skipped {}".format(track)
            pass

    # Mutate tracks + make samples
    print "Processing tracks"
    slices_dict = dict()
    for song, bpm, key in selection + [(seed_track, seed_bpm, seed_key)]:
        filename = os.path.basename(song)
        name, ext = os.path.splitext(filename)
        print "Processing {}".format(filename)

        # Copy over files
        file_out = os.path.join(output_dir, filename)
        shutil.copy(song, file_out)
        file_temp = os.path.join(output_dir, '{0}.tmp{1}'.format(name, ext))

        # Process as necessary
        if not seed_key.is_mixable(key):
            print "Manipulating key"
            manipulate.change_key(file_out, key, seed_key, file_temp)
            shutil.move(file_temp, file_out)

        if seed_bpm != bpm:
            print "Manipulating bpm"
            manipulate.change_bpm(file_out, bpm, seed_bpm, file_temp)
            shutil.move(file_temp, file_out)

        # Trim silence
        print "Removing silence"
        manipulate.remove_silence(file_out, file_temp)
        shutil.move(file_temp, file_out)

        # Slice track
        print "Slicing track"
        beats = analysis.estimate_beats(file_out)

        track_sample_dir = os.path.join(sample_dir, name)
        os.makedirs(track_sample_dir)

        prefix = '{0}_{1}_'.format(name, min_sample_size)
        # slices_dict[name] = manipulate.slice_track(file_out,
        #                                            beats,
        #                                            min_sample_size,
        #                                            track_sample_dir,
        #                                            prefix=prefix)

        slices_dict[name] = [Slice(f) for f in manipulate.slice_track(file_out,
                                                                      beats,
                                                                      min_sample_size,
                                                                      track_sample_dir,
                                                                      prefix=prefix)]

    # Remove samples that have irregular duration
    slices_dict = manipulate.filter_slices(slices_dict)

    # Build songs + samples out of the slices
    # Some songs may return no slices, in which case, ignore that song.
    songs = [Song(nm, slics, sample_sizes) for nm, slics in slices_dict.items() if any(s is not None for s in slics)]

    # Select samples and assemble tracks
    print "Assembling tracks"
    tracks, tracklist = producer.produce_tracks(songs, output_dir)

    # Overlay the tracks
    print "Assembling mix"

    mix_file = os.path.join(output_dir, '_mix.mp3')
    producer.produce_mix(tracks, mix_file, format='mp3')

    # Write the tracklist
    tracklisting = '\n\n---\n\n'.join(['\n'.join(['{0}\t{1}'.format(t, s) for t, s in tl]) for tl in tracklist])
    trl_file = os.path.join(output_dir, '_tracklist.txt')
    with open(trl_file, 'w') as f:
        f.write(tracklisting)

    print "The new machiavel track just dropped ~ (done)"


if __name__ == '__main__':
    preprocess('input')
    mix('input', 15)
