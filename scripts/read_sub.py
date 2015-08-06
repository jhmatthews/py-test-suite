#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
import numpy as np
import time
import sys
import os


class specclass:
    '''This is a class for storing any values read from a Python spec file'''	
    def __init__(self, fre, wave, emi, cen, dis, win, sca, hit, spe):
        self.freq = fre
        self.wavelength = wave
        self.emitted = emi
        self.censrc = cen
        self.disk = dis
        self.wind = win
        self.scattered = sca
        self.hitSurf = hit
        self.spec = spe

class spectotclass:
    '''This is a class for storing any values read from a Python spec_tot file'''   
    def __init__(self, fre, wave, emi, cen, dis, win, sca, hit):
        self.freq = fre
        self.wavelength = wave
        self.emitted = emi
        self.censrc = cen
        self.disk = dis
        self.wind = win
        self.scattered = sca
        self.hitSurf = hit


def read_spec_file (filename):
    
    '''reads a Python .spec file and places in specclass array,
       which is returned'''
    
    if not '.spec' in filename: 
        filename = filename + '.spec'
        
    
    # initialise the spectrum array with blank arrays
    spectrum = specclass ([],[],[],[],[],[], [], [], []) 
    
    # first read the file into a temporary storage array
    spectrum_temp = np.loadtxt (filename, comments ='#', unpack=True)
    
    # now set the correct elements of the class to be the temporary array
    spectrum.freq = spectrum_temp[0]
    spectrum.wavelength = spectrum_temp[1]
    spectrum.emitted = spectrum_temp[2]
    spectrum.censrc = spectrum_temp[3]
    spectrum.disk = spectrum_temp[4]
    spectrum.wind = spectrum_temp[5] 
    spectrum.scattered = spectrum_temp[7]
    spectrum.hitsurf = spectrum_temp[6]
    spectrum.spec = spectrum_temp[8:]
        
     #finally, return the spectrum class which is a series of named arrays      
    return spectrum




def read_spectot_file (filename):
    
    '''reads a Python .spec_tot file and places in spectotclass array,
       which is returned'''
    
    if not '.spec_tot' in filename: 
        filename = filename + '.spec_tot'
        
    
    # initialise the spectrum array with blank arrays
    spectrum = spectotclass ([],[],[],[],[],[], [], []) 
    
    # first read the file into a temporary storage array
    spectrum_temp = np.loadtxt (filename, comments ='#', unpack=True)
    
    # now set the correct elements of the class to be the temporary array
    spectrum.freq = spectrum_temp[0]
    spectrum.wavelength = spectrum_temp[1]
    spectrum.emitted = spectrum_temp[2]
    spectrum.censrc = spectrum_temp[3]
    spectrum.disk = spectrum_temp[4]
    spectrum.wind = spectrum_temp[5] 
    spectrum.scattered = spectrum_temp[6]
    spectrum.hitsurf = spectrum_temp[7]
    
    #finally, return the spectrum class which is a series of named arrays    
    return spectrum



def run_py_wind (vers, fname, cmds=None, ilv=None):
	'''
	run version vers of py_wind on file fname.wind_save
	'''

	if cmds == None:
		cmds = np.array(["1", "n","t", "l","t","p","0","6","r","v","1","2","3","-1", "I", "i","1","1","1","1","2","0","i","0", "1","1","1","2","2","2","2","1","2","3","6", \
			          "3","6","4","6","5","7","5","8","6","14","4","0","q"])

	x = cmds
	np.savetxt("_tempcmd.txt", x, fmt = "%s")


	isys = os.system('/Users/jmatthews/Documents/Python/bin/py_wind'+vers+' '+fname+' < _tempcmd.txt > tempfile &')
	time.sleep(3)

	# remove temporary file
	#os.system("rm -f _tempcmd.txt")
	return isys



def read_pywind_smart(filename, return_inwind=False):
	'''
	read a py_wind file using np array reshaping and manipulation
	'''

	# first, simply load the filename 
	d = np.loadtxt(filename, comments="#", dtype = "float", unpack = True)

	# our indicies are already stored in the file- we will reshape them in a sec
	zindices = d[-1]
	xindices = d[-2]

	# we get the grid size by finding the maximum in the indicies list 99 => 100 size grid
	zshape = int(np.max(zindices) + 1)
	xshape = int(np.max(zindices) + 1)


	# reshape our indices arrays
	xindices = xindices.reshape(xshape, zshape)
	zindices = zindices.reshape(xshape, zshape)

	# now reshape our x,z and value arrays
	x = d[0].reshape(xshape, zshape)
	z = d[1].reshape(xshape, zshape)

	values = d[2].reshape(xshape, zshape)

	# these are the values of inwind PYTHON spits out
	inwind = d[3].reshape(xshape, zshape)

	# create an inwind boolean to use to create mask
	inwind_bool = (inwind >= 0)
	mask = (inwind < 0)

	# finally we have our mask, so create the masked array
	masked_values = np.ma.masked_where ( mask, values )

	#print xshape, zshape, masked_values.shape

	#return the transpose for contour plots.
	if return_inwind:
		return x, z, masked_values.T, inwind_bool.T
	else:
		return x, z, masked_values.T





def read_convergence (root):
    root = "diag_%s/%s_0.diag" % (root, root)
    conv_fraction = []
    with open(root, 'r') as searchfile:
        for line in searchfile:

            # check if we have a matom_diagnostics line reporting level emissivities
            if 'Summary  convergence' in line:
                
                data = line.split()
                conv_fraction.append(float (data[3]))
    
            #print conv_fraction

    final_conv = conv_fraction [-1]
    return final_conv


def read_pf(root):

    if not ".pf" in root:
        root = root + ".pf"

    params, vals = np.loadtxt(root, dtype="string", unpack=True)

    pf_dict = dict()

    old_param = None 
    old_val = None

    for i in range(len(params)):


        # convert if it is a float
        try:
            val = float(vals[i])

        except ValueError:
            val = vals[i]

        if params[i] == old_param:

            if isinstance(pf_dict[params[i]], list):
                pf_dict[params[i]].append(val)

            else:
                pf_dict[params[i]] = [old_val, val]

        else:
            pf_dict[params[i]] = val

        old_param = params[i]
        old_val = val


    return pf_dict