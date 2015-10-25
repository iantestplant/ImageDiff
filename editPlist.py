
import os
target = os.environ["target"]
version = os.environ["version"]
print target, version
plist = "dist/ImageDiff.app/Contents/Info.plist"
s = open(plist).read()
s = s.replace("org.pythonmac.unspecified", "com.testplant")
s = s.replace("0.0.0", version)

open("Info.plist", 'w').write(s)
os.remove(plist)
os.rename("info.plist", plist)
print "edited " + plist
