# MultiObjectTracking with OpenCV

Project: Multiple Object Tracking Using OpenCV from JSON file <br />
Date created: May 3, 2022 <br />

## Description

Tracking multiple objects in a video using OpenCV with inputs from JSON file

### Installing dependencies

* pip install -r requirements.txt

## Executing program

### PYTHON
```
python multiObjectTracking.py --json development_assets/initial_conditions.json --video development_assets/input.mkv --tracker MEDIANFLOW
```

### DOCKER
```
sudo docker build -t docker-epicio -f Dockerfile .
```
```
sudo docker run -v $PWD/app:/app --name testepic10  docker-epicio:latest
```


## Authors

Jason Paul Cahuana Nina <br />
pcahuana.27@gmail.com

## Version History

* 0.1
    * Supported trackers: 'KCF', 'MEDIANFLOW', 'MOSSE', 'CSRT'


## Acknowledgments

Inspiration, code snippets, etc.
* [Amazing_Project](https://pysource.com/2021/01/28/object-tracking-with-opencv-and-python/)
* [Read_JSON](https://www.geeksforgeeks.org/read-json-file-using-python/)
* [Trackers](https://learnopencv.com/object-tracking-using-opencv-cpp-python/)
* [Project_Base](https://automaticaddison.com/how-to-do-multiple-object-tracking-using-opencv/)

