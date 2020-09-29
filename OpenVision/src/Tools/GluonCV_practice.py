import sys
import pprint
pprint.pprint(sys.path)
from matplotlib import pyplot as plt
import cv2
import gluoncv
from gluoncv import model_zoo, data, utils
from gluoncv.data.transforms.pose import detector_to_simple_pose, heatmap_to_coord

detector = model_zoo.get_model('yolo3_mobilenet1.0_coco', pretrained=True)
pose_net = model_zoo.get_model('simple_pose_resnet18_v1b', pretrained=True)
detector.reset_class(["person"], reuse_weights=['person'])
im_fname = utils.download('https://github.com/dmlc/web-data/blob/master/' +
                          'gluoncv/pose/soccer.png?raw=true',
                          path='soccer.png')

x, img = data.transforms.presets.ssd.load_test(im_fname, short=512)
class_IDs, scores, bounding_boxs = detector(x)

pose_input, upscale_bbox = detector_to_simple_pose(img, class_IDs, scores, bounding_boxs)

predicted_heatmap = pose_net(pose_input)
pred_coords, confidence = heatmap_to_coord(predicted_heatmap, upscale_bbox)

plt.rcParams['figure.figsize'] = (15.0, 15.0)
ax = utils.viz.plot_keypoints(img, pred_coords, confidence,
                              class_IDs, bounding_boxs, scores,
                              box_thresh=0.5, keypoint_thresh=0.2)
plt.show()
