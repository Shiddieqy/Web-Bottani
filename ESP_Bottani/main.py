# https://pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
# https://towardsdatascience.com/automatic-vision-object-tracking-347af1cc8a3b

# import the necessary packages
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time

from scipy.signal import lfilter

# serial communication
from pySerialTransfer import pySerialTransfer as txfer
link = txfer.SerialTransfer('COM6')
link.open()
time.sleep(2)

# for motion prediction
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
poly = PolynomialFeatures(degree=2)

x_p = np.array([0]).reshape((-1, 1))
y_p = np.array([0])

x_parabola = poly.fit_transform(x_p)
regressor.fit(x_parabola, y_p)

# make np array int 300-600 every 5 point to predict
x_pred = np.array([i for i in range(1, 600, 10)]).reshape((-1, 1))

y_pred = regressor.predict(poly.fit_transform(x_pred))

def mapObjectPosition (x, y):
    print ("[INFO] Object Center coordinates at \
    X0 = {0} and Y0 =  {1}".format(x, y))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (64, 127, 101)
greenUpper = (127, 255, 255)
pts = deque(maxlen=args["buffer"])
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	vs = VideoStream(src=1).start()
# otherwise, grab a reference to the video file
else:
	vs = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(5.0)

# last 10 points
x_data = []
y_data = []

start_time = time.time_ns()
prev_x = 0
speed_x = 0

while True:
	send_size = 0

	# grab the current frame
	frame = vs.read()
	# handle the frame from VideoCapture or VideoStream
	frame = frame[1] if args.get("video", False) else frame
	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if frame is None:
		break
	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:		

		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			# mapObjectPosition(int(x), int(y))
			# print(str(int(x)) , str(int(y)))

			x_p = np.append(x_p, int(x)).reshape((-1, 1))
			y_p = np.append(y_p, int(y))

			#store last 10 points
			# x_data.append(int(x))
			# y_data.append(int(y))
			# if len(x_data) > 10:
			# 	x_data.pop(0)
			# 	y_data.pop(0)
			
			# x_avg = sum(x_data)/len(x_data)
			# y_avg = sum(y_data)/len(y_data)

			#update kecepatan x
			time_taken = (time.time_ns()-start_time)/1000000
			speed_x = (int(x) - prev_x)/time_taken
			prev_x = int(x)
			start_time = time.time_ns()

			list_ = [int(x), int(y)]
			list_size = link.tx_obj(list_)
			send_size += list_size

			link.send(send_size)

			while not link.available():
				if link.status < 0:
					if link.status == txfer.CRC_ERROR:
						print('ERROR: CRC_ERROR')
					elif link.status == txfer.PAYLOAD_ERROR:
						print('ERROR: PAYLOAD_ERROR')
					elif link.status == txfer.STOP_BYTE_ERROR:
						print('ERROR: STOP_BYTE_ERROR')
					else:
						print('ERROR: {}'.format(link.status))

			# rec_list_  = link.rx_obj(obj_type=type(list_),
            #                          obj_byte_size=list_size,
            #                          list_format='i')

			print('RCVD: {}'.format(speed_x))

		else:
			# reset the points from the camera
			x_p = np.array([0]).reshape((-1, 1))
			y_p = np.array([0]).reshape((-1, 1))
			
    # update the points from the camera
	x_parabola = poly.fit_transform(x_p)
	regressor.fit(x_parabola, y_p)

	# update the points from the prediction
	y_pred = regressor.predict(poly.fit_transform(x_pred))

	# update the points queue
	pts.appendleft(center)

	# make the point green color from the prediction
	# for i in range(len(x_pred)):
	# 	cv2.circle(frame, (int(x_pred[i]), int(y_pred[i])), 5, (0, 255, 0), -1)

    # loop over the set of tracked points
	for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore them
		if pts[i - 1] is None or pts[i] is None:
			continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
# otherwise, release the camera
else:
	vs.release()
# close all windows
cv2.destroyAllWindows()
