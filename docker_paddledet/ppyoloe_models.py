import cv2
import fastdeploy.vision as vision

model = vision.detection.PPYOLOE("weights/model.pdmodel",
                                 "weights/model.pdiparams",
                                 "weights/infer_cfg.yml")
im = cv2.imread("data/images/104333_00.jpg")
result = model.predict(im)

vis_im = vision.vis_detection(im,result, labels=["liewen"], score_threshold=0.7)
cv2.imwrite("data/images/vis_image.jpg", vis_im)
print("the predicted images has been saved in data/images/vis_image.jpg")

