#!/usr/bin/python

import hashlib
import logging
import os
import qrcode


BUILDING=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
FLOOR=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
POSITION=[0, 1, 2, 3]
SALT=[PLEASE ADD YOUR SALT HERE]
URL = 'http://burnished-yeti-674.appspot.com/q/'

for i in BUILDING:
  for j in FLOOR:
    for k in POSITION:
      addr = "%s-%s-%s" % (i, j, k)
      name = hashlib.sha1(addr + SALT).hexdigest()
      im = qrcode.make(URL+name)
      im.save('../app/images/barcode/%s.png' % name)

     #  if not os.path.exists('../app/images/barcode/building-%s' % i):
    	# os.makedirs('../app/images/barcode/building-%s' % i)

     #  im.save('../app/images/barcode/building-%s/%s.png' % (i, name))
