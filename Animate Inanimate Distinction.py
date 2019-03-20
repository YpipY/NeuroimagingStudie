# -*- coding: utf-8 -*-

""" DESCRIPTION:
This fMRI experiment on animate inanimate distinction

Structure:

    - Import modules
    - Set monitor variables
    - Get participants info using GUI
    - INITIALIZE WINDOW
    - PREPARE STIMULI
    - RESPONSES AND OTHER COMMANDS
    - OUTPUT LOGFILE
    - FUNCTIONS FOR EXPERIMENTAL LOOP
    - Define the experimental loop!
    - SET UP INSTRUCTIONS
    - RUN THE EXPERIMENT


"""

#############  IMPORT MODULES  ################################
from __future__ import division
from psychopy import core, visual, event, gui, data, monitors
from itertools import product
from random import sample
from PIL import Image
import pandas as pd
import os
import numpy as np 
import glob


#############  SET MONITOR VARIABLES ###########################
# Monitor parameters
MON_distance = 60  # Distance between subject's eyes and monitor 
MON_width = 34  # Width of your monitor in cm
MON_size = [1440, 900]  # Pixel-dimensions of your monitor, width / height
MON_frame_rate = 60 # Hz: usually 60, but you can always check with the function getActualFrameRate

# Create monitor
my_monitor = monitors.Monitor('testMonitor', width=MON_width, distance=MON_distance)  # Create monitor object from the variables above. This is needed to control size of stimuli in degrees.
my_monitor.setSizePix(MON_size)



############# GET PARTICIPANT INFO USING GUI ###########################
# Initialize dictionary with required variables
EXP_info = {'ID':'',
            'age':'',
            'gender':['female','male'],
            'Scanner':['Prisma','Skyra'],
            'Scan day': ['Tuesday','Wednesday']}

# DlgFromDict creates dialog with fields specified in dictionary to gather required info
if not gui.DlgFromDict(EXP_info, title = 'Animate Inanimate Distinction Experiment', order=['ID', 'age', 'gender','Scanner','Scan day']).OK: # dialog box; order is a list of keys 
    core.quit()

   
    
############# INITIALIZE WINDOW ###########################
# Initialize window for stimulus presentation
win = visual.Window(monitor = my_monitor,
                    units = 'deg',
                    fullscr = False, # Set to True
                    allowGUI = False, 
                    color = 'black')  # Initiate psychopy Window as the object "win", using the myMon object from last line. Use degree as units!


                    
############# PREPARE STIMULI ################################
# Experiment details
# 2x2 blocks, 15 stims each. 30 sec break

# Timing details
STIM_dur = int(0.1 * MON_frame_rate) # duration in seconds multiplied by 60 Hz and made into integer
STIM_delays = 140 # different time intervals between stimuli mean 3.5 sec x 60 hz refresh rate = 210, in order to make less predictable and increase power.
STIM_trials = 1
STIM_break = int(1.5 * MON_frame_rate)

# The image size and position using ImageStim, file info added in trial list below.
STIM_image = visual.ImageStim(win,
    mask=None,
    pos=(0.0, 0.0), # Should be default
    size=(14.0, 10.5),
    ori=1)

# Prepare Fixation cross, i.e. just the character "+".
STIM_fix = visual.TextStim(win, '+')


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

imageFolderPathAni = 'C:/Users/slmoni/Documents/Uni/Introduction to Neuroscience/Neuroimaging studie/Images/Ani'
STIMANI = glob.glob(imageFolderPathAni + '/*.JPG') 

imageFolderPathInani = 'C:/Users/slmoni/Documents/Uni/Introduction to Neuroscience/Neuroimaging studie/Images/Inani'
STIMINANI = glob.glob(imageFolderPathInani + '/*.JPG')

# prepare pandas data frame for recorded data
columns = ['ID', 'age', 'gender', 'Scanner', 'Scan day', 'onset', 'offset', 'duration_measured', 'response','key_t','rt','con']
index = np.arange(0)
DATA = pd.DataFrame(columns=columns, index = index)

