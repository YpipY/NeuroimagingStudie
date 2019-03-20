# -*- coding: utf-8 -*-


#This fMRI experiment on animate inanimate distinction

#############  IMPORT MODULES  ################################
from __future__ import division
from psychopy import core, visual, event, gui, data, monitors
from itertools import product
from random import shuffle
from PIL import Image
import pandas as pd
import os
import numpy as np 
import glob
#Not sure all of these are needed

############  SET MONITOR VARIABLES ###########################
# Monitor parameters
MON_distance = 60  # Distance between subject's eyes and monitor 
MON_width = 34  # Width of your monitor in cm
MON_size = [1920, 1080]  # Pixel-dimensions of your monitor, width / height
MON_frame_rate = 60 # Hz: usually 60, but you can always check with the function getActualFrameRate

# Create monitor
my_monitor = monitors.Monitor('testMonitor', width=MON_width, distance=MON_distance)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_size)

############# GET PARTICIPANT INFO USING GUI ###########################
popup = gui.Dlg(title = 'animate inanimate distinction')            # The titel of the box
popup.addField('ID: ')                               # Imput for alias to distinguish between participants
popup.addField("age: ")
popup.addField("gender: ", choices=['female','male', "other"])
popup.addField("Scanner: ", choices=['Prisma','Skyra'])
popup.addField("Scan day: ", choices=['Tuesday','Wednesday'])
popup.show()                                            # Shows the popup
if popup.OK:                                            # If there is imput in the popup, then it is saved to ID
    EXP_info = popup.data
elif popup.Cancel:                                      # If not the program is closed
    core.quit()

############# INITIALIZE WINDOW ###########################
# Initialize window for stimulus presentation
win = visual.Window(monitor = my_monitor,
                    units = 'deg',
                    fullscr = True, # Set to True
                    allowGUI = False, 
                    color = 'white')  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!

############# PREPARE STIMULI ################################
# Experiment details:
# 2x2 blocks, 15 stims each. 30 sec break 2 repetitions

# Timing details
STIM_dur = int(2 * MON_frame_rate) # Duration of stimuli. No idea why 0.2 is 2 sec (2 sec)
STIM_bloks = 2 # Number bloks
STIM_break = int(0 * MON_frame_rate) # Break between bloks (30 sec)
STIM_rep = 6 # Number of repetitions of the bloks

# The image size and position using ImageStim, file info added in trial list below.
STIM_image = visual.ImageStim(win,
    mask=None,
    pos=(0.0, 0.0), # Should be default
    size=(14.0, 10.5),
    ori=1)

# Prepare Fixation cross, i.e. just the character "+".
STIM_fix = visual.TextStim(win, '+',color='black')

############# RESPONSES AND OTHER COMMANDS ################################
# Relevant keys
KEYS_quit = ['escape']  # Keys that quits the experiment
KEYS_trigger = ['t'] # The MR scanner sends a "t" to notify that it is starting
KEYS_response = ['y', 'b'] # Yellow and blue buttons on response box

############# OUTPUT LOGFILE ################################
# Define output folder
OUTPUT_folder = 'animate_inanimate_exp_data'  # Log is saved to this folder. The folder is created if it does not exist (see ppc.py).

# If folder does not exist, do create it
if not os.path.exists(OUTPUT_folder):
    os.makedirs(OUTPUT_folder)
    
# prepare pandas data frame for recorded data
columns = ['id', 'age', 'gender', 'scanner', 'scan_day', 'onset', 'offset', 'duration_measured', 'response','key_t','rt','con']
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)

############# LOADING THE IMAGES ################################

imageFolderPathAni = 'C:/Users/stimuser/Desktop/CogSci_2018/Group 3 Neuroimaging studie/Images/Ani' #Loading images from the Ain folder (animate)
STIMANI0 = glob.glob(imageFolderPathAni + '/*.JPEG') 

imageFolderPathAni = 'C:/Users/stimuser/Desktop/CogSci_2018/Group 3 Neuroimaging studie/Images/Ani2'#Loading images from the Ain2 folder (animate)
STIMANI1 = glob.glob(imageFolderPathAni + '/*.JPEG') 

imageFolderPathInani = 'C:/Users/stimuser/Desktop/CogSci_2018/Group 3 Neuroimaging studie/Images/Inani' #Loading images from the Inain folder (inanimate)
STIMINANI0 = glob.glob(imageFolderPathInani + '/*.JPEG')

imageFolderPathInani = 'C:/Users/stimuser/Desktop/CogSci_2018/Group 3 Neuroimaging studie/Images/Inani2' #Loading images from the Inain2 folder (inanimate)
STIMINANI1 = glob.glob(imageFolderPathInani + '/*.JPEG')

############# Intro text ################################
#Needs to be changed !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
introText = '''

Welcome. 

In this experiment you have to look at images.

Press button with INDEX finger if the image is bigger then the previous image.
Press button with MIDDLE finger if the image is smaller then the previous image .

Press a bottem to start the experiment
'''

message = visual.TextStim(win, pos =[0,0], text = introText, height = 0.75, alignHoriz = 'center',color='black') # create an instruction text
message.draw() # draw the text stimulus in a "hidden screen" so that it is ready to be presented # flip the screen to reveal the stimulus
win.flip()
event.waitKeys()

