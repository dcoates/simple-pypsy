import numpy
import numpy.fft as fft
from psychopy import *
#import collections

def listOr1( list, idx ):
	#if isinstance( list, collections.Iterable):
	# the above is True for string. We want false for the single character text
	if getattr( list, '__iter__', False):
		return list[idx]
	else:
		return list

class stim_letter():
	"""Generic letter with list of pre-computed (passed in) parameters:
			xpos, ypos, and text """

	def __init__(self, win, height, targcol, selfont,  list ):
		self.param_list = list.copy() # Hopefully will not be that deep
		self.widget = visual.TextStim(win,alignHoriz='center',height=height, rgb=targcol, ori=0, font=selfont ) 
		self.pos = (0,0)
		self.text = ""
		self.height = height

	def getval(self, which, num):
		return listOr1( self.param_list[which], num )

	def getTrial(self, trialNum=0):
		self.pos = (self.getval('xpos',trialNum), self.getval('ypos',trialNum))
		self.text = self.getval('text',trialNum)
		self.height =  self.getval('height',trialNum)

	def strvals(self ):
		result = "%s %s %s %s" % (self.pos[0], self.pos[1], self.text, self.height )
		return result

	def draw(self, c=-999):
		self.widget.setPos(self.pos) 
		self.widget.setText(self.text) 
		self.widget.setHeight(self.height)
		if c>-999:
			self.widget.setRGB( c )
		self.widget.draw()

class olchar():
	"""Compound 'letter' consisting of an o and and l. The l is positioned relative to center of o."""

	def __init__(self, win, height, targcol, selfont, list ):
		self.param_list = list
		list.update( {'text':'o'} )
		self.o = stim_letter( win, height, targcol, selfont, list)
		list.update( {'text': 'l', 'xpos': list['xpos']+list['relx']} )
		self.l = stim_letter( win, height, targcol, selfont, list)

	def getTrial(self, trialNum=0):
		self.o.getTrial(trialNum)
		self.l.getTrial(trialNum)

	def copyParams( self,other, trialNum ):
		self.o.widget.setPos( (other.o.getval('xpos',trialNum), other.o.getval('ypos',trialNum)) )
		self.l.widget.setPos( (other.l.getval('xpos',trialNum), other.l.getval('ypos',trialNum)) )

	def draw( self ):
		self.o.draw()
		self.l.draw()

	def strvals( self ):
		return '%s %s' % (self.o.strvals(), self.l.strvals() )
		
#class phigram():

class stim_illus():
	"""Generic letter with list of pre-computed (passed in) parameters:
			xpos, ypos, and text """

	def __init__(self, win, targcol, size, list ):
		self.param_list = list.copy() # Hopefully will not be that deep

		if self.getval('maskrad')>0.0:
			themask = -numpy.ones( (size, size) ) # init to blank
			actualpix = numpy.floor( size * self.getval('maskrad') )
			for row in numpy.arange(-actualpix, actualpix):
				xoffcenter = numpy.sqrt( actualpix**2 - row**2 ) 
				themask[ size/2.0+row, (size/2.0-xoffcenter):(size/2.0+xoffcenter) ] = 1.0
				
			self.widget = visual.PatchStim(win, mask=themask,  tex="none",
				units='pix', size=(size, size), color=targcol, ori=0 ) 
		else:
			self.widget = visual.PatchStim(win, mask='circle',  tex="none",
				units='pix', size=(size, size), color=targcol, ori=0 ) 

		# rgb ignored? 
#noise = visual.PatchStim( myWin, texRes=1, mask="none", tex="none",
#pos=(-0,exper.yloc_pix), units='pix', size=(noise_size, noise_size),
#rgb=[1.0,1.0, 1.0] )

