#!/usr/bin/env python

# before we import any modules, set the environment variables in launchd. almost certainly a better way to do this
import os, sys
#os.system("source ~/.bash_profile")
#os.system("launchctl setenv PYTHONPATH $PYTHONPATH")
#os.system("launchctl setenv PYTEST $PYTEST")
#os.system("launchctl setenv PYTHON $PYTHON")


import datetime, time
import numpy as np
import plot_output




DATE = datetime.date.today()

print "\nOUTPUT for processing script\n"
print "DATE %s" % DATE

PYTEST = os.environ["PYTEST"]

print PYTEST

os.chdir(PYTEST)


#os.system("%s/scripts/process" % PYTEST) 

#time.sleep(30)


#names = ["fiducial_agn", "cv_standard", "balmer_test", "cv_macro_benchmark"]
names = ["1d_sn", "cv_standard", "fiducial_agn"]
success = np.zeros(len(names))
failed = []

plot_output.make_plots(names)

# check how many runs completed
for i in range(len(names)):

	name = names[i]

	run_passed = False

	f = open("%s/outputs/%s.sig" % (PYTEST, name))

	for line in f:
		if "COMPLETE" in line:
			success[i] = 1
			run_passed = True

	if run_passed == False:
		success[i] = -1
		failed.append(name)


print success
# check successes
# if there's a failure, email me
if success.all() == 1:
	print "Every run completed"
else:
	em = open("%s/email.txt" % PYTEST, "r")

	em.write("Failure on \n\n")
	em.write("Check Latest commit immediately\n\n")

	em.write("List of failures:")
	for model in failed:
		em.write("\tmodel")

	em.close()

	os.system("%s/scripts/email" % (PYTEST))



#commit to git and push
os.system("cd %s;\
          git commit -am 'Regression test for %s';\
          git push origin gh-pages" % (PYTEST, DATE) )


