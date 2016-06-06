import matplotlib
matplotlib.use('TkAgg')

import numpy as np
import scipy
from scipy.io.wavfile import read
import struct
import wave
import pyaudio
import threading
import pylab

class Audio_Analysis:
  def __init__(self):
    # Initial Setup
    self.nFFT = 512
    self.RATE = 48100
    self.BUFFERSIZE = 2**13 
    self.CHANNELS = 2
    self.S_SIZE = 2
    self.recordSecond = .05
    self.threadsStatus = False
    self.audioStatus = False

    # Setting Up Real-Time Mic
    self.buffersToRecord = int(self.RATE*self.recordSecond/self.BUFFERSIZE)
    if self.buffersToRecord == 0: self.buffersToRecord = 1

    self.recordSamples = int(self.BUFFERSIZE*self.buffersToRecord)
    self.recordChunks = int(self.recordSamples/self.BUFFERSIZE)
    self.secPerPoint = 1.0/self.RATE

    self.p = pyaudio.PyAudio()
    self.inStream = self.p.open(format=pyaudio.paInt16, 
                                channels=1, 
                                rate=self.RATE, 
                                input=True, 
                                frames_per_buffer=self.BUFFERSIZE)
    self.xsBuffer = np.arange(self.BUFFERSIZE)*self.secPerPoint
    self.xs = np.arange(self.recordChunks*self.BUFFERSIZE)*self.secPerPoint
    self.audio = np.empty((self.recordChunks*self.BUFFERSIZE), dtype=np.int16)
   
    # Setting up PlayBack Data 
    self.wavFile = 'Adele_vs_Madcon_-_Set_Fire_To_The_Beggin_Rain.wav'

    self.wf = wave.open(self.wavFile, 'rb')
    self.frames = self.wf.getnframes()
    

  def close(self):
    self.p.close(self.inStream)

  def getAudio(self):
    # Stores the Audio from the microphone
    audioString = self.inStream.read(self.BUFFERSIZE)
    return np.fromstring(audioString, dtype=np.int16)

  def record(self, forever=True):
    # Returns the Audio from the microphone
    while True:
      if self.threadsStatus: break
      for i in range(self.recordChunks):
        self.audio[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE]=self.getAudio()
        self.audioStatus = True
        if forever == False: break

  def continuousStart(self):
    #Continuously Record the Mic Data
    self.t = threading.Thread(target=self.record)
    self.t.start()

  def continuousEnd(self):
    #Pause Mic Recording
    self.threadsStatus = True
  
  #Fast Fourier Transform
  def fft(self, data, trimBy=10, logScale=False, divBy=100):
    left, right = np.split(np.abs(np.fft.fft(data)), 2)
    ys = np.add(left, right[::-1])

    if logScale:
      ys = np.multiply(20, np.log10(ys))
    xs = np.arange(self.BUFFERSIZE/2, dtype=float)

    if trimBy:
      i = int((self.BUFFERSIZE/2)/trimBy)
      ys = ys[:i]
      xs = xs[:i]*self.RATE/self.BUFFERSIZE

    if divBy:
      ys = ys/float(divBy)

    return xs, ys
  
  #Grabs the FFT of the Mic Frequency 
  def realtimeFFT(self):
    rtData = self.audio.flatten()

    x, y = self.fft(rtData, logScale=True, divBy=1)
    return x, y

  #def getWFAudio(self):
  #  self.wfStr = self.wf.readframes(self.BUFFERSIZE)
  #  return np.fromstring(self.wfStr, dtype=np.int16)

  #def getPlayback(self):
  #  for i in range(2170*self.recordChunks):
  #    self.audio2[i*self.BUFFERSIZE:(i+1)*self.BUFFERSIZE] = self.getWFAudio()
  #    self.stream2.write(self.wfStr)

  #def playbackFFT(self):
  #  songlen = 2170
  #  self.counter = 0

  #  if self.counter < 2170:
  #    tempArr = self.audio2[self.counter*self.BUFFERSIZE:(self.counter+1)*self.BUFFERSIZE]
  #    tempArr = tempArr.flatten()
  #    self.counter += 1
  #    print self.counter

  #    x, y = self.fft(tempArr, logScale=True)

  #  return x, y
      
  def plotAudio(self):
    pylab.plot(self.audio.flatten())
    pylab.show()
