This GIT commit of the persons tracker using OpenCV (no CNN / TPU inference needed here !) is based on the following GIT :
https://github.com/Practical-CV/Simple-object-tracking-with-OpenCV

Basically the idea is to extend this code with measuring the size eg width of the detected person boudning box, in order to know if the detected person is approaching Reachy Camera.

To run the script simply run the following python script :
python object_tracker.py --prototxt deploy.prototxt --model res10_300x300_ssd_iter_140000.caffemodel
