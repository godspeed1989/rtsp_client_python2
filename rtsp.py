#!/usr/bin/env python2

import time
import sys
import threading
import live555
import h264decode

# Shows how to use live555 module to pull frames from an RTSP/RTP
# source.  Run this (likely first customizing the URL below:

# Example: ./rtsp.py 192.168.0.199  8554  5
if len(sys.argv) < 4:
    print('')
    print('Usage: python2 example.py [cameraIP] [port] [nframe]')
    print('')
    sys.exit(1)

cameraIP = sys.argv[1]
port = sys.argv[2]
nframe = float(sys.argv[3])
frame_i = 0

# rtsp://192.168.0.88:8554
url = 'rtsp://%s:%s/' % (cameraIP, port)

# live555 only provides mechanism for streaming, meaning that it will take NAL packets
# from the network or file source and push it to the "DummySink", you still need to
# decode (transform the NAL units to bitmaps) and render (draw the bitmaps to the screen).

def decodeFrame(receiveBuf):
    #av_packet_from_data(m_packet, receiveBuf, len(receiveBuf))
    #avcodec_decode_video2(codecCtx, frame, &got_picture, m_packet)
    global decoder
    print ''
    if frame_i == 0:
        avcC = receiveBuf
        #TODO get avcC to decode
        decoder = h264decode.Decoder(avcC)
    else:
        yuv = decoder.decodeFrame(receiveBuf)
        print "Read frame of %dx%d pixels" % (yuv.width, yuv.height)
        # e.g. rendering with pygame:
        overlay.display((yuv.y, yuv.u, yuv.v))

fOut = open('out.264', 'wb')

def oneFrame(codecName, bytes, sec, usec, durUSec):
    global frame_i
    if len(bytes) > 0 and codecName == 'H264':
        print('frame %d for %s: %d bytes' % (frame_i, codecName, len(bytes)))
        # H264 start with 0x00 0x00 0x00 0x01
        receiveBuf = b'\0\0\0\1' + bytes

        fOut.write(receiveBuf)

        decodeFrame(receiveBuf)

        frame_i = frame_i + 1
        if frame_i == nframe:
            # Tell Live555's event loop to stop
            live555.stopEventLoop()

# Starts pulling frames from the URL, with the provided callback:
useTCP = False
live555.startRTSP(url, oneFrame, useTCP)

# Run Live555's event loop in a background thread:
t = threading.Thread(target=live555.runEventLoop, args=())
t.setDaemon(True)
t.start()

# Wait for the background thread to finish:
t.join()

