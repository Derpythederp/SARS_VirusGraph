#!/usr/bin/env python


import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import pandas as pd

#import dataset 
sarsdata=pd.read_excel('assets/sars_final.xlsx')
sarsdata['Date'] =  pd.to_datetime(sarsdata['Date']).dt.date


#Print sars data
print(sarsdata.head(10))
print(sarsdata.shape)
print('Peak Infected at: {}'. format(sarsdata['Infected'].max()))
print('Peak Mortality at: {}'.format(sarsdata['Mortality'].max()))



#Creating circular bar chart
plt.style.use('seaborn')

number = sarsdata.shape[0]#number of bars to plot
bottom=400
scale= 0.1 #scale each data value by this factor, 0.1 is in tenths, 0.01 is in hundredths
#scale cannot be too small since will neglect smaller extremes

infected_ser=sarsdata['Infected']
mortality_ser=sarsdata['Mortality']


theta = np.linspace(0.0, 2 * np.pi, number, endpoint=False)
infected_radii = infected_ser * scale
mortality_radii= mortality_ser
width = (2*np.pi) / number #circumference/no. of data

graph=plt.figure(figsize=(15,15))

#Infected subplot
ax1 = graph.add_subplot(1,2,1, polar=True)
bars1 = ax1.bar(theta, infected_radii, width=width, bottom=bottom)

#Mortality subplot
ax2 = graph.add_subplot(1,2,2, polar=True)
bars2 = ax2.bar(theta, mortality_radii, width=width, bottom=bottom)

# Use custom colors and opacity

colors = [ plt.cm.jet(x) for x in np.linspace(0.4, 0.85, number) ]
for c, bar in enumerate(bars1):
    bar.set_facecolor(colors[c])
    bar.set_alpha(0.9)

for c,bar in enumerate(bars2):
    bar.set_facecolor(colors[c])
    bar.set_alpha(0.9)
    
    
#custom labelling- namely the names of graphs
ax1.set_title('2003 Sars Infected (per 10 patients)',pad=25.0, fontsize= 20)
ax2.set_title('2003 Sars Mortality (per patient)', pad=25.0, fontsize= 20)
ax1.set_xticks([],[]) #remove x-ticks which show polar coordinates
ax2.set_xticks([],[])

#set yticks outwards to compensate for bottom (i.e inner radius)
#problem: cannot set yticks through set_yticks as set_yticks only handles removing the unlisted values in the list given
#must use yticks() which returns locations of labels (locs) and labels at said location(labels)

plt.sca(ax1) #sca tells the code to focus onto subplot 1
plt.yticks(np.arange(0,1100+bottom,100))
locs, labels = plt.yticks()
#locs is [   0  100  200  300  400  500  600  700  800  900 1000 1100 1200 1300 1400]
labels= [int(item)-bottom for item in locs]#new list of labels made 
labels=[item if item>=0 else None for item in labels] #yeet the negatives outta the window
#Note: Format is     {success outcome} if {condition} else {fail outcome} for {element} in {iterable}
plt.yticks(locs, labels) #replace locs by new labels 

plt.sca(ax2)
plt.yticks(np.arange(0,1100+bottom,100))
locs, labels = plt.yticks()
#locs is [400.0, 600.0, 800.0, 1000.0, 1200.0, 1400.0]
labels= [int(item)-bottom for item in locs]#new list of labels made 
labels=[item if item>=0 else None for item in labels]
plt.yticks(locs, labels) #replace locs by new labels 



#set dates onto each bar
#theta is angle, theta +90 = direction of words
#implement vectorization using pandas/numpy for speed and less glitchy 

spacer= 400 #spacer decides how much extra space is given to the label name

'''for c2 ,bar in enumerate(bars1):
#failed implementation
    x= (infected_radii[c2] +bottom + spacer) *(np.sin(theta[c2]))
    y= (infected_radii[c2] +bottom + spacer) *(np.cos(theta[c2]))
    s= sarsdata['Infected'][c2]
    rotation= theta[c2] + np.pi/2
    ax1.text(x=x,y=y,s=s,fontsize=10, rotation= rotation)'''

'''Version 2: Failed due to lack of understanding of what ax1.text does

x= np.around((infected_radii.values + bottom +spacer)* np.sin(theta)).astype(int)
y= np.around((infected_radii.values + bottom +spacer)* np.cos(theta)).astype(int)
#finite data required, np.around rounds the values(more accurate than astype directly), while astype converts to int
s= sarsdata['Date'].values
rotation= (theta/np.pi *180)
'''



'''ax.text has x as angles in radian due to polar, y is literally y+bottom, s as string, rotation as rotation in degrees with
zero as horizontal while 90 as vertical. These angles are relative to offset
Meanwhile, theta variable is in radians, so it is x,
y is basically the number (infected_ser+bottom)*scale+spacer OR mortality+spacer+bottom,
s is the same sarsdata['Date'][index of desire]
rotation is x/np.pi * 180 +90
'''
#define label locations with numpy
x=theta #already nparray
#y=(infected_ser.values*scale) +spacer+bottom
y= np.full(96, 1500)
s=sarsdata['Date']
rotation=((x/np.pi) *180)+90

#implement labels
for i in range(0,96):
    ax1.text(x=x[i],y=y[i], s=s[i], rotation=rotation[i],horizontalalignment='center', verticalalignment='center')

for i in range(0,96):
    ax2.text(x=x[i],y=y[i], s=s[i], rotation=rotation[i],horizontalalignment='center', verticalalignment='center')


#Zero to top of polar graph
ax1.set_theta_offset(np.pi/2) 
ax2.set_theta_offset(np.pi/2) 

#plt.savefig('First 96 days of the 2003 Sars Virus.pdf')
plt.show()




