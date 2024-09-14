# -*- coding: UTF-8 -*-
from PIL import ImageGrab
import os


import os
import sys 
import subprocess as commands
import hashlib
import time

class Uploader:

	__file = None

	project_path = ''
	github_username = ''
	github_repo = ''

	# default master branch
	# __MARKDOWN_IMG_URL = '![{}](https://github.com/{}/{}/raw/master/{})';
	# __MARKDOWN_IMG_URL = '![{}](https://cdn.jsdelivr.net/gh/{}/{}/{})';
	__MARKDOWN_IMG_URL = '![{}](https://raw.wangyitu.tech/{}/{}/main/{})';


	def __init__(self, file):
		self.__file = file
		self.github_username = os.environ.get('github_username')
		self.github_repo = os.environ.get('github_repo')
		self.project_path = os.environ.get('project_path')
		# self.project_path ="/Users/wangjun/Code/GITHUB/pic" 
		# self.github_username = "pekaboo"
		# self.github_repo = "https://github.com/pekaboo/pic.git"

		self.run()

	def run(self):
		notify('Uploading','Please wait for a while')
		# Image suffix
		a,b,suffix = self.__file.filename.rpartition('.')


		# Get image
		filename = str(hashlib.md5(self.__file.filename.encode('utf-8')).hexdigest())+str(int(time.time()))+'.'+suffix
		if os.environ.get('github_dir'):
			filename = os.environ.get('github_dir') +'/'+filename
		if not os.path.exists(self.project_path):
			os.makedirs(self.project_path)
		self.__file.save(os.path.join(self.project_path, filename))

		# Git
		cmd = '''
		cd {}
		git add .
		git commit -m 'clipboard'
		git push'''.format(self.project_path)

		a,b = commands.getstatusoutput(cmd)

		if a == 0:
			self.__write_to_doc(filename)
			notify('Success','Upload success')
		else:
			# Alfred workflow debugger console
			sys.stderr.write(str(b))
			notify('Error','Git error')

	def __write_to_doc(self, filename):
		if os.environ.get('github_dir'):
			filename = os.environ.get('github_dir') +'/'+filename
		remote_url = self.__MARKDOWN_IMG_URL.format(filename,self.github_username,self.github_repo,filename)
		os.system('echo "{}"|pbcopy'.format(remote_url))
		a,b = commands.getstatusoutput('pbpaste')
		self.print_pasteboard_content()

	# this func is forked from `kaito-kidd/markdown-image-alfred` thanks
	def print_pasteboard_content(self):
		"""从剪贴板打印出内容"""
		write_command = (
			'osascript -e \'tell application '
			'"System Events" to keystroke "v" using command down\''
		)
		os.system(write_command)




def notify(title, text):
    os.system("""
            osascript -e 'display notification "{}" with title "{}" sound name "Glass"'
            """.format(text, title))
def main():
	# Issue: if your screen is extend, please make sure the `Screen show profile` is LCD or normal RGB
	try:
		# Get latest file from os clipboard
		img = ImageGrab.grabclipboard()

	except BaseException as e:
		notify('Error',str(e))
	else:
		if img is not None:
			# Move and upload
			Uploader(img)
		else:
			notify('Empty','The clipboard is empty')

def function():
	pass


if __name__ == '__main__':
	main()