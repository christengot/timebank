import os
# Conversion dictionary for scopes
s = {"d": 1, "w": 7, "m": 30}
# Conversion dictionary for display units
u = {"m": 1, "h": 60, "d": 60*24}
# Path of bank file
path = "bank"

# Configures a (new or existing) bank.
# scope := scope of entire bank, options are "d", "w", "m"
# unit := display unit, options are "m", "h", "d", "b"
# sleep := time spent sleeping within sleep scope (in hours)
# s_scope := scope of time sleeping, options are same as scope
# c_path := custom path.
# All amounts of time are stored as minutes and converted when
# necessary.
def config(scope="w", unit="h", sleep=8, s_scope="d"):

	# Calculate value for sleep
	s_total = sleep * s[scope] / s[s_scope] * 60
	# So that it's writable
	s_total = str(s_total)

	# Save to bank (or make new one)
	global path
	try: os.rename(path, path + '~')
	except: of = open(path + '~', "w")
	nf = open(path, 'w')
	of = open(path + "~", 'r')
	nf.write(unit + "\n"), nf.write(scope + "\n")
	nf.write(s_scope + "\n"), nf.write(s_total + "\n")
	lines = of.readlines()
	for i in range(4, len(lines)):
		nf.write(lines[i])
	nf.close()
	of.close()
	os.remove(path + "~")

# Returns a number equaling the time left available in the bank.
def avail():
	global path
	with open(path, "r") as f:
		lines = f.readlines()
		i_num = []
		i_name = []
		i_total = int(lines[3])
		for i in range(4, len(lines)):
			item = lines[i].split(":", 1)
			i_num.append(item[1])
			i_name.append(item[0])
			i_total = i_total + int(item[1])
		global s
		max_t = int(s[lines[1].rstrip('\n')]) * 24 * 60
		global u
		print (max_t - i_total) / u[lines[0].rstrip('\n')]

# Adds a debit to the bank.  If no tag is specified, then
# "nc" = no category, is supplied.  A time must be supplied.
def debit(time, tag="nc"):
	global path
	with open(path, "a") as f:
		f.write(tag + ':' + str(time) + '\n')

# Shows the amount of hours spent on input tag.  If no tag
# is specified, all tag totals are shown.  form determines
# the measurement of each tag; no input uses default unit,
# "%" uses percentages.
def showt(tag="all", form=""):
	global path
	#TODO Maybe insert try-catch for "doesn't exist" error.
	with open(path, "r") as f:
		lines = f.readlines()
		tags = []
		times = []
		spent_t = 0
		for i in range(4, len(lines)):
			lines[i] = lines[i].rstrip('\n')
			item = lines[i].split(":", 1)
			item[1] = int(item[1])
			spent_t = spent_t + item[1]
			if item[1] in tags:
				times[tags.index(item[0])] += item[1]
			else:
				tags.append(item[0])
				times.append(item[1])
		
		total_t = 24 * 7 - 8 * 7
		# TODO fix ^
		if form == "%":
			for i in range(len(tags)):
				perc = 100 * times[i] / spent_t
				print "{0:20} : {1:10d}%".format(tags[i], perc)
			print "{0:20} : {1:10}%".format("Total", 100 * spent_t / total_t)
		elif form == "":
			for i in range(len(tags)):
				print "{0:20} : {1:10d}".format(tags[i], times[i])
			print "{0:20} : {1:10}/{2}".format("Total", total[0], total[1])
		# TODO: multiple tags, sorting, goals (productivity, etc)

