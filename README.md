videoExtractor
==============

simple script and library for extracting images from video file and adding exif data to the extracted images

There are two ways of doing this, either input the individual values as command line arguements or pass an image from the camera that has exif data that will be mirrored in the extracted video images

extractFrame.py is the manual script that requires a video file and cmd args to work

extractFrameAuto.py is the automated script, needs a video file and image to work

extractFrameAuto_Calibrate.py is the automated script that will undistort image as well
as add EXIF information from video images

python extractFrame.py -h will display the arguments you need for input

Tested and Verified on Ubuntu 14.04 LTS


# Build docker image

```bash
docker build -t ua-videoextractor .

```

# Running image

example with mavic pro details
```bash
SOURCE_PATH=`readlink -f data`
docker run -it --mount type=bind,src=${SOURCE_PATH},dst=/data ua-videoextractor -a 227/100 -focal 4.73 -fnumber 2.2 -cb DJI -cm FC220 -file /data/DJI_0817.MP4

```