# Radar_RaDICaL_Simplified
Test that, based on the test file of the dataset https://github.com/moodoki/radical_sdk?tab=readme-ov-file, attempts to detect targets with an indication of their distance.

Download the project to disk:

Download the file with 50 tests from https://fireball.teckyianlim.me/file/flaming-cake/indoor_sample_50.h5

Run the test program:

python Test_Radar_RaDICal_Simplfied.py

The program initially has two parameters: FifMax and FifMin to select the intermediate frequency range; by adjusting them, a balance can be achieved between detecting targets and avoiding interference.

The Texas manual, mmwaveSensing-FMCW-offlineviewing_0 .pdf, is attached. that has been followed in this test, specifically the explanations on page 4

References:

https://github.com/itberrios/radical/blob/main/notebooks/range_doppler.ipynb

https://medium.com/@itberrios6/introduction-to-radar-part-2-8a332066917e

Dataset from
https://publish.illinois.edu/radicaldata/

https://github.com/moodoki/radical_sdk

a A small sample (50 frames) to try things from
https://fireball.teckyianlim.me/file/flaming-cake/indoor_sample_50.h5

https://www.ti.com/lit/an/swra553a/swra553a.pdf?ts=1714172430750

Does not provide dataset for try
https://www.plextek.com/articles/a-programmers-introduction-to-processing-imaging-radar-data/
https://www.radartutorial.eu/10.processing/sp04.en.html
