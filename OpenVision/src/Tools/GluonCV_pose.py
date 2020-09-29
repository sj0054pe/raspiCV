from __future__ import division
import argparse, time, logging, os, math, tqdm, cv2

import numpy as np
import mxnet as mx
from mxnet import gluon, nd, image
from mxnet.gluon.data.vision import transforms

import matplotlib.pyplot as plt

import gluoncv as gcv
from gluoncv import data
from gluoncv.data import mscoco
from gluoncv.model_zoo import get_model
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord
from gluoncv.utils.viz import cv_plot_image, cv_plot_keypoints

import cv2
#from google.colab.patches import cv2_imshow

PATH_INPUT="/Users/mayo/Desktop/raspiCV/OpenVision/Assets/Assets_Input/"
PATH_OUTPUT="/Users/mayo/Desktop/raspiCV/OpenVision/Assets/Assets_Output/"
FNAME_INPUT="videoplayback.mp4"

ctx = mx.cpu()
detector_name = "ssd_512_mobilenet1.0_coco"
detector = get_model(detector_name, pretrained=True, ctx=ctx)


detector.reset_class(classes=['person'], reuse_weights={'person':'person'})
detector.hybridize()

estimator = get_model('simple_pose_resnet18_v1b', pretrained='ccd24037', ctx=ctx)
estimator.hybridize()

import numpy as np
import cv2

def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

import os
import sys
import cv2

print(os.path.isfile(PATH_INPUT+FNAME_INPUT))
cap = cv2.VideoCapture(PATH_INPUT+FNAME_INPUT)
#time.sleep(1)  ### letting the camera autofocus
print(cap)

# encoder(for mp4)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# output file name, encoder, fps, size(fit to image size)
width= cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS);
video = cv2.VideoWriter('video2.mp4',fourcc, fps, (int(height), int(width)))

axes = None
num_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
print(num_frames)
for i in range(int(num_frames)):
    ret, frame = cap.read()
    frame = mx.nd.array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).astype('uint8')

    x, frame = gcv.data.transforms.presets.ssd.transform_test(frame, short=512, max_size=350)
    x = x.as_in_context(ctx)
    class_IDs, scores, bounding_boxs = detector(x)

    pose_input, upscale_bbox = detector_to_simple_pose(frame, class_IDs, scores, bounding_boxs,
                                                       output_shape=(128, 96), ctx=ctx)
    if len(upscale_bbox) > 0:
        predicted_heatmap = estimator(pose_input)
        pred_coords, confidence = heatmap_to_coord(predicted_heatmap, upscale_bbox)

        img = cv_plot_keypoints(frame, pred_coords, confidence, class_IDs, bounding_boxs, scores,
                                box_thresh=0.5, keypoint_thresh=0.2)


    if not video.isOpened():
      print("can't be opened")
      sys.exit()

    # can't read image, escape
    if img is None:
        print("can't read")
        break

    #print(img)
    cv2.imwrite("%s.jpeg" % i, img)
    #img=pil2cv(img)

    # add
    video.write(img)
    print("%s/%s" % (i, num_frames))
    #print('written')
    #cv2_imshow(img)
cv2.imshow("Demo", video)
video.release()

#cv2.waitKey(1)


#cap.release()

#python cam_demo.py --num-frames 100
