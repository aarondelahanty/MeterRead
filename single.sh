#!/bin/bash
DATE=$(date +"%Y-%m-%d_%H%M")
raspistill -v -vf -hf -co 70 -ISO 800 -roi .42,.2,.39,1 -ss 5000000 -o /var/www/html/images/meter0001.jpg
raspistill -v -vf -hf -co 70 -ISO 800 -roi .42,.2,.39,1 -ss 5000000 -o /home/pi/MeterRead/meter0001.jpg
#scp /home/pi/MeterRead/meter.jpg aaron@192.168.0.198:C:/Users/aaron/Meter
#time parameter (ms)  following -tl is frequency of capture (e.g. 400000 = 6min)
#time parameter (ms) following -t is the total time overwhich captures are acquired (e.g. 30,000,000 = 8hr)

