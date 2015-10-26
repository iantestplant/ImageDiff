REM Build script for ImageDiff
REM Requires py2exe and inno
set PYTHON_HOME=c:\tools\Python27
set target=ImageDiff
set version=0.2
set path=%QTDIR%\bin;%PYTHON_HOME%
set PYQTBASE=%PYTHON_HOME%

set iscc="%ProgramFiles(x86)%\Inno Setup 5\ISCC.exe"
rd /q/s distwin32
rd /q/s build

%PYTHON_HOME%\Lib\site-packages\PyQt4\pyrcc4.exe imageDiff.qrc -o imageDiff_rc.py
call pyuic4 -d ui\mainWindow.ui > ui\Ui_mainWindow.py

python setupWin32.py py2exe -isip

%iscc%  /F%target%-%version%.setupWindows "%target%.iss"
rd /q/s build
