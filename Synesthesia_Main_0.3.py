# -*- coding: utf-8 -*-
"""
Created on Sat Aug 24 15:58:21 2019

Log

0.2 - Changed to make video from sound, create multiple frames for one audio file at given intervals
0.3 - Change background color to black and higher plot dpi 
References:
    https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files
    http://samcarcagno.altervista.org/blog/basic-sound-processing-python/?doing_wp_cron=1566799114.4202859401702880859375
    http://www.phys.nsu.ru/cherk/fft.pdf
    https://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html 
    https://stackoverflow.com/questions/10443295/combine-3-separate-numpy-arrays-to-an-rgb-image-in-python
    https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/interpolation_methods.html
    https://stackoverflow.com/questions/2878712/make-os-open-directory-in-python
@author: Vikneshan
"""
from scipy import interpolate
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
import math as mh
import time
import os
#import subprocess
#from PIL import Image
from datetime import datetime

start_time=time.time()

def sound2light(Hz):
    #convert sound frequency (hz) into light wavelength (nm)
    if Hz <= 20:
        nm=780
    elif Hz >= 20000:
        nm=380
    else:
        c=780.4004004
        m=-0.02002002002
        nm=m*Hz+c
    return nm


def RGB(nm):
    #convert light wavelength (nm) to RGB values
    nm_ref=[380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,650,655,660,665,670,675,680,685,690,695,700,705,710,715,720,725,730,735,740,745,750,755,760,765,770,775,780]
    R_ref=[97,111,121,128,131,130,126,118,106,84,61,35,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,54,74,94,112,129,146,163,179,195,210,225,240,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,246,237,228,219,209,200,190,181,171,161,151,141,130,119,109,97]
    G_ref=[0,0,0,0,0,0,0,0,0,0,0,0,0,40,70,97,123,146,169,192,213,234,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,239,223,207,190,173,155,137,119,99,79,57,33,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    B_ref=[97,119,141,161,181,200,219,237,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,203,146,84,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    f_r=interpolate.interp1d(nm_ref,R_ref)
    f_g=interpolate.interp1d(nm_ref,G_ref)
    f_b=interpolate.interp1d(nm_ref,B_ref)
    
    R=np.round_(f_r(nm),decimals=0,out=None)
    G=np.round_(f_g(nm),decimals=0,out=None)
    B=np.round_(f_b(nm),decimals=0,out=None)
    return R,G,B


def visualizationPlots(a,n,fs):    
    #Amplitude
    timeArray = np.arange(0,n,1)
    timeArray = timeArray / fs*1000
    plt.subplot(2,1,1)
    plt.plot(timeArray, a, color='k')
    plt.ylabel('Amplitude')
    plt.xlabel('Time (ms)')
    plt.title('Time domain')
    
    #Frequency
    p = fft(a)
    nUniquePts = int(mh.ceil((n+1)/2.0))
    p = p[0:nUniquePts]
    p = abs(p)
    p = p / float(n) # scale by the number of points so that
                     # the magnitude does not depend on the length 
                     # of the signal or on its sampling frequency  
    p = p**2  # square it to get the power 
    
    # multiply by two (see technical document for details)
    # odd nfft excludes Nyquist point
    if n % 2 > 0: # we've got odd number of points fft
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft
    
    freqArray = np.arange(0, nUniquePts, 1.0) * (fs / n)
    plt.subplot(2,1,2)
    plt.plot(freqArray, 10*np.log10(p), color='r')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power (dB)')
    plt.title('Frequency domain')
    
    print('RMS Value of raw signal %s'%np.sqrt(np.mean(a**2)))
    print('RMS Value of fft array %s'%np.sqrt(np.sum(p)))
    
    
def freq_dB(a,n,fs,dB_thres):
    #Frequency
    p = fft(a)
    nUniquePts = int(mh.ceil((n+1)/2.0))
    p = p[0:nUniquePts]
    p = abs(p)
    p = p / float(n) # scale by the number of points so that
                     # the magnitude does not depend on the length 
                     # of the signal or on its sampling frequency  
    p = p**2  # square it to get the power 
    
    # multiply by two (see technical document for details)
    # odd nfft excludes Nyquist point
    if n % 2 > 0: # we've got odd number of points fft
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft
    freqArray = np.arange(0, nUniquePts, 1.0) * (fs / n)
    dB=10*np.log10(p)
    loc=np.nonzero(dB>dB_thres)
    freqArray=freqArray[loc]
    dB=dB[loc]
    return freqArray, dB
    
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out

def create_image(freqArray_top5):
    R=[]
    G=[]
    B=[]
    
    n_new1=len(freqArray_top5)
    x1=mh.floor(mh.sqrt(16/9*n_new1))
    y1=mh.floor(n_new1/x1)
    l1=x1*y1 
    timestamp=str(datetime.now())
    filename='.\\VideoFolder\\'
    filename+=timestamp
    filename+='.png'
    filename=filename.replace(' ','')    
    filename=filename.replace(':','')
    freqArray_top5=freqArray_top5[:l1]
    
    for Hz in freqArray_top5:
        r,g,b=RGB(sound2light(Hz))
        R.append(r)
        G.append(g)
        B.append(b)
    
    R=np.asarray(R).reshape(y1,x1)    
    G=np.asarray(G).reshape(y1,x1)
    B=np.asarray(B).reshape(y1,x1)
    
    rgbArray = np.zeros((y1,x1,3), 'uint8')
    rgbArray[..., 0] = R
    rgbArray[..., 1] = G
    rgbArray[..., 2] = B
    
    plt.figure(dpi=1200)
    plt.imshow(rgbArray,interpolation='spline16')
    plt.style.use('dark_background')
    plt.axis('off')
    plt.savefig(filename)
    plt.close()

fs, data = wavfile.read('Melulu_rev1_viz.wav') # load the data
a_0 = data.T[0]/(2.**15) # this is a two channel soundtrack,get the first track
n_0=len(a_0)

sample_period=0.2 ### in seconds
sample_count=mh.floor(n_0/(fs*sample_period))

a_1=chunkIt(a_0,sample_count)

for a in a_1:
    freqArray_top5=np.empty([])
    n=len(a)
    freqArray, dB=freq_dB(a,n,fs,-300)
    dB_sort=np.argsort(dB)
    freqArray=freqArray[dB_sort]
    dB=dB[dB_sort]
    n_new=len(freqArray)
    x=mh.floor(mh.sqrt(16/9*n_new))
    y=mh.floor(n_new/x)
    l=x*y
    dB=dB[-l:]
    freqArray=freqArray[-l:] #only output all frequencies in order of intensity high to low
    freqArray_top5=np.append(freqArray_top5,freqArray[0:100])
    create_image(freqArray_top5)


os.startfile(os.getcwd())

print("Processing Time--- %s seconds ---" % (time.time() - start_time))