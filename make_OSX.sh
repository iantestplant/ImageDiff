#!/bin/bash
#
# QtHelp includes a dependancy on libQtCLucene.4.dylib, and this has a dependancy on QtCore.framework/Versions/4/QtCore which is not found in the app created by the setup.
# (User "otool -l" to show dependencies)
# This is really a problem with Qt that it installs libQtCLucene in /usr/lib and these are assumed to exist on every system so are not included by setup.
# Solution is to modify libQtCLucene.4.dylib to change the path to QtCore and include libQtCLucene.4.dylib in files.  It is then copied by setup into the app
# Also with the image plugin libraries they also require amending

cp /usr/lib/libQtCLucene.4.dylib .
install_name_tool -change QtCore.framework/Versions/4/QtCore  @executable_path/../Frameworks/QtCore.framework/Versions/4/QtCore libQtCLucene.4.dylib

rm -rf build dist

export target=ImageDiff
export version=1.0
export release=100
#After stuggling for hours with py2app, cx_freeze etc founf that the only packager that supports qt plugins (for the tiff handling) is pyinstaller
pyinstaller -w -i ImageDiff.icns --onefile ImageDiff.py

#echo "Now edit dist\imageDiff.app\Contents\info.plist for version etc"
python editPlist.py

#zip -y -r dist/imageDiff.zip . -i disp/imageDiff.app
