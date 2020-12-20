This commit relies on KittAI's snowboy: https://github.com/Kitt-AI/snowboy.git, and extends it for our Reachy project.

Before cloning the repo, make sure you have the appropriate packages installed and build snowboy in your own environment.
	sudo apt install python-pyaudio python-numpy python-virtualenv
	sudo apt-get install swig python-dev libatlas-base-dev build-essential make	

Rest of the instructions on how I set it up can be found on this Notion page: https://www.notion.so/Wake-Word-Triggers-Hot-Terms-e825cc2f92944104be9621ecacb63807

This assumes you're adding it onto a pi setup -- otherwise follow instructions on snowboy github for your own environment.

We extended snowboy by adding our own custom universal model, using 'Reachy' as the trigger/hot word.  Instead of a 'ding' sound on callback, Reachy responds randomly when the hotword is detected.

The setup at the lab relies on espeak (already installed).  The code in the directory will just print the greeting into the terminal, and doesn't assume you have the same setup as our lab's. 

This is a copy of the code already on the raspberry pi4 in our setup.  Please only copy this directory if you need it in your *own* setup.

For the setup in our physical lab, you can try the code by following these instructions in terminal.

1. cd ~/speaker/usb_4_mic_array/wakeup_word/snowboy/examples/Python3
2. python3 demoReachy.py ./resources/models/reachy.umdl
