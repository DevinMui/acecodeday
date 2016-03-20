# CamRoll

### Description

CamRoll is a few scripts that allow users to take control of the Sphero by controlling it with your hands and using computer vision.

### Dependencies

You will need:

* OpenCV
* Python OpenCV
* Python 2
* node.js
* npm
* Linux skills

### Downloading

1. Git it! `git clone https://www.github.com/devinmui/acecoding.git`
2. `cd acecoding/`
3. `cp *.xml /path/to/opencv/haarcascades/`
4. Install node dependencies: `npm install`
5. Run node express server: `node sphero-control.js` (may take multiple tries)
6. Run python opencv code: `python record.py`

### Arrow key control

Instead of executing steps 5 - 6, execute `node arrow_control.js`