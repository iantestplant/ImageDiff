
# coding=UTF8
from distutils.core import setup
import py2exe
import os, sys

from distutils.core import setup
import py2exe
sys.argv.append('py2exe')
os.environ['path'] = os.environ['qtdir'] + r"\bin;" + os.environ['path']
target = os.environ["target"]
setup(
	version = os.environ['version'],
	name= target,
	description = "eggPlant image differencing",
	data_files = [('imageformats', [r'C:\Tools\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qico4.dll',
	r'C:\Tools\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qtiff4.dll',
	r'C:\Tools\Python27\Lib\site-packages\PyQt4\plugins\imageformats\qjpeg4.dll',
	])],
	zipfile = None,
	windows=[{
		"script": "imageDiff.py",
		"icon_resources": [(1, "imageDiff.ico")]
	} ],
	options = {
		"py2exe": {
			"includes": ['sip'],
			"excludes": [
				'unittest',
			],
			"optimize": 2,
			"bundle_files": 3,
			"dll_excludes": ['w9xpopen.exe',"MSVCP90.dll"],
			"dist_dir": 'distwin32',
		}
	}
)
