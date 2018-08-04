#!/usr/bin/env python
'''
Receive json-encoded post requests from function 'post_data()' in static/proto.js
'''
from bashcom import bashcom as bc
import cgi
import json
from PIL import Image

print

data = json.loads(cgi.FieldStorage()['package'].value)
instructions = data['instructions']
with open('image_data.json','r') as f:
	image_data = json.loads(f.read())
full = image_data['full']
cwd = image_data['cwd']

def TEST(data):
	with open('TEST','w') as f:
		f.write( str(data) )

def make_thumbnail(image_path):
	
	thumbsize = 200,200
	
	im = Image.open(image_path)
	im.thumbnail(thumbsize)
	#image = file(im.tostring().encode('utf8')).read()
	
	im.save('%s/tmp.jpg' % cwd)
	with open('%s/tmp.jpg' % cwd,'r') as f:
		image = f.read().encode('base64').replace('\n','')
	
	return image

def main():
	
	
	
	
	
	if instructions == 'get_image':
		'''  '''
		if not full:
			with open('%s/picsort_thumbnails/%s' % (cwd, data['image_name']) ,'rb') as f:
				image = f.read().encode('base64').replace('\n','')
			
		#'''
		#TEST(data['image_name'])
		else:
			with open('%s/%s' % (cwd, data['image_name']), 'rb') as f:
				image = f.read().encode('base64').replace('\n','')
		
		
		#image_path = '%s/%s' % (cwd, data['image_name'])
		#image = make_thumbnail(image_path)
		
		image = 'data:image/png;base64,{0}'.format(image)
		data['image'] = image
		print json.dumps( {'package' : data} )


	if instructions == 'make_new_dir':
		'''  '''
		new_dir_name = data['new_dir_name']
		new_dir_path = '%s/%s' % (cwd, new_dir_name) if not new_dir_name.startswith('/') else new_dir_name
		bc('mkdir %s' % new_dir_path)
		print json.dumps({'package' : data})
	
	
	if instructions == 'move_copy':
		'''  '''
		action 		= data['action'][0:3:2]
		image 		= data['image']
		new_dir 	= data['new_dir']
		
		#path = '%s/%s' % (cwd, image
		
		cmd = '%s %s/\"%s\" %s/%s/' % ( action, cwd, image, cwd, new_dir )
		
		#test(cmd)
		
		bc(cmd, shell=True)

		if action == 'mv':
			bc('rm %s/picsort_thumbnails/\"%s\"' % (cwd, image) , shell=True)
		
		print json.dumps({'package':data})
		
		pass
		
	
if __name__ == '__main__':
	main()