##### Define the experimental loop!
def run_condition(condition):
    """
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """
    # Loop over trials
    for i in range(STIM_trials):
        
        # Clear keyboard record
        event.clearEvents(eventType='keyboard')

        # Display image and monitor time
        time_flip = core.monotonicClock.getTime() # onset of stimulus
        for s in range(1, 6):
            for frame in range(STIM_dur):
                stim_img = visual.ImageStim(win, image = STIMANI[s])
                stim_img.draw()
                win.flip()
 
        # Display fixation cross
        offset = core.monotonicClock.getTime()  # offset of stimulus
        for frame in range(STIM_break):
            STIM_fix.draw()
            win.flip()
            # Get actual duration at offset
            
     
        # Check responses
        keys = event.getKeys(keyList=('y','b','escape'), timeStamped=True) # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.                          
        
        # Log first response only
        if keys:
            key = keys[0][0]
            time_key = keys[0][1]
            
            # Log info on responses
            DATA = DATA.append(
                {'ID': ID[0],
                'age': ID[1],
                'Scanner': ID[2],
                'Scan day': ID[3],
                'onset': time_flip - exp_start,
                'offset': offset - exp_start,
                'duration_measured': offset - time_flip,
                'key_t': key,
                'key_t': time_key - exp_start,
                'rt': offset - time_flip,
                'con':'ani'},
                ignore_index=True) 
            print (DATA)
            # Check if escape key was pressed
            if key in KEYS_quit:
                STIM_comb_df.to_csv(OUTPUT_filename)
                win.close()
                core.quit()
            
        # Clear keyboard record
        event.clearEvents(eventType='keyboard')

        # Display image and monitor time
        time_flip = core.monotonicClock.getTime() # onset of stimulus
        for s in range(1, 6):
            for frame in range(STIM_dur):
                stim_img = visual.ImageStim(win, image = STIMINANI[s])
                stim_img.draw()
                win.flip()
 
        # Display fixation cross
        offset = core.monotonicClock.getTime()  # offset of stimulus
        for frame in range(STIM_break):
            STIM_fix.draw()
            win.flip()
            # Get actual duration at offset 
        # Check responses
        keys = event.getKeys(keyList=('y','b','escape'), timeStamped=True) # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.                          
        
        # Log first response only
        if keys:
            key = keys[0][0]
            time_key = keys[0][1]
            
            # Log info on responses
            DATA = DATA.append(
                {'ID': ID[0],
                'age': ID[1],
                'Scanner': ID[2],
                'Scan day': ID[3],
                'onset': time_flip - exp_start,
                'offset': offset - exp_start,
                'duration_measured': offset - time_flip,
                'key_t': key,
                'key_t': time_key - exp_start,
                'rt': offset - time_flip,
                'con':'inani'},
                ignore_index=True) 
                
            # Check if escape key was pressed
            if key in KEYS_quit:
                STIM_comb_df.to_csv(OUTPUT_filename)
                win.close()
                core.quit()


 
   
############# SET UP INSTRUCTIONS ########################
def msg(txt):
    message = visual.TextStim(win, pos =[0,0], text = txt, height = 0.75, alignHoriz = 'center') # create an instruction text
    message.draw() # draw the text stimulus in a "hidden screen" so that it is ready to be presented # flip the screen to reveal the stimulus
    win.flip()

introText = '''

Welcome. 

In this experiment you have to read sentences.

Press button with INDEX finger if meaning CLEAR.
Press button with MIDDLE finger if meaning STRANGE.

The experiment will start in a few moments
'''

outroText = '''

This is the end of the experiment. 

Thank you for your participation!

'''


############# RUN THE EXPERIMENT ########################

# Display instructions 
msg(introText)       

#Wait for scanner trigger "t" to continue
event.waitKeys(keyList = KEYS_trigger) 

# Start timer
exp_start = core.monotonicClock.getTime()

# Run the experimental loop
run_condition('sentence_exp')

# save logfile
date = data.getDateStr()  
OUTPUT_filename = OUTPUT_folder + '/log_' + str(EXP_info['ID']) + '_' + date + '.csv'
DATA.to_csv(OUTPUT_filename)

# outro
msg(outroText)

# stop experiment
win.close()
core.quit()