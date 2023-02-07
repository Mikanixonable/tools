import os
import glob


files = glob.glob("*.bmp")
for i, f in enumerate(files, 1):
	ftitle, fext = os.path.splitext(f)
	
	pos=ftitle.find('_')
	pos+=1
	ftitle = ftitle[pos:]
	os.rename(f,"uni"+hex(int(ftitle))[2:]+".bmp")