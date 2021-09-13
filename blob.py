import cv2
import numpy as np
import time
from pythonosc.udp_client import SimpleUDPClient

ip = "192.168.1.10"
port = 8000

client = SimpleUDPClient(ip, port)  # Create client

# define a video capture object
vid = cv2.VideoCapture(0)
'''
#change size
vid.set(3, 80)
vid.set(4, 60)
'''

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()
 
# Change thresholds
params.minThreshold = 127
params.maxThreshold = 255
 
# Filter by Area.
params.filterByArea = True
params.minArea = 100
params.maxArea = 100000
 
# Filter by Circularity
params.filterByCircularity = False
params.minCircularity = 0.1
 
# Filter by Convexity
params.filterByConvexity = False
params.minConvexity = 0.87
 
# Filter by Inertia
params.filterByInertia = False
params.minInertiaRatio = 0.01

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)


background_set = False
while(True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    #convert 'frame' to gray
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  

    #Set "Background" on 'b' 
    if cv2.waitKey(25) & 0xFF == ord('b'):
      background = im
      background_set = True
      #cv2.imshow("background", background )
      continue
                                                                                                        #print("finished")
                                                                                                        #cv2.imshow("Keypoints", im ) # frame
                                                                                                        #print("after imshow")
    #remove background (if it exists!)
    if background_set:
        im = cv2.absdiff(im,background)


    #ret,im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)

    ret,im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)

    '''Gaussian adaptive thresholding
    im = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    '''



    # Detect blobs.
    keypoints = detector.detect(im)
    client.send_message("#grains", len(keypoints))   # Send float message
    ''' filter info
    client.send_message("/RF/xy", ) #gain/ frequency
    client.send_message("/RF/fader8", ) #que
    client.send_message("/RF/multitoggle2/3/1", ) #lowpass
    client.send_message("/RF/multitoggle2/3/2", ) #highpass
    client.send_message("/RF/multitoggle2/3/3", ) #bandpass
    client.send_message("/RF/multitoggle2/2/1", ) #bandstop
    client.send_message("/RF/multitoggle2/2/2", ) #peaknotch
    client.send_message("/RF/multitoggle2/2/3", ) #low shelf
    client.send_message("/RF/multitoggle2/1/1", ) # high sheld
    client.send_message("/RF/multitoggle2/1/2", ) # resonant
    client.send_message("/RF/multitoggle2/1/3", ) # allpass
    '''

    '''reverb info"
    client.send_message("/RF/rotary6", ) #time
    client.send_message("/RF/rotary11", ) #width
    client.send_message("/RF/rotary12", ) #space
    client.send_message("/RF/wet", ) #wet
    client.send_message("/RF/dry", ) #dry
    '''

    ''' dist info
    client.send_message("dist", ) #level
    '''

    pts = cv2.KeyPoint_convert(keypoints)
    print(np.mean(pts, axis = 0))

    '''
    for x in keypoints: # possible reworking of synth
        print(x.pt, x.size)
        client.send_message(loc, x.pt)
        client.send_message(size, x.size)
    '''



    '''Draw detected blobs as red circles.
    cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the 
    size of the circle corresponds to the size of blob'''
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    cv2.imshow("Keypoints", im_with_keypoints)

    #cv2.waitKey(0) //stepwise

    #wait 25(+25) ms between frames, close on 'q'
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
