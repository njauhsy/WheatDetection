# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 16:40:08 2019

@author: 术玉
"""

import cv2

def livedetect():
  cap = cv2.VideoCapture(0)

# Create the haar cascade
  faceCascade = cv2.CascadeClassifier("haar_adaboost_data//xml//cascade.xml")

  while(True):
	# Capture frame-by-frame
	  ret, frame = cap.read()

	# Our operations on the frame come here
	  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	  wheat = faceCascade.detectMultiScale(
		  gray,
		  scaleFactor=1.1,
		  minNeighbors=5,
		  minSize=(30, 30)
		#flags = cv2.CV_HAAR_SCALE_IMAGE
	  )

	  #print("Found {0} wheat!".format(len(wheat)))
	  num=format(len(wheat))

	# Draw a rectangle around the faces
	  for (x, y, w, h) in wheat:
		  cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


	# Display the resulting frame
	  cv2.imshow("'Esc' to quit and 'q' to save", frame)
	  if cv2.waitKey(1)==27:break
	  #if cv2.waitKey(1)=='s':break
	  if cv2.waitKey(1)& 0xFF== ord('q'):
		  i=0
		  cv2.imwrite('user_data//result//live_'+str(i)+'.jpg',frame)
		  imagepath1='user_data//result//live_'+str(i)+'.jpg'
		  i=i+1
		  break
      



# When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()
  return imagepath1,num
  
  
