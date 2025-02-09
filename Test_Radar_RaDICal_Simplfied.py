
#  Alfonso Blanco, january 2025


# Dtaset from
# https://publish.illinois.edu/radicaldata/
# https://github.com/moodoki/radical_sdk  a A small sample (50 frames) to try things from
# https://fireball.teckyianlim.me/file/flaming-cake/indoor_sample_50.h5

# PARAMETERS ####################################################
FifMax=77080.0 # Mhz intermediate frecuency max
FifMin=77035.0 # Mhz intermediate frecuency min

FactorDetectMoving=1.7

# speed of wave propagation
c = 299792458.0# m/s
Finicial= 77000 # Mhz

#The Slope (S) of the chirp defines the rate at which the chirp ramps up.
#In this example the chirp is sweeping a bandwidth of 4GHz in 40us which corresponds to a Slope of 100MHz/us
S=100 #MHz/us
S=100*10e6 # Mhz/sec
# t=(Fif - Finicial) / S # us
# d=t * 10e-6* c/2 # meters

#Idle_time= 58.0 / 1000000.0 # sec # not used
#ADC_sample_rate= 9499.0 # Msps samples per second # not used

DATA_PATH = "indoor_sample_50.h5"

#############################################################################
# the speed of a person is betwenn 1,11 m/s and 1,66m/s
# experimentally supossing the persons in the frame 0 image has a speed of 1,2  m/s
# the factor aplied to the cocient of phases from two consecutive chirps
# would be:
FactorPhaseVariation=1.2/0.54

import h5py
import numpy as np
import matplotlib.pyplot as plt
import cmath

data_dict = {}
with h5py.File(DATA_PATH, 'r') as h5_obj:

    for key in h5_obj.keys():
        print(key, 'shape: ', h5_obj[key].shape)
        data_dict.update({key : np.asarray(h5_obj[key])})

#print(data_dict['radar'].shape)

# Now we have the data stored in a dictionary,
# let’s go ahead and access a random frame of raw Radar data.
for data_idx in range (50): 
    
    adc_data = data_dict['radar'][data_idx, ...]

    # 
    # https://github.com/itberrios/radical/blob/main/notebooks/range_doppler.ipynb
    # https://medium.com/@itberrios6/introduction-to-radar-part-2-8a332066917e
    #

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
    

    # Moving from time domain to frequency domain using FFT
        
    range_cube = np.fft.fft(adc_data, axis=2)
    
    # https://stackoverflow.com/questions/33846123/when-should-i-use-fftshiftfftfftshiftx-and-when-fftx
    range_cube = np.fft.fftshift(np.fft.fft(range_cube, axis=2), axes=2)

    Tab_r=[]

    Tab_angle=[]
    
    Tab_angle1=[]
    
    strDistance=""
    
    # for each chirp in radar frame
    for i in range(range_cube.shape[0]):

        # for each antena in a chirp
        for j in range (range_cube.shape[1]):
            #range_bin_chirps = range_cube.sum(axis=1) # MOD

            # for each frecuency (component) of a chirp in an antenna
            for k in range(range_cube.shape[2]): #MOD
                
                 r, phi= cmath.polar(range_cube[i][j][k])

                 
                 # In order to avoid interferences limit distance by mean of intermediate frecuency  
                 if r > FifMax: continue
                 if r < FifMin: continue
                 
                                 
                 angle = np.angle(range_cube[i][j][k], deg=True)
                 
                 # To avoid interference, only moving targets are considered.
                 # Moving targets are detected if there are phase shift between two consecutive chirp 
                 #
                 angle1=0
                 SwPasa=0
                 if i > 0:
                      angle1=np.angle(range_cube[i-1][j][k], deg=True)
                      #print(" angle " + str(angle) + " angle ant= " + str(angle1))
                      r1, phi1= cmath.polar(range_cube[i-1][j][k])
                      t1=(r1 - Finicial) / S # us
                      d1= (t1 *  c)/(2* 1000000.0) # meters
                      
                 # negative phases are no considered
                 if angle1 <= 0 : continue
                 
                 if angle1 < angle:     
                    if angle1*FactorDetectMoving < angle:                     
                      SwPasa=1
                 if angle < angle1:     
                    if angle1*FactorDetectMoving < angle1:
                      SwPasa=1     
                 
                 if SwPasa==0: continue
                 #print (" Fif = " + str(r) + " angle = " + str(angle)[0:4] + " Fif ant= " + str(r1) + " angle chirp ant = " + str(angle1)[0:4] )
                 #print (" Fif = " + str(r) + " phase = " + str(phi)[0:4]+ " Fif ant= " + str(r1) + " phase chirp ant = " + str(phi1)[0:4] )  

                 # the cocient of phases is the same for objects with almost the the same speed
                 # for that is asumed to be a mean to get the speed
                 phi_variation=phi1/phi
                                 
                 #print (" Phase variation " + str(phi_variation)[0:4])
                 
                 Tab_r.append(r)
      
                 #Tab_phi.append(phi)

                 Tab_angle.append(angle)

                 Tab_angle1.append(angle1)
      
                
                 t=(r - Finicial) / S # us
                 d= (t *  c)/(2* 1000000.0) # meters
                 #print (" distance = " +str(d)[0:6])
                 strDistance=strDistance +str(d)[0:6] + " meters  - "

                 # Experimentally, if the phase variation between two consecutive chirps is less then 0.5
                 # speed can not be determined

                 if phi_variation > 0.5:
                     speed = phi_variation * FactorPhaseVariation
                     
                     #print (" speed = " +str(speed))
                                       
                     strDistance= strDistance + " speed = " +str(speed)[0:4] + " m/s  - "

                 else:
                     
                     strDistance= strDistance + " speed  cannot be determined" 
                 
                    
    rgb_image = data_dict['rgb'][data_idx, ...]

    fig, ax = plt.subplots(1, 2, figsize=(15, 5))

    fig.suptitle("distances and speed = "+ strDistance )

    
    ax[0].imshow(rgb_image)
    ax[0].set_title("Frame " + str(data_idx))
    ax[1].set_ylabel("Fif Mhz")
    ax[1].set_xlabel("Phase angle degres");
    ax[1].scatter(Tab_angle, Tab_r, **{'color': 'lightsteelblue', 'marker': 'o'})    
    
    plt.show()

   
