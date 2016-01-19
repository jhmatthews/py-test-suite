#!/usr/bin/env python
'''
                    UNLV

Synopsis:  

This routine carries out a series of thin shell python simulations.
The wind mdot is set to produce a hydrogen density of 1e7 - to change
this one had to change the wind_mdot parameter. The loop is carried out
over the 2-10kev luminosity of the central source. A luminosity of
1e21 give a mainly neutral plasma (IP=5e-10) whilst 1e37 is almost 
totally ionized (IP=5e6). The code strips out ion densities and constructs 
data files with the cloudy type ionization parameter as the first 
line.
If one wants a constant temperature file, then one needs to hack python
to stop the temperature changing
We currently write out H,He,C,N,O and Fe. We also output heating and cooling
mechanisms.


Command line usage (if any):

	usage: python_pl_loop *optional file suffix*

Description:  

Primary routines:

Notes:
									   
History:

081214 nsh Commented

'''



import sys, subprocess
import py_read_output as r

#Use an optional suffix so file will be py_hydrogen_*suffix*.dat, 

#If nothing is supplied, default is PL.


python_ver= "py"+sys.argv[1]  	#This is where we define the version of python to use
run_name = sys.argv[2]
datafile = sys.argv[3]
ltransfer = "5"


#if  len(sys.argv) > 1:
#	run_name=sys.argv[1]
#	python_ver = "py"+run_name
#else:
#	run_name='tabnew'




npoints=81 			#this is the parameter which says how many runs to perform - we do 10 per order of magnitude in lum
dn = 160.0/(npoints - 1.) 
#Open empty files to contain data


Hout=open('py_hydrogen_'+run_name+'.dat','w')
Heout=open('py_helium_'+run_name+'.dat','w')
Cout=open('py_carbon_'+run_name+'.dat','w')
Nout=open('py_nitrogen_'+run_name+'.dat','w')
Oout=open('py_oxygen_'+run_name+'.dat','w')
Feout=open('py_iron_'+run_name+'.dat','w')
Tout=open('py_temperature_'+run_name+'.dat','w')
Heat=open('py_heat_'+run_name+'.dat','w')
Heat.write('IP total photo ff compton ind_comp lines\n')
Cool=open('py_cool_'+run_name+'.dat','w')

Cool.write('IP total recomb ff compton DR DI lines Adiabatic\n')



for i in range(npoints):
	lum=10**((dn*float(i)+210.0)/10.0)   #The 210 means the first luminosity is 21.0
	print 'Starting cycle '+str(i+1)+' of '+str(npoints)
	print 'Lum= '+str(lum)
	pf_template = r.read_pf("ion_loop_template.pf")
	pf_template ["Atomic_data"] = "data/%s" % datafile
	pf_template ["Line_transfer()"] = "%s" % ltransfer)]
	pf_template ["lum_agn(ergs/s)"] = str(lum)
	
	r.write_pf("input.pf", pf_template)

	subprocess.check_call("time "+python_ver+" input > output",shell=True)	   #This is where we define the version of python to use
	subprocess.check_call("tail -n 60 output  | grep OUTPUT > temp",shell=True)#Strip the last 60 lines from the output
	inp=open('temp','r')
	for line in inp.readlines():
		data=line.split()
		if (data[1]=='Lum_agn='):       #This marks the start of the data we want. Field 14 is the cloudy ionization parameter
			Hout.write(data[14])
			Heout.write(data[14])
			Cout.write(data[14])
			Nout.write(data[14])
			Oout.write(data[14])
			Feout.write(data[14])
			Heat.write(data[14])
			Cool.write(data[14])
			Tout.write('Lum= '+data[2]+' Sim_IP= '+data[12]+' Cloudy_IP= '+data[14]+' T_e= '+data[4]+' N_e= '+data[8]+'\n')
                if (data[1]=='Absorbed_flux(ergs-1cm-3)'):
			Heat.write(' '+data[2]+' '+data[4]+' '+data[6]+' '+data[8]+' '+data[10]+' '+data[12]+'\n')
		if (data[1]=='Wind_cooling(ergs-1cm-3)'):
     			Cool.write(' '+data[2]+' '+data[4]+' '+data[6]+' '+data[8]+' '+data[10]+' '+data[12]+' '+data[16]+' '+data[14]+'\n')
		if (data[1]=='H'):
			for j in range(2):
				Hout.write(' '+data[j+2])
			Hout.write('\n')
		if (data[1]=='He'):
			for j in range(3):
				Heout.write(' '+data[j+2])
			Heout.write('\n')
		if (data[1]=='C'):
			for j in range(7):
				Cout.write(' '+data[j+2])
			Cout.write('\n')
		if (data[1]=='N'):
			for j in range(8):
				Nout.write(' '+data[j+2])
			Nout.write('\n')
		if (data[1]=='O'):
			for j in range(9):
				Oout.write(' '+data[j+2])
			Oout.write('\n')
		if (data[1]=='Fe'):
			for j in range(27):
				Feout.write(' '+data[j+2])
			Feout.write('\n')
#Flush the output files so one can see progress and if the loop crashes all is not lost
	Hout.flush()
	Heout.flush()
	Cout.flush()
	Nout.flush()
	Oout.flush()
	Feout.flush()
	Tout.flush()
	Heat.flush()
	Cool.flush()	
	print 'Finished cycle '+str(i+1)+' of '+str(npoints)
#Close the files.
Hout.close()
Heout.close()
Cout.close()
Nout.close()
Oout.close()
Feout.close()
Tout.close()
Heat.close()
Cool.close()

