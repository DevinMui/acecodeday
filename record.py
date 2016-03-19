import cv2
from pymouse import PyMouse
from pykeyboard import PyKeyboard

cap = cv2.VideoCapture(0)

fist_cascade = cv2.CascadeClassifier('fist.xml')
palm_cascade = cv2.CascadeClassifier('palm.xml')

init_palm_area = 0

init_fist_area = 0

while True:
	ret, frame = cap.read()

	fist_area = 0
	palm_area = 0

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	fists = fist_cascade.detectMultiScale(gray, 1.3, 5)
	palms = palm_cascade.detectMultiScale(gray, 1.3, 5)

	for x,y,w,h in palms:
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
	if fist_area != 0:
		if fist_area > init_fist_area:
			print "greater"
		elif fist_area < init_fist_area:
			print "less than"
		elif fist_area == init_fist_area:
			print "equal"

	elif palm_area != 0:
		if palm_area > init_palm_area:
			print "greater"
		elif palm_area < init_palm_area:
			print "less than"
		elif palm_area == init_palm_area:
			print "equal"

	cv2.imshow('frame', frame)

	if cv2.waitKey(20) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()