#psychopy.visual.PatchStim(win, tex='sin', mask='none', units='', pos=(0.0,
#0.0), size=None, sf=None, ori=0.0, phase=(0.0, 0.0), texRes=128, rgb=None,
#dkl=None, lms=None, color=(1.0, 1.0, 1.0), colorSpace='rgb', contrast=1.0,
#opacity=1.0, depth=0, rgbPedestal=(0.0, 0.0, 0.0), interpolate=False, name

		self.pos = (0,0)
	#{'xpos':0, 'ypos':0, 'ori':oriseq, 'thick':1, 'sf':10, 'phase0':0, 'phase1':2} )
		ph0 = self.getval('phase0')
		ph1 = self.getval('phase1')
		thik = self.getval('thick')
		
		self.texture = numpy.zeros( (len(self.param_list['texori']), size, size) ) 
		for txX, texori in enumerate(self.param_list['texori']):
			for i in numpy.linspace(0,size,self.getval('sf',0), endpoint=False):
				xill = size/2.0 + (size/2.0 - i) * numpy.tan( texori * numpy.pi / 180.0 )
				#print i,xill
				ybot = numpy.min( i+ph0+thik, size-1 )
				self.texture[txX, (i+ph0):ybot,0:xill] = 1.0
				ybot2 = numpy.min( i+ph1+thik, size-1 )
				self.texture[txX, i+ph1:ybot2,xill:size] = 1.0
			#texture[i+ph0,0:size*0.5] = 1.0
		#for i in numpy.linspace(0,size,self.getval('sf',0), endpoint=False):
			#texture[i+ph1,size*0.5:size] = 1.0
		#self.widget.setTex( (numpy.random.rand( size, size)*1.005)-1.0)

		#dev = 0.1;
		#linesat = numpy.linspace(0,size,self.getval('sf',0), endpoint=False)
		#frac = numpy.random.rand(len(linesat))*dev+0.5-dev/2.0;
		#for i,val in enumerate(linesat):
			#texture[val+ph0,0:(size*frac[i])] = 1.0
			#texture[val+ph1,(size*frac[i]):size] = 1.0

		#self.widget.setTex( self.texture )

	def getval(self, which, num=0):
		return listOr1( self.param_list[which], num )

	def getTrial(self, trialNum=0):
		self.pos = (self.getval('xpos',trialNum), self.getval('ypos',trialNum))
		self.ori = self.getval('ori',trialNum)
		self.oriseq = self.getval('oriseq',trialNum)

	def strvals(self ):
		result = "%s %s %s" % (self.pos[0], self.pos[1], self.ori )
		return result

	def draw(self):
		self.widget.setPos(self.pos) 
		self.widget.setOri(self.ori) 
		self.widget.setTex(self.texture[self.oriseq]) 
		self.widget.draw()

	"""Stimulus consisting of target letter surrounded by phis"""

def downsample(myarr,factor):
    """
    Downsample a 2D array by averaging over *factor* pixels in each axis.
    Crops upper edge if the shape is not a multiple of factor.

    This code is pure numpy and should be fast.
    """
    xs,ys = myarr.shape
    crarr = myarr[:xs-(xs % int(factor)),:ys-(ys % int(factor))]
    dsarr = numpy.concatenate([[crarr[i::factor,j::factor]
        for i in numpy.arange(factor)]
        for j in numpy.arange(factor)]).mean(axis=0)
    return dsarr

class stim_letternoise():
	"""Generic letter with list of pre-computed (passed in) parameters:
			xpos, ypos, and text """

	def __init__(self, win, height, width, backmean, list ):
		self.param_list = list.copy() # Hopefully will not be that deep
		self.widget = visual.PatchStim(win, tex=None, size=(height,width) ) 
		self.widget = visual.PatchStim( win, texRes=1, mask="none", tex="none", units='pix', size=(height,width), color=[1.0,1.0, 1.0] )
		self.pos = (0,0)
		self.text = ""
		self.height = height
		self.width = width
		self.backmean = backmean
		portion = 256.0/height
		self.sf = downsample( numpy.real( numpy.load( 'meany.npy' )[0:(portion*height)][0:(portion*width)] ), 256.0/height )

	def getval(self, which, num):
		return listOr1( self.param_list[which], num )

	def getTrial(self, trialNum=0):
		self.pos = (self.getval('xpos',trialNum), self.getval('ypos',trialNum))
		noise = numpy.random.rand( self.height, self.width )
		noise_fft = fft.fft2( noise )
		recon = numpy.real( fft.ifft2( noise_fft * self.sf ) )
		# Make in the range -1, 1 which tex wants:
		recon = recon - numpy.mean(recon)
		recon = recon * 1.0 / ( recon.max() - recon.min() )
		recon = (recon - recon.min() ) - 0.8
		recon += self.backmean
		self.recon = recon
		self.widget.setTex( recon )

	def strvals(self ):
		result = "%s %s %s %s" % (self.pos[0], self.pos[1], self.text, self.height )
		return result

	def draw(self, c=-999):
		self.widget.setPos(self.pos) 
		self.widget.draw()

