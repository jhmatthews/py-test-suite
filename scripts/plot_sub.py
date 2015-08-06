#!/usr/bin/env python
'''
plot_sub.py contains some specific routines for making plots for easily comparing
results of regression tests
'''
from pylab import *
import numpy as np
import read_sub as sub
import os
from astropy.io import ascii

FOLDER = os.environ["PYTEST"]
FOLDER = FOLDER + "/plots/"

def make_standard_plot(s, name):

	fig = figure(figsize=(8.3,11.6))

	suptitle("Spectrum %s" % name)

	nplots = len(s.colnames) - 9
	nx = 2
	ny = (nplots + 1) / nx

	for i in range(nplots):
		subplot(ny, nx, i+1)
		plot(s["Lambda"], smooth(s[s.colnames[9+i]]))

	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%sspec_%s.png" % (FOLDER, name))
	clf()

	return 0


def make_components_plot(s, name):

	fig = figure(figsize=(8,8))
	suptitle("Spectrum components %s" % name)

	plot(s["Lambda"], smooth(s["Emitted"]), label="Emitted")
	plot(s["Lambda"], smooth(s["Disk"]), label="Disk")
	plot(s["Lambda"], smooth(s["Wind"]), label="Wind")
	plot(s["Lambda"], smooth(s["HitSurf"]), label="HitSurf")
	plot(s["Lambda"], smooth(s["Scattered"]), label="Scattered")
	legend()


	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%sspec_components_%s.png" % (FOLDER, name))
	clf()

	return 0



def make_log_spec_tot_plot(s, name):

	fig = figure(figsize=(8,8))
	suptitle("Logspectot: %s" % name)

	plot(s["Lambda"], smooth(s["Emitted"]), label="Emitted")
	plot(s["Lambda"], smooth(s["Disk"]), label="Disk")
	plot(s["Lambda"], smooth(s["Wind"]), label="Wind")
	plot(s["Lambda"], smooth(s["HitSurf"]), label="HitSurf")
	plot(s["Lambda"], smooth(s["Scattered"]), label="Scattered")
	legend()


	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%slogspectot_%s.png" % (FOLDER, name))
	clf()

	return 0

def make_log_spec_tot_comp_plot(s1, s2, name):

	fig = figure(figsize=(16,8))
	suptitle("Logspectot: %s (left) v Last Release (right)" % name)

	subplot(121)
	plot(s1["Lambda"], smooth(s1["Emitted"]), label="Emitted")
	plot(s1["Lambda"], smooth(s1["Disk"]), label="Disk")
	plot(s1["Lambda"], smooth(s1["Wind"]), label="Wind")
	plot(s1["Lambda"], smooth(s1["HitSurf"]), label="HitSurf")
	plot(s1["Lambda"], smooth(s1["Scattered"]), label="Scattered")
	legend()

	subplot(122)
	plot(s2["Lambda"], smooth(s2["Emitted"]), label="Emitted")
	plot(s2["Lambda"], smooth(s2["Disk"]), label="Disk")
	plot(s2["Lambda"], smooth(s2["Wind"]), label="Wind")
	plot(s2["Lambda"], smooth(s2["HitSurf"]), label="HitSurf")
	plot(s2["Lambda"], smooth(s2["Scattered"]), label="Scattered")
	legend()


	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%slogspectot_comp_%s.png" % (FOLDER, name))
	clf()



def make_components_comp_plot(s1, s2, name):

	fig = figure(figsize=(16,8))
	suptitle("Spectrum components: %s (left) v Last Release (right)" % name)

	subplot(121)
	plot(s1["Lambda"], smooth(s1["Emitted"]), label="Emitted")
	plot(s1["Lambda"], smooth(s1["Disk"]), label="Disk")
	plot(s1["Lambda"], smooth(s1["Wind"]), label="Wind")
	plot(s1["Lambda"], smooth(s1["HitSurf"]), label="HitSurf")
	plot(s1["Lambda"], smooth(s1["Scattered"]), label="Scattered")
	legend()

	subplot(122)
	plot(s2["Lambda"], smooth(s2["Emitted"]), label="Emitted")
	plot(s2["Lambda"], smooth(s2["Disk"]), label="Disk")
	plot(s2["Lambda"], smooth(s2["Wind"]), label="Wind")
	plot(s2["Lambda"], smooth(s2["HitSurf"]), label="HitSurf")
	plot(s2["Lambda"], smooth(s2["Scattered"]), label="Scattered")
	legend()


	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%scomponents_comp_%s.png" % (FOLDER, name))
	clf()










