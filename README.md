# ImageDiff
TestPlant Image Differencing Tool

<b>Prerequisites for building.</b><br>


#Windows
* Python 2.7 or later.
* Qt 4
* PyQt4
* Py2Exe
Inno setup is used to create a windows installer in the Ouput folder, but a zip of distwin32 includes everything.
You will also need Visual C++ 2008 redistributable installed if you are not running the installer.
Unlike with pyinstaller on OSX I was not able to get a single bundled exe to work on windows.
<p>

<b>Building on windows:</b><br>
run make.bat.<br>
Files for distribution are in distwin32 and and the installer in Output

#OSX
* Python 2.7
* QT4 and PyQt can be installed using Macports.
* pyinstaller (pip install pyinstaller).  This was the only installer that would correctly enable the QT plugins for images to work.
For all image types other than png, plugin support in needed otherwise the bundled executable fails to read tiff or other formats.

<b>Building on OSX</b><br>
First build on win32 so the pyrrc4 tool is called to create the image resources and pyuic4 to generate the python from mainWindow.ui.

run make.bat.<r>
ImageDiff.app  is in the dist folder.

#ToDo
* Update the plist file in ImageDiff.app to include company data, copywrite etc.



