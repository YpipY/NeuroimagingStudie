# -*- coding: utf-8 -*-

""" DESCRIPTION:
This fMRI experiment displays different sentences with motion or non-motion verbs.
The script awaits a trigger pulse from the scanner with the value "t"

/Roberta Rocca & Mikkel Wallentin 2018 (with some of the code adapted from Jonas LindeLoev: https://github.com/lindeloev/psychopy-course/blob/master/ppc_template.py)

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
import pandas as pd
import os



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
if not gui.DlgFromDict(EXP_info, title = 'Semantics experiment', order=['ID', 'age', 'gender','Scanner','Scan day']).OK: # dialog box; order is a list of keys 
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
# 12 min. exp. = 720 sec. -> 144 trials with stimulus duration 1500 ms onset asyncrony of 5 s (i.e. 3.5 s fixation cross in between on average.

# Specify conditions                                                                                               
condition = 'sentence_exp' # Here just one. If there are more conditions, add here or call in GUI. 

# Define sentence components
STIM_pros = ('We ','You ','They ') #Initial pronoun
STIM_verbs = ('walk ','run ','jump ','stand ','sit ','lie ') #three motion verbs, three non-motion verbs
STIM_preps = ('in ', 'into ') # static / dynamic prepositions
STIM_locs = ('the house', 'the garden','the culture','the system') #one concrete one abstract

# Timing details
STIM_dur = int(1.5 * MON_frame_rate) # duration in seconds multiplied by 60 Hz and made into integer
STIM_delays = (140, 180, 240, 280) # different time intervals between stimuli mean 3.5 sec x 60 hz refresh rate = 210, in order to make less predictable and increase power.
STIM_repetitions = 1 
STIM_trials = 144

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
OUTPUT_folder = 'sentence_exp_data'  # Log is saved to this folder. The folder is created if it does not exist (see ppc.py).

# If folder does not exist, do create it
if not os.path.exists(OUTPUT_folder):
    os.makedirs(OUTPUT_folder)

# Set filename
date = data.getDateStr()  
OUTPUT_filename = OUTPUT_folder + '/log_' + str(EXP_info['ID']) + '_' + date + '.csv'



############# FUNCTIONS FOR EXPERIMENTAL LOOP ########################
##### Create all combos and store in a dataframe
def make_trial_list(delays_list, nr_trials, duration): # Add condition as argument and to combinations function if you have many
    cols_sent = ['pronoun', 'verb', 'preposition', 'location']
     
    # Create a df with all combinations of sentence components     
    global STIM_comb_df
    STIM_comb_df = pd.DataFrame(list(product(STIM_pros, STIM_verbs, STIM_preps, STIM_locs)), columns = cols_sent)
    STIM_comb_df = STIM_comb_df.sample(frac = 1).reset_index(drop=True)
    
    # create list with delays, and shuffle
    STIM_comb_df['delay'] = int(nr_trials/len(delays_list)) * delays_list
    STIM_comb_df['delay'] = sample(STIM_comb_df['delay'], nr_trials)
    # Add info on duration (do as in delay or shift this part to the experimental loop if you have different durations)
    STIM_comb_df['duration_frames'] = duration
    
    # Add default to other relevant columns
    cols_ID = ['ID', 'age', 'gender', 'Scanner', 'Scan_day']
    cols_resp = ['onset','offset', 'duration_measured','response', 'key_t', 'rt', 'correct_resp']
    STIM_comb_df = pd.concat([STIM_comb_df, pd.DataFrame(columns = cols_ID + cols_resp)], axis = 1)

    # Fill with ID info
    STIM_comb_df[cols_ID] = EXP_info.values()
    
    # Fill with default for response info
    STIM_comb_df[cols_resp] = ''
    
    # Add trial number
    STIM_comb_df['trial_nr'] = range(1, 145)

    
##### Define the experimental loop!
def run_condition(condition):
    """
    Runs a block of trials. This is the presentation of stimuli,
    collection of responses and saving the trial
    """
    
    # Make global changes to the dataframe  
    global STIM_comb_df
    
    # Loop over trials
    for i in range(STIM_trials):
        
        # Clear keyboard record
        event.clearEvents(eventType='keyboard')
        
        # Prepare image
        stim_sent = STIM_comb_df['pronoun'][i] + STIM_comb_df['verb'][i] + STIM_comb_df['preposition'][i] + STIM_comb_df['location'][i] 

        # Display image and monitor time
        time_flip = core.monotonicClock.getTime() # onset of stimulus
        for frame in range(STIM_dur):
            stim_sentence = visual.TextStim(win=win, text=stim_sent, pos=[0,0], height=1, alignHoriz='center')
            stim_sentence.draw()
            win.flip()
 
        # Display fixation cross
        offset = core.monotonicClock.getTime()  # offset of stimulus
        for frame in range(STIM_comb_df['delay'][i]):
            STIM_fix.draw()
            win.flip()
            # Get actual duration at offset
            
        #Log time variables
        STIM_comb_df['onset'][i]= time_flip - exp_start
        STIM_comb_df['offset'][i] = offset - exp_start
        STIM_comb_df['duration_measured'][i] = offset - time_flip   
     
        # Check responses
        keys = event.getKeys(keyList=('y','b','escape'), timeStamped=True) # timestamped according to core.monotonicClock.getTime() at keypress. Select the first and only answer.                          
        
        # Log first response only
        if keys:
            key = keys[0][0]
            time_key = keys[0][1]
            
            # Log info on responses
            STIM_comb_df['response'][i] = key
            STIM_comb_df['key_t'][i] = time_key - exp_start
            STIM_comb_df['rt'][i] = time_key - time_flip  
        
            # Check if responses are correct
            if STIM_comb_df['response'][i] == 'y':
                STIM_comb_df['correct_resp'][i] = 1 if STIM_comb_df['verb'][i] in STIM_verbs[0:3] else 0

            if STIM_comb_df['response'][i] == 'b':
                STIM_comb_df['correct_resp'][i] = 1 if STIM_comb_df['verb'][i] not in STIM_verbs[0:3] else 0
  
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
# Setup the dataframe
make_trial_list(STIM_delays, STIM_trials, STIM_dur)

# Display instructions 
msg(introText)       

#Wait for scanner trigger "t" to continue
event.waitKeys(keyList = KEYS_trigger) 

# Start timer
exp_start = core.monotonicClock.getTime()

# Run the experimental loop
run_condition('sentence_exp')

# save logfile
STIM_comb_df.to_csv(OUTPUT_filename)

# outro
msg(outroText)

# stop experiment
win.close()
core.quit()


