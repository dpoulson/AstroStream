#!/usr/bin/env python3

import sys
import zwoasi as asi
import cv2
import time
import tkinter as tk
import logging
import numpy as np
from time import strftime
from stream import Stream
from config import AstroConfig

__author__ = 'Darren Poulson'
__version__ = '0.0.1'
__license__ = 'GPLv3'

config = AstroConfig()

title = "Astro Stream"

YOUTUBE_URL = "rtmp://x.rtmp.youtube.com/live2/{}".format(
    config.settings['youtube_key'])
TWITCH_URL = "rtmp://live.twitch.tv/app/{}".format(
    config.settings['twitch_key'])

filename = 'image_video_mono.mp4'

prev_frame_time = 0
new_frame_time = 0
watermark = cv2.imread('watermark.png')
(wH, wW) = watermark.shape[:2]
state_playing = False
state_streaming = False

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def save_control_values(filename, settings):
    filename += '.txt'
    with open(filename, 'w') as f:
        for k in sorted(settings.keys()):
            f.write('%s: %s\n' % (k, str(settings[k])))
    print('Camera settings saved to %s' % filename)


def update_exposure(val):
    print('Updating exposure to %s' % val)
    camera.set_control_value(asi.ASI_EXPOSURE, int(val))


def update_gain(val):
    print('Updating gain to %s' % val)
    camera.set_control_value(asi.ASI_GAIN, int(val))


def toggle_stream():
    global stream, state_streaming
    print('Toggling Stream')
    if toggle_stream.config('relief')[-1] == 'sunken':
        toggle_stream.config(relief="raised")
        stream.finish()
        state_streaming = False
    else:
        toggle_stream.config(relief="sunken")
        state_streaming = True
        stream = Stream(YOUTUBE_URL, width, height)


def toggle_play():
    global stream, state_playing
    print('Toggling Play')
    if toggle_play.config('relief')[-1] == 'sunken':
        toggle_play.config(relief="raised")
        state_playing = False
    else:
        toggle_play.config(relief="sunken")
        state_playing = True


def do_overlay(frame):
    # Overlays
    global prev_frame_time, new_frame_time
    # Calculate framerate to display
    new_frame_time = time.time()
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = "{:.2f}".format(fps)
    heading = title + ": " + cameras_found[0] + " FPS: " + fps
    exposure = "Exposure: " + str(sli_exposure.get())
    gain = "Gain: " + str(sli_gain.get())
    cv2.rectangle(frame, (0, 0), (1600, 200), (0, 0, 0),
                  cv2.FILLED, cv2.FILLED, 1)
    cv2.putText(frame, heading, (20, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, exposure, (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, gain, (20, 70), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, strftime("%c"), (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1,
                cv2.LINE_AA)
    return frame


config = AstroConfig()
asi.init(config.settings['libpath'])

window = tk.Tk()
window.title(title)
greeting = tk.Label(text=title)
greeting.pack()
sli_exposure = tk.Scale(window, from_=100, to=20000, orient=tk.HORIZONTAL,
                        resolution=100,
                        command=update_exposure, length=400)
sli_exposure.set(5000)
sli_exposure.pack()
sli_gain = tk.Scale(window, from_=0, to=600, orient=tk.HORIZONTAL,
                    resolution=10,
                    command=update_gain, length=400)
sli_gain.set(150)
sli_gain.pack()
toggle_play = tk.Button(text="Play", width=12, relief="raised",
                        command=toggle_play)
toggle_play.pack()
toggle_stream = tk.Button(text="Stream", width=12, relief="raised",
                          command=toggle_stream)
toggle_stream.pack()


num_cameras = asi.get_num_cameras()
if num_cameras == 0:
    print('No cameras found')
    sys.exit(0)

cameras_found = asi.list_cameras()  # Models names of the connected cameras

if num_cameras == 1:
    camera_id = 0
    print('Found one camera: %s' % cameras_found[0])
else:
    print('Found %d cameras' % num_cameras)
    for n in range(num_cameras):
        print('    %d: %s' % (n, cameras_found[n]))
    # TO DO: allow user to select a camera
    camera_id = 0
    print('Using #%d: %s' % (camera_id, cameras_found[camera_id]))

camera = asi.Camera(camera_id)
camera_info = camera.get_camera_property()
controls = camera.get_controls()
camera.stop_video_capture()
camera.stop_exposure()

camera.set_image_type(asi.ASI_IMG_RAW16)
img = camera.capture()
width = int(img.shape[1])
height = int(img.shape[0])


# Use minimum USB bandwidth permitted
camera.set_control_value(asi.ASI_BANDWIDTHOVERLOAD,
                         camera.get_controls()['BandWidth']['MinValue'])


# Set some sensible defaults. They will need adjusting depending upon
# the sensitivity, lens and lighting conditions used.
camera.disable_dark_subtract()

camera.set_control_value(asi.ASI_GAIN, 150)
camera.set_control_value(asi.ASI_EXPOSURE, 10000)
camera.set_control_value(asi.ASI_WB_B, 99)
camera.set_control_value(asi.ASI_WB_R, 75)
camera.set_control_value(asi.ASI_GAMMA, 50)
camera.set_control_value(asi.ASI_BRIGHTNESS, 50)
camera.set_control_value(asi.ASI_FLIP, 0)


print('Enabling video mode')
camera.start_video_capture()


# Set the timeout, units are ms
timeout = (camera.get_control_value(asi.ASI_EXPOSURE)[0] / 1000) * 2 + 500
camera.default_timeout = timeout

if camera_info['IsColorCam']:
    print('Capturing a single color frame')
    filename = 'image_video_color.jpg'
    camera.set_image_type(asi.ASI_IMG_RGB24)
    camera.capture_video_frame(filename=filename)
else:
    print('Capturing a single 8-bit mono frame')
    filename = 'image_video_mono.mp4'
    camera.set_image_type(asi.ASI_IMG_RAW8)
    time.sleep(1)
    while True:
        window.update()
        if state_playing:
            frame = camera.capture_video_frame()
            if frame is None:
                continue
            frame = do_overlay(frame)
            cv2.imshow("Frame", frame)
            if state_streaming:
                stream.stream_pipe.write(frame.astype(np.uint8).tobytes())
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

# close output window

cv2.destroyAllWindows()
if state_streaming == 'streaming':
    stream.finish()

print('Saved to %s' % filename)
save_control_values(filename, camera.get_control_values())
