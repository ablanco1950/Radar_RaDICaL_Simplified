# Radar_RaDICaL_Simplified
Test that, based on the test file of the dataset https://github.com/moodoki/radical_sdk?tab=readme-ov-file, attempts to detect targets with an indication of their distance.

Download the project to disk:

Download the file with 50 tests from https://fireball.teckyianlim.me/file/flaming-cake/indoor_sample_50.h5

Run the test program:

python Test_Radar_RaDICal_Simplfied.py

As this is a room, to avoid waves reflected by walls and others:

- Distances are limited  by limiting  intermediate frecuency

- Only moving targets are considered. Moving targets are detected by the phase shift between one chirp component and the same component
  in the previous chirp detected by the same antenna.

The Texas manual, mmwaveSensing-FMCW-offlineviewing_0 .pdf, is attached. that has been followed in this test, specifically the explanations on page 4 and page 28

References:

https://github.com/itberrios/radical/blob/main/notebooks/range_doppler.ipynb

https://medium.com/@itberrios6/introduction-to-radar-part-2-8a332066917e

Dataset from
https://publish.illinois.edu/radicaldata/

https://github.com/moodoki/radical_sdk


https://fireball.teckyianlim.me/file/flaming-cake/indoor_sample_50.h5
Is one small sample (50 frames) to try.

https://www.ti.com/lit/an/swra553a/swra553a.pdf?ts=1714172430750

https://www.plextek.com/articles/a-programmers-introduction-to-processing-imaging-radar-data/
But does not provide dataset for try:

https://www.radartutorial.eu/10.processing/sp04.en.html

https://moodoki.github.io/radical_sdk/ProjectBBoxExample.html
It seems to be limited to detecting objects in radar photos and does not use radar signals. In a similar way to that used in https://github.com/ablanco1950/Radar_Marine-Yolov11 wich uses photos of screen radar.
Would be computer vision projects rather than signal processing
