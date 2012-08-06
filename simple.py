from psychopy import *
from psychopy import log
import numpy as np
import time 
import matplotlib.pyplot as pyplot
import os 
import pylab # for frame interval plotting only

import stims
import conditions

# Utility functions
def randi( high, numvals=None, low=0 ):
    if numvals == None:
        return np.array(np.random.rand() * (high-low)+low, dtype=int)
    else:
        return np.array(np.random.rand(numvals) * (high-low)+low, dtype=int)

def buildtrialseq( vals, ntrials ):
    return np.random.permutation( np.tile ( vals, np.ceil( float(ntrials)/len(vals)) ) )[0:ntrials]

# Outputfile params
SubjectName = 'test' 
CreateUniqueBlockFiles = True
OutputHeader = True

# This experiment: contrasts
backcol= ( 0.00, 0.00, 0.00)
targcol= (-0.95,-0.95,-0.95)

# This experiment: monitor, font, etc.
exper = conditions.experSony( ( 1024, 768 ), 288, 500.0, 10.0, 0 )
font = conditions.fontArial( targcol )
fontsize=0.625
font.setCharDegs( fontsize, exper )

# This experiment - trials, timing, etc. 
ntrials = 10
pre_time = 0.0
trial_time = 0.100  # in sec. use -1 for infinite
mask_time = 0.100

fullscr = False # make sure this matches next
# Set up the screen, etc.
myWin = visual.Window(exper.screendim, allowGUI=True, color=backcol, units='pix', fullscr=fullscr )
myWin.setMouseVisible(False)
showFrameTiming = False

#set the log module to report warnings to the std output window (default is errors only)
log.console.setLevel(log.ERROR)

fixation = visual.TextStim(myWin,pos=(0,exper.yloc_fixation_pix),alignHoriz='center',height=9, color=font.contrast, ori=0, font=font.selfont ) 
fixation.setText( 'o' )

# Post-trial text
response_list_disp = visual.TextStim(myWin,pos=(0,exper.yloc_fixation_pix-exper.deg2pix(5.0)),alignHoriz='center',height=font.let_height_ptfont,
    color=font.contrast, ori=0, font=font.selfont, text='Left for x, Right for o' ) 

orda = 97 
targets = [ 'x', 'o' ]

maxtrials = ntrials
test_heights = font.let_height_ptfont

targseq = [targets[i] for i in buildtrialseq( np.arange(len(targets)), maxtrials) ]
 
targ = stims.stim_letter( myWin, font.let_height_ptfont, font.contrast, font.selfont, 
    {'height': test_heights, 'xpos':0.0, 'ypos':exper.yloc_pix, 'text':targseq}  )

stims = [ targ ] 
cues = [] # [ cueU, cueD ]

# Noise mask
noise_wid = 16
noise_size = 256  # TODO: Parametrize. Base on min/mix of stimuli??
noise = visual.PatchStim( myWin, texRes=1, mask="none", tex="none", pos=(0,-exper.deg2pix(10.0)), units='pix', size=(noise_size, noise_size), color=[1.0,1.0, 1.0] )
noisemult = 2.0 # multiplier for rand (contrast)
noiseoff =  1.2 # - offset of rand
noisebinary = True # TODO: Better specify contrast of binary noise: is floor(rand*mult)-off

maxtrials = ntrials
 
if CreateUniqueBlockFiles:
    # Find a unique filename by appending a number to the session
    blockidx = 0
    gotunique = False
    while gotunique==False: 
        outfilename = "%s_%s-%02d.csv" % (SubjectName, time.strftime("%m%d%Y", time.localtime() ), blockidx)
        if os.path.exists(outfilename):
            blockidx += 1
        else:
            gotunique = True
else:
    outfilename = "%s_%s.csv" % (SubjectName, time.strftime("%m%d%Y", time.localtime() ) )
        
outfile = open(outfilename, "wt")
xval = 0
done = False
trialNum=0

