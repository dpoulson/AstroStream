# AstroStream
This is a script to control a dedicated astronomy camera (currently only ASI ZWO Mono cameras) and send the output to a youtube or twitch live stream.

## Pre-requisites

Only tested on debian style systems currently.

Install packages:

sudo apt-get install python3-opencv python3-numpy python3-tk python3-pip libasicamera

You will also need the zwoasi python module:

python3 -m pip install zwoasi

## Setup

Create a config:

cp main.cfg-default ~/.config/astrostream/main.cfg

And edit it to set the required keys.

## Usage

Run the main.py code

Controls are fairly straight forward. You can adjust the exposure and gain. Play will display the camera output with overlay, and stream will start sending to youtube.
