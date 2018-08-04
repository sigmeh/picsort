#!/usr/bin/env python
import os
import sys
from bashcom import bashcom as bc
import re
from PIL import Image
import json

installation_dir = os.path.dirname(os.path.realpath(__file__))

def test(msg):
	with open('TEST','w') as f:
		f.write(str(msg))

def generate_thumbnails( thumbsize ):
	''' Create directory picsort_thumbnails in cwd if it does not exist. 
		Collect names of image files, create and save thumbnails in cwd. '''
	
	with open('image_data.json','r') as f:
		image_data = json.loads(f.read())
	cwd = image_data['cwd']
	image_list = image_data['image_list']
	total_images = len(image_list)
	
	if not os.path.exists('%s/picsort_thumbnails' % cwd):
		bc('mkdir %s/picsort_thumbnails' % cwd)
	
	picsort_thumbnails_contents = [x for x in bc('ls %s/picsort_thumbnails' % cwd).split('\n') if x]
	
	### Create each image thumbnail if it does not exist
	for i,image in enumerate(image_list):
		if image in picsort_thumbnails_contents:
		 	print 'Found \"%s\" in picsort_thumbnails; skipping rewrite...' % image
		 	continue
		im = Image.open('%s/%s' % (cwd, image))
		im.thumbnail(thumbsize)
		im.save('%s/picsort_thumbnails/%s' % (cwd, image))	
		print 'Created thumbnail %d of %d' % (i+1, total_images)
	
	cwd_contents = bc('ls %s' % cwd).split('\n')
	cwd_dirs = [x for x in cwd_contents if os.path.isdir(x)]
	
	
	image_data = {'cwd' : cwd, 'image_list' : image_list}
	#image_data = {'cwd' : cwd, 'image_list' : image_list, 'cwd_dirs' : cwd_dirs}
	
	with open('%s/image_data.json' % installation_dir, 'w') as f:
		f.write(json.dumps(image_data))

def main():
	thumbsize = 400,400
	generate_thumbnails(thumbsize)
	pass
if __name__ == '__main__':
	main()