myWin.setRecordFrameIntervals(True)
myWin._refreshThreshold=0.03 # set to 30 ms on my monitor
#mywin._refreshThreshold=1/85.0+0.004 #i've got 85Hz monitor and want to allow 4ms tolerance

# Calibrate by seeing how long 100 redraws takes
fixation.setText( 'Calibrating monitor...' )
for i in np.arange(100):
    fixation.draw()
    [stim.draw() for stim in stims]
    #[cue.draw() for cue in cues]
    myWin.flip()
savetimes = myWin.frameIntervals
fliprate = np.mean( savetimes[20:] )
print 'fliprate=%f' % fliprate

fixation.setText( 'Press any key twice to start (first goes to fixation screen)\n' )
fixation.draw()
myWin.flip()
event.waitKeys()

fixation.setText( 'o' )
fixation.draw()
myWin.flip()
event.waitKeys()

# Turn this on to save timing information:
#myWin.setRecordFrameIntervals(False)

while not done:
    fixation.draw()
    myWin.flip()
    core.wait(pre_time)
    fixation.draw()
    [stim.getTrial(trialNum ) for stim in stims]
    myWin.flip()

    [stim.draw( (targcol[0],targcol[0],targcol[0]) ) for stim in stims]
    [cue.draw() for cue in cues]
    fixation.draw()
    myWin.flip()
    core.wait(trial_time)
        
    if mask_time > 0:
        fixation.draw()
        if noisebinary:
            thenoise = np.floor(np.random.rand(noise_size,noise_size)*noisemult)-noiseoff 
            # clip to allowable range:
            thenoise[thenoise<-1] = -1 
            thenoise[thenoise>1] = 1

            noise.setTex( thenoise )
        else:
            noise.setTex( (np.random.rand(noise_size,noise_size)*noisemult)-noiseoff)
        noise.draw()
        myWin.flip()
        core.wait(mask_time)

    # If positive trial_time, show response screen
    if (trial_time >= 0):
        fixation.draw()
        response_list_disp.draw()
        myWin.flip()

    validkey = False
    while validkey == False:
        for key in event.waitKeys():
            if key in [ 'escape', 'q' ]:
                resp = -1
                done = True
                validkey = True
            if key in [ 'left' ]:
                resp = 0
                validkey = True
            if key in [ 'right' ]:
                resp = 1
                validkey = True

    outfile.write("%s %s %s\n" % (key, resp, targ.text) )

    trialNum += 1
    if trialNum >= maxtrials:
        done = True

myWin.close()

if OutputHeader:
    outfile.write( '#END\n' )
    outfile.write( '%s\n' % [str(stim) for stim in stims])
    outfile.write( "#V 0.2\n" )
    outfile.write( '#font=' + str(font.let_height_ptfont) + "\n")
    outfile.write( '#font.let_height_pixels=' + str(font.let_height_pixels) + "\n")
    outfile.write('#font.let_height_mm=' + str(font.let_height_mm) + "\n")
    outfile.write('#font.let_height_deg=' + str(font.let_height_deg) + "\n")
    #outfile.write('#ratio of (ascender+descender) to o=' + str(ascender_and_descender_to_o) + "\n")
    #outfile.write('#ratio of ptfont to pixels=0' + str(ptfont_to_pixels) + "\n")
    #utfile.write( '#distance=' + str(distance) + "\n")
    #utfile.write( '#pixels per mm=' + str(screensize) + "\n")
    #utfile.write( '#degrees_eccentricity=' + str(degrees_eccentricity) + "\n" )
    outfile.write( '#exper.yloc_pix=' + str(exper.yloc_pix) + "\n" )
    outfile.write( '#trial time=' + str(trial_time) + "\n")
    outfile.write( "key, targ.strvals(), olL.strvals(), olR.strvals() ")
    outfile.write( '#fontsize=' + str(fontsize) + "\n")
    outfile.write( '#trial_time=' + str(trial_time) + "\n")
outfile.close()

if showFrameTiming:
    pylab.plot(myWin.frameIntervals, '.-')
    pylab.grid()
    pylab.show()

