# Pi Mask Detection

This code runs a face detection models as well as a binary classifier mask/no mask on camera
footage from a raspberry Pi to detect whether a person is wearing or not their mask.

For each _event_ - _i.e._, someone not wearing their mask - we store an event in a local SQLite database.


# Installation instruction on the Pi
### Prerequisite: 
_Hardware_
 - A [Raspberry Pi 4](https://amzn.to/3iB5VYB) model B with 4Go of RAM and at least 2Go storage available on the SD card (untested on 2Go RAM models but should work) - **required**.
 - A Camera compatible wth the Pi **required**.
 - [A Coral USB accelerator](https://amzn.to/2F8wgzA) to speed up model inference on your Pi - _nice to have but not mandatory._
 - A fan and heat dissipating components are **highly recommended** to avoid overheating (my ventilated Pi in its protective case never goes above 38°C while running the inference code and the [alertDispatcher](https://github.com/fpaupier/alertDispatcher)). 
 
 _Software_
 - You have setup your Pi with an operating system (I used [NOOBS](https://www.raspberrypi.org/downloads/noobs/)).
 - Your Pi has python 3.7 installed. Run ``` `which python3` -V``` to see which version of python3 you have.
    ```shell script
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.7
    ```
  - Install SQLite 3 on your Pi.
    ````shell script
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install sqlite3
    ````
Then you can create the database using the command ``sqlite alert.db``. Create the alert table using the SQL commands from the `schema.sql` file of this project. 


## Install steps 

1. Create a virtual env in this project folder, let's call it `venv` and activate it:
````shell script
python3 -m venv venv
source venv/bin/activate
````

2. Install dependencies, if on your development machine, use `dev-requirements.txt` instead of `requirements.txt` since `requirements.txt` requires the pi camera module.
```shell script
pip install -r requirements.txt
```


3. For TensorFlow Lite _(TF Lite)_ runtime on your Pi, check out [Tensorflow Quickstart](https://www.tensorflow.org/lite/guide/python) for the latest instructions.
Running the following command worked for me to install the TF Lite runtime.  
```shell script
pip install https://dl.google.com/coral/python/tflite_runtime-2.1.0.post1-cp37-cp37m-linux_armv7l.whl
```

4. Install lib for Coral USB accelerator following the [getting started doc of Coral](https://coral.ai/docs/accelerator/get-started)

## Running unit tests

Use pytest, cd to the test folder and run pytest:
```shell script
cd tests && pytest serialization.py
``` 

## Running the project
Running the `detect_mask.py` script will start capture the video feed from the Pi camera and capture alerts.

```shell script
python detect_mask.py
``` 


# Machine learning models used
I provide you with two pretrained models, a widely available face detection model (`ssd_mobilenet_v2`) and a binary classifier _mask/no mask_ I trained. (See under the `models/` folder. They are optimized to run on the Coral USB edge TPU accelerator.
  
You can retrain you own classification model using your coral device, see [Coral - retrain classification](https://coral.ai/docs/edgetpu/retrain-classification/#requirements)

