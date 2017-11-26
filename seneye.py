# Seneye talking

import urllib2
import seneye_login
	
seneyeurl = seneye_login.seneyeurl()

#download the data:
file = urllib2.urlopen(seneyeurl)

#convert to string:
data = file.read()
#close file because we dont need it anymore:
file.close()

#print data

#split the raw data into an array split on comma
text = data.split(',')

#select the values needed and set as variables
temperature = text[4]
ph = text[10]
nh3 = text[16]
#light = text[20]

#temperature - strip off extra characters not needed
temperature = temperature.replace('"','')
temperature = temperature.replace('curr:','')
print temperature

#ph - strip off extra characters not needed
ph = ph.replace('"','')
ph = ph.replace('curr:','')
print ph

#nh3 - strip off extra characters not needed
nh3 = nh3.replace('"','')
nh3 = nh3.replace('curr:','')
print nh3

#light - strip off extra characters not needed
#light = light.replace('"','')
#light = light.replace('curr:','')
#print light
