import os
import time
# Conversion dictionary for scopes
s = {"d": 1, "w": 7, "m": 30}
# Conversion dictionary for display units
u = {"m": 1, "h": 60, "d": 60*24}
# Conversion dictionary for scope names
sn = {"d": "day", "w": "week", "m": "month"}
# Path of bank file
bank_path = "mybank"

# Creates the initial "bank" file and fills in 
# default values (unless custom ones are
# submitted.
# "unit" := Display unit for time amounts.  Options
# are "m" (minute), "h" (hour), "d" (day), "b" (.beat).
# "scope" := Current span of time in frame. Options
# are "d" (day), "w" (week), "m" (month).
# "sleep" := Amount of sleep per "s_scope". Used
# in calculating the sleep estimate for the scope.
# Use 0 if you want to manually add/track sleep at
# each occurrence.
# "s_sleep" := Scope of sleep
def setup(scope="w", unit="h", sleep=8, s_scope="d"):
	# Save to bank (or make new one)
	try: open(bank_path, "r")
	except:
		print "Bank already exists! Use individual config"
		print "functions or delete old bank."
	else:
		with open(bank_path, "w") as f:
			t_sleep = sleep * s[scope] / s[s_scope] * 60
			f.write(unit + '\n'), f.write(scope + '\n'),
			f.write(s_scope + '\n'), f.write(str(sleep) + '\n'),
			f.write(str(t_sleep) + '\n')

# Changes individual settings. See "setup()" for details
# about settings.
# NOTE: If program crashes executing this command (for
# example, when forgetting quotes around a char value),
# make sure to restore the bank with the backup file
# (usually bank~) before running any more commands, to
# prevent bank content loss.
def change(setting, value):

	# See if bank exists
	try: open(bank_path, "r")
	except: print "No bank exists to change."

	# Perform change
	os.rename(bank_path, bank_path + '~')
	with open(bank_path + '~', "r") as of:
		with open(bank_path, "w") as nf:
			if setting == "unit":
				nf.write(str(value) + '\n')
				of.seek(2)
				is_scope = 3
			else: nf.write(of.readline())
			if setting == "scope":
				nf.write(str(value) + '\n')
				of.seek(4)
				is_scope = 2
			else: nf.write(of.readline())
			if setting == "s_scope":
				nf.write(str(value) + '\n')
				of.seek(6)
				is_scope = 1
			else: nf.write(of.readline())
			if setting == "sleep":
				nf.write(str(value) + '\n')
				of.seek(8)
				is_scope = 0
			else: nf.write(of.readline())
			nf.write(str(update(bank_path + '~', value, is_scope)) + '\n')

			# Copy the items, if they exist
			of.seek(0)
			lines = of.readlines()
			if len(lines) > 5:
				for i in range(5, len(lines)): 
					nf.write(lines[i])

	# Remove backup file (comment out to disable removal)
	os.remove(bank_path + '~')

# Updates sleep estimate.  Sleep estimate is used in
# predicting time remaining in bank spent awake. If
# you want all estimates of time remaining to not
# subtract estimated sleep, make this value 0.
# (You also have the option of manually
# managing sleep using "debit()"/"credit()" functions.)
# "update()" is run automatically when "sleep" values
# are changed, and therefore should never really be
# invoked manually.
def update(pathto, value, is_scope):
	with open(pathto, "r+") as f:
		if is_scope == 3:
			unit = value
			f.seek(2)
			scope = f.read(1)
			f.seek(4)
			s_scope = f.read(1)
			f.seek(6)
			sleep = int(f.read(1))
		elif is_scope == 2:
			scope = value
			f.seek(4)
			s_scope = f.read(1)
			f.seek(6)
			sleep = int(f.read(1))
			f.seek(0)
			unit = f.read(1)
		elif is_scope:
			s_scope = value
			f.seek(6)
			sleep = int(f.read(1))
			f.seek(2)
			scope = f.read(1)
			f.seek(0)
			unit = f.read(1)
		else:
			sleep = int(value)
			f.seek(4)
			s_scope = f.read(1)
			f.seek(2)
			scope = f.read(1)
			f.seek(0)
			unit = f.read(1)
		t_sleep = sleep * s[scope] / s[s_scope] * 60
		return t_sleep

# Returns a number equaling the time left available in the bank.
def avail():
	with open(bank_path, "r") as f:
		lines = f.readlines()
		i_num = []
		i_name = []
		i_total = int(lines[3])
		for i in range(4, len(lines)):
			item = lines[i].split(":", 1)
			i_num.append(item[1])
			i_name.append(item[0])
			i_total = i_total + int(item[1])
		max_t = int(s[lines[1].rstrip('\n')]) * 24 * 60
		print (max_t - i_total) / u[lines[0].rstrip('\n')]

# Adds a debit to the bank.  If no tag is specified, then
# "nc" = no category, is supplied.  A time must be supplied.
def debit(time, tag="nc"):
	global unit
	with open(bank_path, "a+") as f:
		unit = f.read(1)
		f.write(tag + ':' + str(time * u[unit]) + '\n')

# Shows the amount of hours spent on input tag.  If no tag
# is specified, all tag totals are shown.  "form" determines
# the measurement of each tag; no input uses default unit,
# "%" uses percentages.
def showt(tag="all", form=""):

	#TODO Maybe insert try-catch for "doesn't exist" error.
	with open(bank_path, "r") as f:
		lines = f.readlines()
		tags = []
		unit = lines[0].rstrip('\n')
		scope = lines[1].rstrip('\n')
		times = []
		spent_t = 0
	
	# If there are no items in bank yet, no show.  Otherwise
	if len(lines) < 5:
		print "No data to display yet. Add some with debit()"
	else:
		for i in range(5, len(lines)):
			lines[i] = lines[i].rstrip('\n')
			item = lines[i].split(":", 1)
			item[1] = int(item[1])
			spent_t = spent_t + item[1]
			if item[0] in tags:
				times[tags.index(item[0])] += item[1]
			else:
				tags.append(item[0])
				times.append(item[1])
		# Calculate total time in scope
		total_t = s[scope] * 24 * 60
		print "This {0}".format(sn[scope])
		if form == "%":
			for i in range(len(tags)):
				perc = 100 * times[i] / total_t
				print "{0:20} : {1:10d}%".format(tags[i], perc)
			print "{0:20} : {1:10}%".format("Total", 100 * spent_t / total_t)
		elif form == "":
			for i in range(len(tags)):
				print "{0:20} : {1:10d}".format(tags[i], times[i] / u[unit])
			print "{0:20} : {1:10} /{2}".format("Total", spent_t / u[unit], total_t / u[unit])

# Not yet implemented.
def credit(time, tag, message=""):
	pass

# Starts tracking time for an activity.
def start(tag):
	# Create file for recording
	with open(tag, "w") as f:
		f.write(str(int(time.time())))

# Ends timing an activity, returns time spent.
def end(tag):
	# Reopen record file
	with open(tag, "r") as f:
		diff = int(time.time()) - int(f.readline())
		# Diff is in seconds, return in minutes
		return diff / 60

