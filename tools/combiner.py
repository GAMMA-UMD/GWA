from scipy import signal
import scipy.io.wavfile
import numpy as np

def lowpass( data, high, freq, order=5 ):
    nyq = 0.5 * freq # nyquist sampling rate
    h = high / nyq

    b, a = signal.butter( order, [h], btype='lowpass' )

    return signal.lfilter( b, a, data )

def highpass( data, low, freq, order=5 ):
    nyq = 0.5 * freq # nyquist sampling rate
    l = low / nyq

    b, a = signal.butter( order, [l], btype='highpass' )

    return signal.lfilter( b, a, data )
    
def crossfilter( data1, data2, freq, crossover ):
    # Use Linkwitz-Riley crossover filter to combine audio data

    l1 = lowpass( data1, crossover, freq, 2 )
    l2 = lowpass( l1, crossover, freq, 2 )

    r1 = highpass( data2, crossover, freq, 2 )
    r2 = highpass( r1, crossover, freq, 2 )

    if np.isnan( l2 ).any():
        print( "WARNING: encountered NaN values crossfiltering left hand side, replacing with finite values" )

    if np.isnan( r2 ).any():
        print( "WARNING: encountered NaN values crossfiltering right hand side, replacing with finite values" )

    return np.nan_to_num( l2 ) + np.nan_to_num( r2 )

def hybrid_combine( fdtd_path, geo_path, cross_freq ):
    fs1, geo_wav = scipy.io.wavfile.read(geo_path)
    fs2, fdtd_wav = scipy.io.wavfile.read(fdtd_path)
    if not (fs1 == fs2):
        fdtd_wav = signal.resample(fdtd_wav, int(fs1/fs2 * len(fdtd_wav)))
        fs2 = fs1
    fs = fs1
    siglen = max([len(geo_wav), len(fdtd_wav)])
    geo_wav.resize(siglen)
    fdtd_wav.resize(siglen)
    hybrid_wav = crossfilter(fdtd_wav, geo_wav, fs, cross_freq)
    return hybrid_wav

