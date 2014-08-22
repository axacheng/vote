#!/usr/bin/python
import os

BUILDING=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

for b in BUILDING:
  all_files = os.listdir('./out/building-%s/' % b)

  for i in all_files:
  	name = i.split('.')[0]
  	print name
  	cmd='/usr/local/bin/wkhtmltopdf %s.html %s.pdf' % (name, name)
  	os.system(cmd)