def make_geometry_plot(name):

	# read electron density from the file - could also try e.g. te or ionC4
	var = ["te", "tr", "ne", "nphot", "ioncH1", "ioncH2", "IP", "tot_lum"]


	fig = figure(figsize=(16.6,11.6))
	suptitle("Geometry: %s (left) v Python 78 (right)" % name)
	locs = [1,2,5,6,9,10,13,14]
	for i in range(len(var)):
		subplot(4,4,locs[i])
		x, z, value = sub.read_pywind_smart("%s.%s.dat" % (name, var[i]) )
		contourf(z,x,np.log10(value) )
		loglog()
		title("LOG " + var[i])
		colorbar()

		subplot(4,4,locs[i]+2)
		x, z, value = sub.read_pywind_smart("../../Python_78/wind_data/%s.%s.dat" % (name, var[i]) )
		contourf(z,x,np.log10(value) )
		loglog()
		title("LOG " + var[i])
		colorbar()

	savefig("geo_%s.png" % name)
	clf()


	var = ["ionHe1", "ionHe2", "ionC3", "ionC4", "ionC5", "ionN5", "ionO6", "ionSi4"]
	fig = figure(figsize=(16.6,11.6))
	suptitle("Ions: %s (left) v Python 78 (right)" % name)
	for i in range(len(var)):
		subplot(8,4,locs[i])
		x, z, value1 = sub.read_pywind_smart("%s.%s.dat" % (name, var[i]) )
		contourf(z,x,np.log10(value1) )
		loglog()
		title("LOG " + var[i])
		colorbar()

		subplot(8,4,locs[i]+2)
		x, z, value2 = sub.read_pywind_smart("../../Python_78/wind_data/%s.%s.dat" % (name, var[i]) )
		contourf(z,x,np.log10(value2) )
		loglog()
		title("LOG " + var[i])
		colorbar()



	savefig("ions_%s.png" % name)
	clf()

	return 0




def make_geometry_ratios(name):

	# read electron density from the file - could also try e.g. te or ionC4
	var = ["te", "tr", "ne", "nphot", "ioncH1", "ioncH2", "IP", "tot_lum"]


	figure(figsize=(8.3,11.6))
	suptitle("Difference Ratios Geometry: %s (left) v Python 78 (right)" % name)
	cont = [0.75,0.9,0.95,0.99,1.0,1.01,1.05,1.1, 1.25]

	for i in range(len(var)):

		subplot(4,2,i+1)
		x, z, value1 = sub.read_pywind_smart("%s.%s.dat" % (name, var[i]) )
		x, z, value2 = sub.read_pywind_smart("../../Python_78/wind_data/%s.%s.dat" % (name, var[i]) )

		print np.mean(value2/value1), var[i]

		contourf(z,x, value2/value1, cont, extend="both")
		loglog()
		title("LOG " + var[i])
		colorbar()

	savefig("geo_diff_%s.png" % name)
	clf()


	var = ["ionHe1", "ionHe2", "ionC3", "ionC4", "ionC5", "ionN5", "ionO6", "ionSi4"]
	figure(figsize=(8.3,11.6))
	suptitle("Difference Ratios Ions: %s (left) v Python 78 (right)" % name)

	for i in range(len(var)):

		subplot(4,2,i+1)
		x, z, value1 = sub.read_pywind_smart("%s.%s.dat" % (name, var[i]) )
		x, z, value2 = sub.read_pywind_smart("../../Python_78/wind_data/%s.%s.dat" % (name, var[i]) )

		contourf(z,x,value2/value1, cont, extend="both")
		loglog()
		title("LOG " + var[i])
		colorbar()



	savefig("ions_diff_%s.png" % name)
	clf()

	return 0



