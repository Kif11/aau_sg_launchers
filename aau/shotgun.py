import shotgun_api3 as sgapi

# Login to SG
SERVER_PATH = 'https://aau.shotgunstudio.com' # change this to http if you have a local install not using HTTPS
SCRIPT_USER = 'util'
SCRIPT_KEY = 'cf1e303b918f7cab09c73ae4a100d89f596410f25690a41ba21d6211797d1daf'

sg = sgapi.Shotgun(SERVER_PATH, SCRIPT_USER, SCRIPT_KEY)