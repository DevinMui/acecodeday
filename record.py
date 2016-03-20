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

detected = False

while True:
	# mouse positiions
	last_x = 0
	last_y = 0
	number_of_fists = 0
	detected = False
	ret, frame = cap.read()

	fist_area = 0
	palm_area = 0
	height, width = frame.shape[:2]
	half_width = width / 2
	# change to grayscale
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detection
	fists = fist_cascade.detectMultiScale(gray, 1.3, 5)
	palms = palm_cascade.detectMultiScale(gray, 1.3, 5)

	# detect palms and fists
	for x,y,w,h in palms: # typically, < 5000 is a false positive
		if w * h < 2500:
			print "probably a false positive"
		else:
			last_x = x
			cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
			if init_palm_area == 0: # set the init area for comparisons later
				init_palm_area = w * h
			else:
				print "PALM AREA: " + str(w*h)
				palm_area = w * h
				detected = True
			print "PALM"

	for x,y,w,h in fists:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
		number_of_fists = number_of_fists + 1
		if init_fist_area == 0: # set the init area for comparisons later
			init_fist_area = w * h
		else:
			print "FIST AREA: " + str(w*h)
			fist_area = w * h
			detected = True

		print "FIST"

	# for these actions, we will need a specific zone
	# or range for the equal so that it is not hard to stop moving

	# these actions will move the mouse position depending if detected == True
	if detected:

		if fist_area != 0:

			if last_x > half_width + 300: # right but probably reversed
					r = requests.get(url + '/left')
				elif last_x < half_width - 300: # left but probably reversed
					r = requests.get(url + '/right')
				else:
					r = requests.get(url + '/stop')
					if fist_area > init_fist_area + 2500:
						print "greater"
						r = requests.get(url + '/forward')
					elif fist_area < init_fist_area - 2500:
						print "less than"
						r = requests.get(url + '/backward')
					else:
						print "equal"


		# probably not do anything for this
		elif palm_area != 0:
			if last_x > half_width: # right but probably reversed
				r = requests.get(url + '/left')
			elif last_x < half_width: # left but probably reversed
				r = requests.get(url + '/right')
			else:
				r = requests.get(url + '/stop')
			print "something"
	else:
		r = requests.get(url + '/stop')
		print "nothing detected :("

	cv2.imshow('frame', frame)

	# kill script
	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()