def make_residual_plot(s1, s2, name):

	fig = figure(figsize=(8.3,11.6))

	nplots = len(s1.colnames[9:])
	nx = 2
	ny = (nplots + 1) / nx

	suptitle("Spectrum Residuals: %s v Last Release" % name)

	print len(s2.colnames), len(s1.colnames)

	for i in range(len(s1.colnames[9:])):
		subplot(ny, nx, i+1)
		plot(s1["Lambda"], smooth(s1[s1.colnames[9+i]] - s2[s2.colnames[9+i]]))

	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%sresidual_%s.png" % (FOLDER, name))
	clf()
	return 0


def make_comp_plot(s1, s2, name):

	fig = figure(figsize=(8.3,11.6))

	nplots = len(s1.colnames[9:])

	if nplots > 1:
		nx = 2
		ny = (nplots + 1) / nx
	else: 
		nx = 1
		ny = 1

	suptitle("Comparison: %s v Last Release" % name)

	for i in range(len(s1.colnames[9:])):
		subplot(ny, nx, i+1)
		plot(s1["Lambda"], smooth(s1[s1.colnames[9+i]]), label=name)
		plot(s1["Lambda"], smooth(s2[s2.colnames[9+i]]), label="Last Release")
		if i == 0: legend()


	xlabel("Wavelength")
	ylabel("Flux")
	savefig("%scomp_%s.png" % (FOLDER, name))
	clf()

	return 0



def make_ion_plots_from_loop(suffix):


	ions = ["hydrogen", "helium", "oxygen", "nitrogen", "carbon", "iron"]

	nions = len(ions)

	figure(figsize=(16,12))

	suffix1 = "test"
	suffix2 = "release"
	f1 = os.environ["PYTEST"]+"/outputs/"
	f2 = os.environ["PYTEST"]+"/outputs_release/"




	suptitle("Ion fractions v U: crosses=release, lines=dev")
	cc = 'cmykrbgcmykrbgcmykrbgcmykrbg'

	for i in range(nions):

		subplot(3,2,i+1)


		data1 = np.loadtxt("%spy_%s_%s.dat" % (f1, ions[i], suffix1), unpack=True)
		data2 = np.loadtxt("%spy_%s_%s.dat" % (f2, ions[i], suffix2), unpack=True)

		for j in range(len(data1[1:])):

			plot(data1[0], data1[j+1],c=cc[j], label="Dev")
			scatter(data2[0], data2[j+1],c=cc[j], marker="x", label="Release")

		title(ions[i])
		#loglog()
		semilogx()
		semilogy()
		#ylim(0.98,1.02)
		

	savefig("%sions_loop_comp.png" % FOLDER)
	clf()






def make_hc_plots_from_loop(suffix):

	#suffix = sys.argv[2]
	ENV = os.environ["PYTEST"]
	names = [ENV+"/outputs/", ENV+"/outputs_release/"]
	labs = ["Dev", "Release"]

	suffixes = ["test", "release"]


	for i in range(len(names)):

		suffix = suffixes[i]

		print "%spy_heat_%s.dat" % (names[i], suffix)

		h = ascii.read("%spy_heat_%s.dat" % (names[i], suffix))
		c = ascii.read("%spy_cool_%s.dat" % (names[i], suffix))

		subplot(2,2,i+1)
		title("Cooling " + labs[i])

		for name in c.colnames[1:]:
			loglog(c["IP"], c[name], label=name)

		ylim(1e-20,1e-8)
		legend()


		subplot(2,2,3+i)
		title("Heating " + labs[i])

		for name in h.colnames[1:]:
			loglog(h["IP"], h[name], label=name)

		ylim(1e-20,1e-4)
		legend()


	savefig("%shc_curve.png" % FOLDER)
	clf()








def smooth(x,window_len=20,window='hanning'):
        if x.ndim != 1:
                raise ValueError, "smooth only accepts 1 dimension arrays."
        if x.size < window_len:
                raise ValueError, "Input vector needs to be bigger than window size."
        if window_len<3:
                return x
        if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
                raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
        s=np.r_[2*x[0]-x[window_len-1::-1],x,2*x[-1]-x[-1:-window_len:-1]]
        if window == 'flat': #moving average
                w=np.ones(window_len,'d')
        else:  
                w=eval('np.'+window+'(window_len)')
        y=np.convolve(w/w.sum(),s,mode='same')
        return y[window_len:-window_len+1]
