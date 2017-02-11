from models.key import Key
from essentia import Pool, streaming, run


def get_bpm(file_in):


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
