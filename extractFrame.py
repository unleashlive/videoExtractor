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
import pyexiv2

parser = argparse.ArgumentParser(description='Program transforms video into seperate images for use in visual SFM')

parser.add_argument('-file', action="store",
    help='file to transform', 
    dest="files", default=None)

parser.add_argument('-n', action="store",
    help='use only nth image',  
    dest="capture_step", default=1)

#camera focal number example f(1/8)
parser.add_argument('-fnumber', action="store",
    help='the focal number of the camera',  
    dest="fnumber", default=None)

#camera focal length example 43.0mm
parser.add_argument('-focal', action="store",
    help='the focal length of the camera',  
    dest="focal_length", default=None)

#aperture value of the lens 4.62EV (f/5.0) 
parser.add_argument('-a', action="store",
    help='apeture value of the lens',  
    dest="apeture_value", default=None)

#camera brand name
parser.add_argument('-cb', action="store",
    help='camera brand name', 
    dest="camera_brand", default=None)

#camera brand model
parser.add_argument('-cm', action="store",
    help='camera model',  
    dest="camera_model", default=None)


args = parser.parse_args()

capture_step = int(args.capture_step)
if capture_step < 1: capture_step = 1

tf = ''.join(args.files)
files = []
for f in tf.split(' '):
    files.append(f.split(','))

fnumber = args.fnumber
focal_length = args.focal_length
aperture_value = args.apeture_value
camera_model = args.camera_model
camera_brand = args.camera_brand

# N = F/D
# N = f number
# F = focal lenght
# D = diameter of lens

def check_apeture_value(val):
    # check if apeture value is ok
    # example input should be
    # 5.00EV (f/2.8)
    if re.search('%d/.%dEV /(f/%d/)',val):
        return True
    return False

def check_focal_value(val):
    # check if focal value is ok
    # example input should be
    # 49.00 mm
    if re.search('%d/.%d mm',val):
        return True
    return False

def check_focal(val):
    if(re.search("(m|M){2}",val)):
        return val
    else:
        return str(val+"mm")

files = [item for sublist in files for item in sublist]
print("Converting files:", files)

print("values:")
print("FNumber:", fnumber)
print("Focal Length:", focal_length)
print("Aperture Value:", aperture_value)
print("Camera Model:", camera_model)
print("Camera Brand:", camera_brand)

for f in files:
    capture = cv2.VideoCapture(f)

    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = capture.get(cv2.CAP_PROP_FPS)
    frame_count =  capture.get(cv2.CAP_PROP_FRAME_COUNT)
    codec = capture.get(cv2.CAP_PROP_FOURCC)

    print("Starting work on %s now" % f)

    if capture_step > frame_count: frame_count = frame_count - 1

    # aperture = Fraction(random.uniform(1.0, 16.0)).limit_denominator(2000)
    # calculate exposure
    num, den = aperture_value.split('/')  # convert 227/100 to fraction
    exposure = Fraction(1.0/int(num)).limit_denominator(4000)
    imgNum = 0
    for i in xrange(int(frame_count)):
        ret, frame = capture.read()
        if ret and (i % capture_step == 0):
            sys.stdout.write('saving frame:%s\r'%i)
            sys.stdout.flush()
            path = "./frames/UA_%04d.jpg"%(imgNum)
            imgNum += 1
            cv2.imwrite(path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

           
            exif = GExiv2.Metadata()
            exif.open_path(path)
            #exif = pyexiv2.ImageMetadata(path)
            #exif.read()

            t = os.path.getctime(path)
            ctime = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(t))
            #exif.set_gps_info(-41.3969702721, 122.6295057244, 76)

            exif.set_tag_string('Image.ImageDescription',"SEQ#%s"%i)
            exif.set_tag_string('Exif.Image.Make', camera_brand)
            exif.set_tag_string('Exif.Image.Model', camera_model)
            exif.set_tag_string('Exif.Image.DateTime', ctime)
            #exif['Exif.Image.Software'] = "https://github.com/eokeeffe/videoExtractor"
            #exif['Exif.Image.Orientation'] = str(0)

            exif.set_tag_string('Exif.Photo.UserComment', "Unleash live")
            #exif['Exif.Photo.Flash'] = str(flash[0])
            exif.set_tag_string('Exif.Photo.FNumber', str(fnumber))
            # exif.set_tag_string('Exif.Photo.FocalLength', str(focal_length))
            exif.set_tag_string('Exif.Photo.FocalLengthIn35mmFilm', str(focal_length))
            exif.set_tag_string('Exif.Photo.ApertureValue', str(aperture_value))
            exif.set_tag_string('Exif.Photo.ExposureTime', str(exposure))
            #exif['Exif.Photo.ExposureBiasValue'] = "0 EV"
            #exif['Exif.Photo.ISOSpeedRatings'] = "50"
            exif.save_file(path)
            #exif.write()
