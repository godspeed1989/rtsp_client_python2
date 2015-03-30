#!/usr/bin/env python2

import sys
import time
import vlc

# Example: ./rtsp_vlc.py 192.168.0.199  8554
if len(sys.argv) < 3:
    print('')
    print('Usage: python2 example.py [cameraIP] [port]')
    print('')
    sys.exit(1)

cameraIP = sys.argv[1]
port = sys.argv[2]

# rtsp://192.168.0.88:8554
url = 'rtsp://%s:%s/' % (cameraIP, port)

player = vlc.MediaPlayer(url)
player.play()

frame_i = 0
while 1:
    #time.sleep(1)
    #print "%d X %d" % (player.video_get_width(), player.video_get_height())
    char = raw_input("\n{p(ause)|c(ontinue)|r(elease)|s(nap)}>>> ")
    if char == "p":
        player.pause()
    elif char == "c":
        player.play()
    elif char == "r":
        player.release()
        break
    elif char == "s":
        frame_i = frame_i + 1
        player.video_take_snapshot(0, ('%d.png' % frame_i), 0, 0)
    else:
        print ''

