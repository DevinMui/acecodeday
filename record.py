import cv2
import requests
#from pymouse import PyMouse
#from pykeyboard import PyKeyboard

cap = cv2.VideoCapture(0)

url = "http://localhost:3000"

# haar haar haar cascades
fist_cascade = cv2.CascadeClassifier('fist.xml')
palm_cascade = cv2.CascadeClassifier('palm.xml')

init_palm_area = 0

init_fist_area = 0

# mouse positiions
last_x = 0
last_y = 0

detected = False

while True:
	ret, frame = cap.read()

	fist_area = 0
	palm_area = 0

	# change to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detection
	fists = fist_cascade.detectMultiScale(gray, 1.3, 5)
	palms = palm_cascade.detectMultiScale(gray, 1.3, 5)

	# detect palms and fists
	for x,y,w,h in palms: # typically, < 5000 is a false positive
		if w * h < 4000:
			print "probably a false positive"
		else:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			if init_palm_area == 0: # set the init area for comparisons later
				init_palm_area = w * h
			else:
				palm_area = w * h
			print "PALM"

	for x,y,w,h in fists:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		if init_fist_area == 0: # set the init area for comparisons later
			init_fist_area = w * h
		else:
			fist_area = w * h

		print "FIST"

	# for these actions, we will need a specific zone
	# or range for the equal so that it is not hard to stop moving

	# these actions will move the mouse position depending if detected == True
	if detected:
		if fist_area != 0:
			if fist_area > init_fist_area + 500:
				print "greater"
				r = requests.get(url + '/forward')
			elif fist_area < init_fist_area - 500:
				print "less than"
				r = requests.get(url + '/backward')
			else:
				print "equal"
				r = requests.get(url + '/stop')

		# probably not do anything for this
		elif palm_area != 0:
			if palm_area > init_palm_area + 500:
				print "greater"
				r = requests.get(url + '/forward')
			elif palm_area < init_palm_area - 500:
				print "less than"
				r = requests.get(url + '/backward')
			elif:
				print "equal"
				r = requests.get(url + '/stop')
	else:
		print "nothing detected :("

	cv2.imshow('frame', frame)

	# kill script
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()