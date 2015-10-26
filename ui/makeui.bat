set PYTHON_HOME=c:\tools\Python27
set path=%QTDIR%\bin;%PYTHON_HOME%
call pyuic4 -d mainWindow.ui > Ui_mainWindow.py
%PYTHON_HOME%\Lib\site-packages\PyQt4\pyrcc4.exe imageDiff.qrc -o imageDiff_rc.py
