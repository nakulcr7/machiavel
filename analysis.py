from models.key import Key
from essentia import Pool, streaming, run
from database import save, load


def analyze(file_in):
    """
    Returns (bpm, Key) after analyzing the given audio file
    """
    data = load(file_in)
    if data is not None:
        bpm, key, scale = data
        return bpm, Key(key, scale)
    bpm = get_bpm(file_in)
    key = get_key(file_in)
    save(file_in, bpm, key)
    return bpm, key


def get_bpm(file_in):
    pool = Pool()

    loader = streaming.MonoLoader(filename=file_in)
    bt = streaming.RhythmExtractor2013()
    bpm_histogram = streaming.BpmHistogramDescriptors()
    # BPM histogram output size is 250
    centroid = streaming.Centroid(range=250)

    loader.audio >> bt.signal
    bt.bpm >> (pool, 'bpm')
    bt.ticks >> None
    bt.confidence >> (pool, 'confidence')
    bt.estimates >> None
    bt.bpmIntervals >> bpm_histogram.bpmIntervals
    bpm_histogram.firstPeakBPM >> (pool, 'bpm_first_peak')
    bpm_histogram.firstPeakWeight >> None
    bpm_histogram.firstPeakSpread >> None
    bpm_histogram.secondPeakBPM >> (pool, 'bpm_second_peak')
    bpm_histogram.secondPeakWeight >> None
    bpm_histogram.secondPeakSpread >> None
    bpm_histogram.histogram >> (pool, 'bpm_histogram')
    bpm_histogram.histogram >> centroid.array
    centroid.centroid >> (pool, 'bpm_centroid')

    run(loader)
    return pool['bpm']


def get_key(file_in):
    """
    Estimates the key and scale for an audio file.
    """
    loader = streaming.MonoLoader(filename=file_in)
    framecutter = streaming.FrameCutter()
    windowing = streaming.Windowing(type="blackmanharris62")
    spectrum = streaming.Spectrum()
    spectralpeaks = streaming.SpectralPeaks(orderBy="magnitude",
                                            magnitudeThreshold=1e-05,
                                            minFrequency=40,
                                            maxFrequency=5000,
                                            maxPeaks=10000)
    pool = Pool()
    hpcp = streaming.HPCP()
    key = streaming.Key()

    loader.audio >> framecutter.signal
    framecutter.frame >> windowing.frame >> spectrum.frame
    spectrum.spectrum >> spectralpeaks.spectrum
    spectralpeaks.magnitudes >> hpcp.magnitudes
    spectralpeaks.frequencies >> hpcp.frequencies
    hpcp.hpcp >> key.pcp
    key.key >> (pool, 'tonal.key_key')
    key.scale >> (pool, 'tonal.key_scale')
    key.strength >> (pool, 'tonal.key_strength')

    run(loader)

    return Key(pool['tonal.key_key'], pool['tonal.key_scale'])
