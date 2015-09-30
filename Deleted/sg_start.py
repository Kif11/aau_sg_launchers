import sys
import subprocess
import shlex
import os

platform_name = {'linux2': 'linux', 'darwin': 'mac', 'win32': 'windows'}[sys.platform]

cwd = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')

sys.path.append(cwd + "/install/core/python")
sys.path.append(cwd + "/install/core/python/tank_vendor")

import sgtk
import shotgun_api3 as sgapi

if platform_name == 'windows':
	TANK = cwd + '/tank.bat'
elif platform_name == 'mac':
	TANK = cwd + '/tank'

# Login to SG
SERVER_PATH = 'https://aau.shotgunstudio.com' # change this to http if you have a local install not using HTTPS
SCRIPT_USER = 'util'
SCRIPT_KEY = 'cf1e303b918f7cab09c73ae4a100d89f596410f25690a41ba21d6211797d1daf'
sg = sgapi.Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)

# List all students on shotgun
students = sg.find("HumanUser", [], ["sg_student_login"])
student_list = [student['sg_student_login'] for student in students]

print TANK

login_success = False
while not login_success:

	user_login = raw_input("Enter your user name on Shotgun: ")

	# Check if the user name exists on SG
	if user_login in student_list:
		# Set user name environmental variable to his login that Shotgun
		# hook can corectly resolve it
		os.environ['USERNAME'] = user_login
		login_success = True

		print "Welcome to SG Toolkit command line interface. To list all available commands hit enter."
	else:
		print "Can not find", user_login, "user on Shotgun"


while True:

	user_command = raw_input("-> ")
	
	if len(user_command) > 0:
		user_command = user_command.split(' ')
		user_command.insert(0, TANK)
		subprocess.call(user_command)
	else:
		subprocess.call(TANK)