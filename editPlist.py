
import os
version = os.environ["version"]
release = os.environ["release"]

print('version=%s release=%s'%(version, release))
s = open('Info_template.plist').read()
s = s.replace("[VERSION]", version)
s = s.replace("[RELEASE]", release)

plist = "dist/ImageDiff.app/Contents/Info.plist"
open(plist, 'w').write(s)

print "edited " + plist

