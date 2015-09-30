import sys
import subprocess
import shlex
import os

platform_name = {'linux2': 'linux', 'darwin': 'mac', 'win32': 'windows'}[sys.platform]

script_dir = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

sys.path.append(script_dir + "/install/core/python")
sys.path.append(script_dir + "/install/core/python/tank_vendor")

import sgtk
import shotgun_api3 as sgapi

# Login to SG
SERVER_PATH = 'https://aau.shotgunstudio.com' # change this to http if you have a local install not using HTTPS
SCRIPT_USER = 'util'
SCRIPT_KEY = 'cf1e303b918f7cab09c73ae4a100d89f596410f25690a41ba21d6211797d1daf'
sg = sgapi.Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

def is_user(name):

	return sg.find_one('HumanUser', [['login','is', name]], ['login'])


cwd = os.getcwd()

# Grab user name from system environment
system_user = os.environ['USERNAME'].lower()

# Try to find user with a given login on shotgun
sg_user = is_user(system_user)

if sg_user != None:
	login_success = True
else:
	login_success = False

# If user name doesn exist on SG ask user to enter correct one
while not login_success:

	user_login = raw_input("Enter your user name on Shotgun: ")

	# Check if the user name exists on SG
	sg_user = is_user(user_login)

	if sg_user != None:
		# Set user name environmental variable to his login that Shotgun
		# hook can corectly resolve it
		os.environ['USERNAME'] = user_login
		login_success = True

	else:
		print "Can not find", user_login, "user on Shotgun"

if login_success:
	print "Successufuly login!"

# Configure maya environment
os.environ['MAYA_SCRIPT_PATH'] = os.path.join(cwd, 'script')
os.environ['PYTHONPATH'] = os.path.join(cwd, 'script')
os.environ['PROJECT'] = cwd

# Determine the tank comand for the current platforme
if platform_name == 'windows':
	TANK = script_dir + '/tank.bat'
elif platform_name == 'mac':
	TANK = script_dir + '/tank'

# Launch maya trough SG Toolkit
subprocess.call(TANK + ' launch_nuke')