##### Experimental loop!
event.waitKeys(keyList='t')
exp_start = core.monotonicClock.getTime() # getting the start time

# Loop over trials
for k in range (STIM_rep):
    for i in range(STIM_bloks):
        
        # Clear keyboard record
        event.clearEvents(eventType='keyboard')

        STIMANI= eval("STIMANI"+str(i))
        shuffle(STIMANI)

        # Display image and monitor time
        time_flip = core.monotonicClock.getTime() # onset of stimulus
        for s in range(len(STIMANI)): #Runs though 15 images
            for frame in range(STIM_dur):
                stim_img = visual.ImageStim(win, image = STIMANI[s])
                stim_img.draw()
                win.flip()

        # Display fixation cross
        offset = core.monotonicClock.getTime()  # offset of stimulus
        for frame in range(STIM_break):
            STIM_fix.draw()
            win.flip()
            
     
        # Check responses
        keys = event.getKeys(keyList=('y','b','escape'), timeStamped=True) # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.                          
        
        # Log first response only
        if keys:
            key = keys[0][0]
            time_key = keys[0][1]
            
            # Check if escape key was pressed
            if key in KEYS_quit:
                win.close()
                core.quit()
            
            # Log info on responses
            DATA = DATA.append({
                'id': EXP_info[0],
                'age': EXP_info[1],
                'gender': EXP_info[2],
                'scanner': EXP_info[3],
                'scan_day': EXP_info[4],
                'onset': time_flip - exp_start,
                'offset': offset - exp_start,
                'duration_measured': offset - time_flip,
                'response': key,
                'key_t': time_key - exp_start,
                'rt': offset - time_flip,
                'con':'ani'+str(i)},
                ignore_index=True) 
        else:
            key=None
            # Log info on responses
            DATA = DATA.append({
                'id': EXP_info[0],
                'age': EXP_info[1],
                'gender': EXP_info[2],
                'scanner': EXP_info[3],
                'scan_day': EXP_info[4],
                'onset': time_flip - exp_start,
                'offset': offset - exp_start,
                'duration_measured': offset - time_flip,
                'response': 'NA',
                'key_t': 'NA',
                'rt': offset - time_flip,
                'con':'ani' +str(i)},
                ignore_index=True) 

            
        # Clear keyboard record
        event.clearEvents(eventType='keyboard')

        STIMINANI= eval("STIMINANI"+str(i)) # Calls for the right blok
        shuffle(STIMINANI)

        # Display image and monitor time
        time_flip = core.monotonicClock.getTime() # onset of stimulus
        for s in range(len(STIMINANI)):
            for frame in range(STIM_dur):
                stim_img = visual.ImageStim(win, image = STIMINANI[s])
                stim_img.draw()
                win.flip()

        # Display fixation cross
        offset = core.monotonicClock.getTime()  # offset of stimulus
        for frame in range(STIM_break):
            STIM_fix.draw()
            win.flip()
            
        # Check responses
        keys = event.getKeys(keyList=('y','b','escape'), timeStamped=True) # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.                          
        
        # Log first response only
        if keys:
            key = keys[0][0]
            time_key = keys[0][1]
            
            # Check if escape key was pressed
            if key in KEYS_quit:
                win.close()
                core.quit()
            
            # Log info on responses
            DATA = DATA.append({
                'id': EXP_info[0],
                'age': EXP_info[1],
                'gender': EXP_info[2],
                'scanner': EXP_info[3],
                'scan_day': EXP_info[4],
                'onset': time_flip - exp_start,
                'offset': offset - exp_start,
                'duration_measured': offset - time_flip,
                'response': key,
                'key_t': time_key - exp_start,
                'rt': offset - time_flip,
                'con':'inani' +str(i)},
                ignore_index=True) 
        else:
            key=None
            # Log info on responses
            DATA = DATA.append({
                'id': EXP_info[0],
                'age': EXP_info[1],
                'gender': EXP_info[2],
                'scanner': EXP_info[3],
                'scan_day': EXP_info[4],
                'onset': time_flip - exp_start,
                'offset': offset - exp_start,
                'duration_measured': offset - time_flip,
                'response': 'NA',
                'key_t': 'NA',
                'rt': offset - time_flip,
                'con':'inani' +str(i)},
                ignore_index=True) 


############# Saves data ################################
date = data.getDateStr() 
OUTPUT_folder = 'animate_inanimate_exp_data' #saves to this folder
OUTPUT_filename = OUTPUT_folder + '/log_' + str(EXP_info[0]) + '_' + date + '.csv'
DATA.to_csv(OUTPUT_filename)

############# Outro text ################################

outroText = '''

This is the end of the experiment. 

Thank you for your participation!

'''

message = visual.TextStim(win, pos =[0,0], text = outroText, height = 0.75, alignHoriz = 'center', color='black') # create an instruction text
message.draw() # draw the text stimulus in a "hidden screen" so that it is ready to be presented # flip the screen to reveal the stimulus
win.flip()
event.waitKeys()

# stop experiment
win.close()
core.quit()
