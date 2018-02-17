import numpy as np
#import matplotlib.pyplot as plt
import scipy.io.wavfile
import scipy.fftpack
from pyaudio import PyAudio, paFloat32
import soundfile as sf
import os
#https://healthyalgorithms.com/2013/08/22/dsp-in-python-active-noise-reduction-with-pyaudio/
p = PyAudio()

rate, data = scipy.io.wavfile.read("test-mic.wav")

fft = scipy.fft(data)
fft = scipy.fftpack.fftshift(fft)

#Length is 24000, audio file is 3 seconds and rate is 8000.
print(fft)
#for i in range(len(fft)):
#    if i < len(fft) / 2:
#        fft[i] = 0
#    elif i >= len(fft) / 2 + 200:
#        fft[i] = 0

#fft now contains only some of the previous data.  ifft it back.
ifft = scipy.fftpack.ifftshift(fft)
ifft = scipy.ifft(ifft)
print(ifft)

ifft = np.asarray(ifft, dtype=np.int16)
scipy.io.wavfile.write("test-mic-clean.wav", rate, ifft)
