#!/usr/bin/env python
#import read_sub as sub
import py_read_output as rd 
import py_plot_util as util
import plot_sub as p
from pylab import * 
import numpy as np 
import sys
import os
from astropy.io import ascii

'''
usage
 e.g. python plot_output.py 
'''
  
FOLDER = os.environ["PYTEST"] + "/outputs/"
BENCH_FOLDER = os.environ["PYTEST"] + "/outputs_release/"

def make_plots(names):  

	try:
		VERSION=""
		f = open("%s%s.out" % (FOLDER,names[0]), "r")
		for line in f:
			data = line.split()
			if len(data) > 2:
				if data[0] == "!!Python" and data[1]=="Version":
					VERSION = data[2]

			#if data[0] == "!!Python" and data[1]=="Version":

	except IOError:
		print "Couldn't read version"
		VERSION=""
		


	print "VERSION %s" % VERSION

	for i in range(len(names)):

		shortname = names[i]
		name = FOLDER + shortname
		benchname = BENCH_FOLDER + shortname

		pf_dict = rd.read_pf(name)						# read in pf file

		try:
			convergence = rd.read_convergence (name + ".out")		# get convergence of model
		except IndexError:
			print "Couldn't read convergence info for root %s, possible failure" % name

		print "Model %s" % name
		print "%.2fpc Converged" % (100.0*convergence)

		# run py_wind- only need to run this to create the files
		util.run_py_wind(name, vers=VERSION)

		#p.make_geometry_plot(name)					# make plots of pywind quantities
		#p.make_geometry_ratios(name)


		# this is the current dev spectral file
		make_plots=True
		try:
			s = rd.read_spectrum(name)
		except IOError:
			print "Couldn't read spectrum for root %s, possible failure" % name
			make_plots = False

		# this is the benchmark spectral file to test against
		if make_plots:
			s_bench = rd.read_spectrum(benchname)

			get_standard_dev(shortname, s, s_bench)

			# just make some standard spectrum plots
			#p.make_standard_plot(s, shortname)
			#p.make_components_plot(s, shortname)

			p.make_residual_plot(s, s_bench, shortname)		# make residual plots
			p.make_comp_plot(s, s_bench, shortname)			# make comparison plots
			p.make_components_comp_plot(s, s_bench, shortname)	# make components comparison plots



		# this is the current dev spectot file
		#s = sub.read_spectot_file (name)

		# this is the benchmark spectot file to test against
		#s_bench = sub.read_spectot_file(benchname)

		#p.make_log_spec_tot_plot(s, name)
		#p.make_log_spec_tot_comp_plot(s, s_bench, name)

		p.make_hc_plots_from_loop (shortname)
		p.make_ion_plots_from_loop (shortname)




	# move all the wind data somewhere out the way
	#os.system("mkdir wind_data")
	#os.system("mv *.dat wind_data/")
	#os.system("open -a preview *.png")

	print "all done"

	return 0



def get_standard_dev(run_name, s1, s2):

	sd_dict = dict()

	for i in range(2,len(s1.colnames)):

		sd = get_one_standard_dev(s1[s1.colnames[i]], s2[s1.colnames[i]])

		mean = np.mean(s1[s1.colnames[i]])

		print "Run %s: Column %s Normalised Standard deviation in flux = %8.4e Mean %8.4e" % (run_name, s1.colnames[i], sd, mean)

	return 0






def get_one_standard_dev(array1, array2):

	'''
	array-like arguments
	'''

	N = len(array1)

	diff = (array1 - array2)

	diffsquaredsum = np.sum(diff * diff)

	SD = np.sqrt(diffsquaredsum / N)

	return SD






