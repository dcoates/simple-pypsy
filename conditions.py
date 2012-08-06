import numpy

# Utility functions
def  deg2rad( angle ):
    return angle / 180.0 * numpy.pi
def  rad2deg( angle ):
    return angle * 180.0 / numpy.pi

class experSony():
	def __init__(self, screendim, screenheight, distance, stim_ecc_deg, yloc_fixation_pix=0 ):
		self.screendim = screendim
		#screensize = 100.0 / 36.0 # pix/mm for Sony Trinitron at 1024x768 (or ~ 768/284)
		self.screensize = screendim[1] / screenheight # height is 284 mm, 768 pixels
		self.distance = distance 
		self.stim_ecc_deg = stim_ecc_deg 
		self.yloc_fixation_pix = yloc_fixation_pix #distance from fixation to ceter of screen in pixels
		self.yloc_pix = -distance * numpy.tan( deg2rad(stim_ecc_deg))* self.screensize + yloc_fixation_pix#y-location of the center of the letter from center of screen

	def deg2pix( self, angle ):
		return numpy.round( self.distance * self.screensize * (numpy.tan ( deg2rad(self.stim_ecc_deg + angle / 2.0)) -
        	numpy.tan( deg2rad(self.stim_ecc_deg - angle / 2.0)) ) )# height in pixels

	def pix2deg( self, pix ):
		return rad2deg( numpy.arctan( ( pix / self.screensize) / self.distance ) )

class fontArial():
	def __init__(self, contrast):
		self.selfont = 'Arial'
		self.ascender_and_descender_to_o=6.0/8.0
		self.ptfont_to_pixels=720.0/700.0
		self.contrast = contrast

	def setCharDegs(self, degs, exper):
		self.o_height_degs = degs/(1+self.ascender_and_descender_to_o/2.0) #7.125  # desired height of 'o' in degreess

		self.let_height_deg = self.o_height_degs + self.ascender_and_descender_to_o * self.o_height_degs
		self.let_height_pixels = exper.deg2pix( self.let_height_deg )

		# Caclulations
		self.let_height_ptfont = numpy.floor( self.ptfont_to_pixels * self.let_height_pixels )

		# TODO: replace with deg2 routine
		self.let_height_mm=exper.distance * (numpy.tan ( deg2rad(exper.stim_ecc_deg + self.let_height_deg / 2)) -
        		numpy.tan( deg2rad(exper.stim_ecc_deg - self.let_height_deg / 2)) )# height in mm, just to check with ruler

		# empirical, for Arial 
		self.max_l_left  = -numpy.round(self.let_height_ptfont * 0.20)
		self.max_l_right = numpy.round(self.let_height_ptfont * 0.20 )
		self.min_spacing = numpy.round(self.let_height_ptfont/2.0)

