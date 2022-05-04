# Project: Multiple Object Tracking Using OpenCV from JSON file
# Author: Jason Paul Cahuana Nina
# Date created: May 3, 2022
# Description: Tracking multiple objects in a video using OpenCV with inputs from JSON file
 
import cv2 # Computer vision library for show visualization our results
import json # To read json files
from random import randint # Handles the creation of random integers for colors
import time #To get our metrics
import argparse #To define and get arguments


# Define and parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('--json', type=str, default=None,
					help='String_path=For JSON file')
parser.add_argument('--video', type=str, default=None,
					help='String_path=For Video file')
parser.add_argument('--tracker', type=str, default=None,
					help='Kind of tracker for our project. Available trackers: KCF, MEDIANFLOW,MOSSE, CSRT')
args = parser.parse_args()


# Opening JSON file
#jsonRead = open('development_assets/initial_conditions.json')
jsonRead = open(args.json)

# create class for object Tracking
class objectTracking:
    def __init__(self,kind,id,coordinates):
        self.kind=kind
        self.id=id
        self.coordinates=coordinates

#open json file
data = json.load(jsonRead)
# Iterating through the json and save our information
listObjectsTrackings=[]
color_list=[]
for i in data:
    coor=i['coordinates']
    coor= tuple(coor)
    tempObjects= objectTracking(i['object'],i['id'],coor)#print(i))
    listObjectsTrackings.append(tempObjects)

    blue = randint(127, 255)
    green = randint(127, 255)
    red = randint(127, 255)
    color_list.append((blue, green, red))
# Closing file
jsonRead.close()

#open our video input
#filename = "development_assets/input.mkv" 
filename = args.video
file_size = (1920,1080)
 
# We want to save the output to a video file
output_filename = 'output_object_tracking.mp4'
output_frames_per_second = 20.0

# Choose object tracking algorithms 
type_of_trackers = ['KCF', 'MEDIANFLOW', 'MOSSE', 'CSRT']
# Order result:
# 4. MEDIANFLOW=> time: 00:00:08.74 // isn't accurate but fast
# 3. MOSSE=> time: 00:00:04.51  // isn't accurate but fast
# 2. KCF=> time: 00:00:13.19  // is a little accurate but fast
# 1. CSRT=> time: 00:00:27.30  // is accurate but slow.            

#desired_tracker = 'MEDIANFLOW'
desired_tracker = args.tracker
 
# Generate a MultiTracker object    
multi_tracker = cv2.MultiTracker_create()
                                          
def generate_tracker(type_of_tracker):
  """
  Create object tracker.
  :param type_of_tracker string: OpenCV tracking algorithm 
  """
  if type_of_tracker == type_of_trackers[0]:
    tracker = cv2.TrackerKCF_create()
  elif type_of_tracker == type_of_trackers[1]:
    tracker = cv2.TrackerMedianFlow_create()
  elif type_of_tracker == type_of_trackers[2]:
    tracker = cv2.TrackerMOSSE_create()
  elif type_of_tracker == type_of_trackers[3]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('The name of the tracker is incorrect')
    print('Here are the possible trackers:')
    for track_type in type_of_trackers:
      print(track_type)
  return tracker

def main():
 
  # Load our video
  cap = cv2.VideoCapture(filename)
 
  # Create a VideoWriter object so we can save the video output
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  result = cv2.VideoWriter(output_filename,  
                           fourcc, 
                           output_frames_per_second, 
                           file_size) 
 
  # Capture the first video frame
  success, frame = cap.read() 
 
  # Do we have a video frame? If true, proceed.
  if success:
    start = time.time() #We take our begin time for metrics
    print("Tracking objects. Please wait...")     
    # Set the tracker
    type_of_tracker = desired_tracker   
    print("type_of_tracker: ",type_of_tracker)
    #add our  kind of tracker, frame and coordinates
    for bbox in listObjectsTrackings:
        multi_tracker.add(generate_tracker(type_of_tracker), frame, bbox.coordinates)
       
    # Process the video
    while cap.isOpened():
        success, frame = cap.read() 
        # Do we have a video frame? If true, proceed.
        if success:
    
            # Update the location of the bounding boxes
            success, bboxes = multi_tracker.update(frame)
    
            # Draw the bounding boxes on the video frame
            for i, bbox in enumerate(bboxes):
              
              point_1 = (int(bbox[0]), int(bbox[1]))
              point_2 = (int(bbox[0] + bbox[2]), 
              int(bbox[1] + bbox[3]))
              cv2.rectangle(frame, point_1, point_2, color_list[i], 5)
              cv2.putText(frame, str(listObjectsTrackings[i].id),point_1,cv2.FONT_HERSHEY_SIMPLEX,1,color_list[i], 2)
              
            # Write the frame to the output video file
            result.write(frame)
        # No more video frames left
        else:
            break
         
  # Stop when the video is finished
  cap.release()

  # Release the video recording
  result.release()
  end = time.time() #paramos el tiempo
  hours, rem = divmod(end-start, 3600)
  minutes, seconds = divmod(rem, 60)
  print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
 
main()