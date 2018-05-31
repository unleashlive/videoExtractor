#!/usr/bin/env python

#
#  make sure to run install.sh before trying this script
#  for exif data manipulation
#

import cv2
import gi
gi.require_version('GExiv2', '0.10')
from gi.repository import GExiv2
from fractions import Fraction
import argparse,re,time,os,sys
import random,math

parser = argparse.ArgumentParser(description='Program transforms video into seperate images for use in visual SFM')

parser.add_argument('-still', action="store",
    help='file to read exif from,must be of the same camera', 
    dest="still", default=None)

parser.add_argument('-file', action="store",
    help='file to transform', 
    dest="files", default=None)

parser.add_argument('-n', action="store",
    help='use only nth image',  
    dest="capture_step", default=1)

args = parser.parse_args()

capture_step = int(args.capture_step)
if capture_step < 1: capture_step = 1

tf = ''.join(args.files)
files = []
for f in tf.split(' '):
    files.append(f.split(','))

# N = F/D
# N = f number
# F = focal lenght
# D = diameter of lens

files = [item for sublist in files for item in sublist]
print("Converting files:",files)

exif1 = GExiv2.Metadata()
exif1.open_path(args.still)
print ("Using file:%s as exif data input"%args.still)
print ("values:")
print ("FNumber:",exif1.get_fnumber())
print ("Focal Length:",exif1.get_focal_length())
print ("Aperture Value:",exif1.get_tag_string('Exif.Photo.ApertureValue'))
print ("Camera Model:",exif1.get_tag_string('Exif.Image.Model'))
print ("Camera Brand:",exif1.get_tag_string('Exif.Image.Make'))
print ("Camera Exposure Time:",  exif1.get_exposure_time())
for f in files:
    capture = cv2.VideoCapture(f)

    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_count =  capture.get(cv2.CAP_PROP_FRAME_COUNT)
    codec = capture.get(cv2.CAP_PROP_FOURCC)

    print ("Starting work on %s now" % f)

    if capture_step > frame_count: frame_count = frame_count - 1

    ISOSPEEDS = [64, 100, 200, 250, 320, 400, 640, 800, 1000, 1600, 3200]

    SHUTTERSPEEDS = [15, 30, 60, 125, 250, 400, 
    500, 1000, 1250, 1600, 2000, 4000]
    
    FSTOPS = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.7, 
    1.8, 2, 2.2, 2.4, 2.6, 2.8, 3.2, 3.4, 3.7, 
    4, 4.4, 4.8, 5.2, 5.6, 6.2, 6.7, 7.3, 8, 8.7, 
    9.5, 10, 11, 12, 14, 15, 16, 17, 19, 21, 22]
    
    flash = [0x00,#No flash
    0x1, 
    0x18, 
    0x19, 
    0x49, 
    0x4d, 
    0x4f, 
    0x49, 
    0x4d, 
    0x4f]

    #aperture = Fraction(random.uniform(1.0, 16.0)).limit_denominator(2000)
    #exposure = Fraction(1.0/round(random.randint(8, int(100.0*aperture))+1, -2)).limit_denominator(4000)
    
    for i in xrange(int(frame_count)):
        ret, frame = capture.read()
        if ret and (i % capture_step == 0):
            sys.stdout.write('saving frame:%s\r'%i)
            sys.stdout.flush()
            path = "%s.jpg"%(i)
            cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            fnumber = exif1.get_exif_tag_rational('Exif.Photo.FNumber')
            focal = exif1.get_exif_tag_rational('Exif.Photo.FocalLength')
            aperture = exif1.get_exif_tag_rational('Exif.Photo.ApertureValue')
            exposure = exif1.get_exposure_time()
            exif = GExiv2.Metadata()
            exif.open_path(path)
            t = os.path.getctime(path)
            ctime = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(t))

            exif.set_tag_string('Exif.Image.ImageDescription',"SEQ#%s"%i)
            exif.set_tag_string('Exif.Image.Make', exif1.get_tag_string('Exif.Image.Make'))
            exif.set_tag_string('Exif.Image.Model',exif1.get_tag_string('Exif.Image.Model'))
            exif.set_tag_string('Exif.Image.DateTime', ctime)
            exif.set_tag_string('Exif.Photo.UserComment', "Unleash live")

            exif.set_exif_tag_rational('Exif.Photo.FNumber', fnumber[0],fnumber[1])
            exif.set_exif_tag_rational('Exif.Photo.FocalLength', focal[0], focal[1])
            exif.set_exif_tag_rational('Exif.Photo.ApertureValue',aperture[0],aperture[1])
            exif.set_exif_tag_rational('Exif.Photo.ExposureTime', exposure[0],exposure[1])
            exif.save_file(path)
