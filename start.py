#!/usr/bin/env python
'''
Script to start localhost server (as server.py)
1. Get port number for new server (default is 8000); confirm port is between 1-65535
2. Check for running server and kill if necessary
3. Rewrite new port numbers to html file if necessary

Usage:
	$ python start.py [port]
'''

import subprocess as sp
from bashcom import bashcom as bc
import time
import requests
import kill_server
import sys
import re
import os
import json

installation_dir = os.path.dirname(os.path.realpath(__file__))
cwd = os.getcwd()

def p(m):
	#print statement wrapper
	print m

#
#
def get_port():
	'''	Retrieve port via sys.argv, raw_input, or set default (8000)
		Ensure port is valid; otherwise raise excetion
	'''
	'''
	if len(sys.argv) > 1:
		port = sys.argv[1]
	else:
		port = raw_input('Enter port number or hit enter for default (8000): ')
	'''
	port = raw_input('Enter port number or hit enter for default (8000): ')	
	if not port:
		port = 8000
	
	try:
		port = int(port)
		if not 1024 <= int(port) <= 65535:
			raise Exception
	except Exception as e:
		sys.exit('Port must be a number 1024-65535\nTraceback:\n%s' % e)
		
	return port

#
#
def check_localhost( port ):
	''' Check for active server at given port; 404 suggests root directory is elsewhere; kill it '''
	
	r = requests.get('http://127.0.0.1:%s/picsort' % port)
	
	
	#'''
	if r.status_code == 404:
		print 'Got 404 message; attempting server kill'		
		kill_server.main()
	else:
		print 'Returned status code:', r.status_code
		if r.status_code == 200:
			print 'Opening page...'
			cmd = ('open http://localhost:%s/picsort' % port).split()
			sp.Popen(cmd)	#open in default browser
			return	
	#'''
	start( port )

#
#
def start( port ):
	
	try:
		write_new_port( port )		
		time.sleep(0.1)

		print 'Starting new python server on port %s...' % port
		cmd = ('python server.py %s &' % port )
		sp.Popen(cmd,  shell=True, cwd=installation_dir )
		time.sleep(.5)
	
		#open default page
		cmd = ('open http://localhost:%s/picsort' % port).split()
		sp.Popen(cmd)	#open in default browser
		
	except Exception as e:
		print 'Error found:',e
		time.sleep(.5)
		print 'Cannot start server.'

#	
#		
def write_new_port( port ): 
	''' Rewrite picsort.html to fill in appropriate port number (port number will be rewritten even if unchanged) 
		This will overwrite port numbers for all local urls within {{picsort}}.html (i.e., script/link tags)
	'''
	
	with open('%s/picsort.html' % installation_dir , 'r') as f:
		doc = f.read()
	
	local_urls = re.findall('http\:\/\/localhost\:\d+\/[\w\/\.]+\'', doc)
	for i in local_urls:
		new_url = re.sub('\:\d+\/',':%s/' %port,i)
		doc = re.sub(i, new_url, doc)
#
#		
def main():
	''' Get port number or accept 8000 as default; check for localhost connection; kill if necessary, then start new server'''
	
	#kill_server.main()
	time.sleep(.1)
	port = get_port()
	
	print 'Initializing server...'
	
	try:
		raise
		#check_localhost( port )
		
	except:
		print '''No connection to localhost found; starting server'''
		#print 'error'
		start( port )

	
		
if __name__ == '__main__':
	main()

