# Build an image that can
# - extract images with videos
# - enrich images exif data with camera focal and aperture\

# IMAGE: ubuntu based python 2.7, opencv 3.2


FROM valian/docker-python-opencv-ffmpeg:py2

MAINTAINER UnleashLive <getstarted@unleashlive.com>


RUN apt-get -y update && apt-get install -y \
        build-essential \
        cmake \
        git \
        unzip \
        gir1.2-gexiv2-0.10 \
        python-gi \
        python-pyexiv2

# Cleanup APT
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /video-extractor
RUN mkdir /video-extractor/frames
WORKDIR /video-extractor

COPY extractFrame.py /video-extractor
COPY extractFrameAuto.py /video-extractor
COPY extractFrameAuto_Calibrate.py /video-extractor

# Entry point
ENTRYPOINT ["python", "/video-extractor/extractFrame.py"]
#ENTRYPOINT ["python", "/video-extractor/extractFrameAuto.py"]
#ENTRYPOINT ["python", "/video-extractor/extractFrameAuto_Calibrate.py"]