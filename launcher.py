import sys
import subprocess
import shlex
import os
from aau.shotgun import sg

platform_name = {'linux2': 'linux', 'darwin': 'mac', 'win32': 'windows'}[sys.platform]

toolkit_skripts_path = '//180net1/mnt$/software/shotgun/sX_JRG'
project_path = '//180net1/Collab/sX_JRG'

def is_user(name):

	return sg.find_one('HumanUser', [['login','is', name]], ['login'])

# Grab user name from system environment
system_user = os.environ['USERNAME'].lower()

# Try to find user with a given login on shotgun
# sg_user = is_user(system_user)
sg_user = None


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


# Determine the tank path for the current platforme
if platform_name == 'windows':
	TANK = toolkit_skripts_path + '/tank.bat'
elif platform_name == 'mac':
	TANK = toolkit_skripts_path + '/tank'


# Use first command line argument to determin next action
if sys.argv[1] == 'maya':

	# Configure maya environment
	os.environ['MAYA_SCRIPT_PATH'] = os.path.join(project_path, 'script')
	os.environ['PYTHONPATH'] = os.path.join(project_path, 'script')
	os.environ['PROJECT'] = project_path

	# Launch maya trough SG Toolkit
	subprocess.call(TANK + ' launch_maya')
	
elif sys.argv[1] == 'nuke':
	subprocess.call(TANK + ' launch_nuke')

elif sys.argv[1] == 'console':

	while True:

		user_command = raw_input("-> ")
		
		if len(user_command) > 0:
			user_command = user_command.split(' ')
			user_command.insert(0, TANK)
			subprocess.call(user_command)
		else:
			subprocess.call(TANK)