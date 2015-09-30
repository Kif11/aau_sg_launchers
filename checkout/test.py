import os

def make_launcher():

	
	content = '''@echo off
set PROJECT=%cd%
set MAYA_PROJECT=%cd%
"C:\Program Files\Autodesk\Maya2015\bin\maya.exe"'''

	script_name = 'RunMayaClient.bat'
	script = os.path.join('D:/', script_name)

	with open(script, 'w') as f:
			f.write(content)


make_launcher()