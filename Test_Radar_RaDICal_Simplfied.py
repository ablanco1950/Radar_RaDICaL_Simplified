#  Alfonso Blanco, january 2025

# References
# https://github.com/itberrios/radical/blob/main/notebooks/range_doppler.ipynb
# https://medium.com/@itberrios6/introduction-to-radar-part-2-8a332066917e
#
# Dtaset from
# https://publish.illinois.edu/radicaldata/
# https://github.com/moodoki/radical_sdk  a A small sample (50 frames) to try things from
# https://fireball.teckyianlim.me/file/flaming-cake/indoor_sample_50.h5

# PRAMETERS
FifMax=77095 # Mhz intermediate frecuency max
FifMin=77020 # Mhz intermediate frecuency min

# speed of wave propagation
c = 299792458 # m/s

#The Slope (S) of the chirp defines the rate at which the chirp ramps up.
#In this example the chirp is sweeping a bandwidth of 4GHz in 40us which corresponds to a Slope of 100MHz/us
S=100 #MHz/us
S=100/10e-6 # Mhz/s
# d=(Fif*c)/ ( 2*S)

DATA_PATH = "indoor_sample_50.h5"

import h5py
import numpy as np
import matplotlib.pyplot as plt
import cmath

data_dict = {}
with h5py.File(DATA_PATH, 'r') as h5_obj:

    for key in h5_obj.keys():
        print(key, 'shape: ', h5_obj[key].shape)
        data_dict.update({key : np.asarray(h5_obj[key])})

print(data_dict['radar'].shape)

# Now we have the data stored in a dictionary,
# let’s go ahead and access a random frame of raw Radar data.
for data_idx in range (50): 
    
    adc_data = data_dict['radar'][data_idx, ...]

    # We call this ADC data because it is the output of the Analog to Digital Converter (ADC) in the Radar.

    #print(adc_data.shape)
    #print(adc_data)

    # the print is (32, 8, 304)

    #Our data is 3D and is sometimes referred to as the Radar cube.
    #The first dimension is the number of chirps in a Radar frame,
    #this is also the number of Doppler Velocity bins we have.
    #The second dimension is the number of virtual receive antennas,
    # in this case we have a Uniform Linear Array (ULA) of 8 receive antennas.
    # The third dimension is the number of ADC samples which is also the number of range bins.

    #     -Number of ADC samples → Number of Range Bins
    #     - Number of Chirps → Number of Doppler Velocity Bins
    # Let’s go ahead and process the Range data, to do this we take the FFT across all of the ADC samples.
    # We can display the Range Cube data by summing across all the antennas,
    # then take the log of the magnitude for better visualization in Decibels (dB).

    #Process Range
    range_cube = np.fft.fft(adc_data, axis=2).transpose(2, 1, 0)

    range_cube = np.fft.fftshift(np.fft.fft(range_cube, axis=2), axes=2)

    #range_cube2= 10*np.log10( np.abs(range_cube)**2 ).sum(axis=1).T
       
    range_cube1=range_cube.flatten()
    
    Tab_r=[]
    Tab_phi=[]
    strDistance=""
   
    for i in range(len(range_cube1)):
     
      r, phi= cmath.polar(range_cube1[i])
      
      if r > FifMax: continue
      if r < FifMin: continue
      
      Tab_r.append(r)
      
      Tab_phi.append(phi)
      d=(r*c)/ ( 2*S * 1000000.0)
      print (" distance = " +str(d))
      strDistance=strDistance +str(d) + " - "
      #d=10*np.log10( d**8 )
      #print (" distance log = " +str(d))
   
    rgb_image = data_dict['rgb'][data_idx, ...]

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    fig.suptitle("distances = "+ strDistance )

    #ax.imshow(rgb_image)
    #ax.set_title("Frame " + str(data_idx))
    ax[0].imshow(rgb_image)
    ax[0].set_title("Frame " + str(data_idx))
    ax[1].plot(Tab_phi, Tab_r, **{'color': 'lightsteelblue', 'marker': 'o'})
    

    plt.show()

   
