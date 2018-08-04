#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
import cgitb
import time
import subprocess as sp
import sys
import os


installation_dir = os.path.dirname(os.path.realpath(__file__))

def start_server( port ):
	server=BaseHTTPServer.HTTPServer
	handler=CGIHTTPServer.CGIHTTPRequestHandler
	server_address=("", int(port) )
	#handler.cgi_directories=['%s' % installation_dir]
	handler.cgi_directories=['/','cgi-bin']

	httpd=server(server_address, handler)
	httpd.serve_forever()


def main():
	
	port = sys.argv[1]
	
	try:
		start_server( port )
		
	except:
		
		py_proc = sp.Popen(['ps -fA | grep python'], stdout=sp.PIPE, shell=True).communicate()[0]
		serv_proc = sp.Popen(['ps -fA | grep server'], stdout=sp.PIPE, shell=True).communicate()[0]
		
		time.sleep(.5)
		
		print
		print 'Cannot start server...'
		print 'The following information is available:'
		print '#--------python processes--------#'
		print py_proc
		print '#--------------------------------#'
		print '#--------server processes--------#'
		print serv_proc
		print '#-----------------------------------#'
		print
		print 'Kill active server.py processes running elsewhere if necessary.'
		print
		
if __name__ == '__main__':
	main()