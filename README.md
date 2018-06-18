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

push to ECR
```bash
eval $(aws ecr get-login --no-include-email --region ap-southeast-2 | sed 's|https://||')
docker tag ua-videoextractor:latest 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/video-modelling:ua-videoextractor
docker push 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/video-modelling:ua-videoextractor

```

# Pulling image from Unleash Hub

Ensure AWS secrets are configured on host

```bash
eval $(aws ecr get-login --no-include-email --region ap-southeast-2 | sed 's|https://||')
docker pull 712356514005.dkr.ecr.ap-southeast-2.amazonaws.com/video-modelling:ua-videoextractor
```

# Running image

Input data folder: /data
Output data folder: /data/out
```bash
SOURCE_PATH=`readlink -f data`
docker run -it --mount type=bind,src=${SOURCE_PATH},dst=/data  ua-videoextractor -a 227/100 -focal 4.73 -fnumber 2.2 -cb DJI -cm FC220 -file /data/DJI_0817.MP4 -n 30

```

interactive mode

```bash
docker run -it --mount type=bind,src=${SOURCE_PATH},dst=/data --entrypoint "/bin/bash" ua-videoextractor
```