import imutils
import cv2
from pip._vendor.urllib3.connectionpool import xrange
import numpy as np
class PreprocessorWithAspect:
 def __init__(self, width, height, inter=cv2.INTER_AREA):
  # store the target image width, height, and interpolation
      # method used when resizing
      self.width = width
      self.height = height
      self.inter = inter
      pass

 def preprocess(self, image):
  # grab the dimensions of the image and then initialize
        # the deltas to use when cropping
  (h, w) = image.shape [:2]
  dW = 0
  dH = 0
  # if the width is smaller than the height, then resize
  # along the width (i.e., the smaller dimension) and then
  # update the deltas to crop the height to the desired dimension
  if w < h:
           image = imutils.resize(image, width=self.width, inter=self.inter)
           dH = int((image.shape[0] - self.height) / 2.0)
# otherwise, the height is smaller than the width so
   # resize along the height and then update the deltas
   # to crop along the width
  else:
           image = imutils.resize(image, height=self.height,inter=self.inter)
           dW = int((image.shape[1] - self.width) / 2.0)
# now that our images have been resized, we need to
   # re-grab the width and height, followed by performing the crop
  (h, w) = image.shape[:2]
  image = image[dH:h - dH, dW:w - dW]
# finally, resize the image to the provided spatial
        # dimensions to ensure our output image is always a fixed size
  return cv2.resize(image, (self.width, self.height),interpolation=self.inter)

 def render(self, img_rgb):
     #img_rgb = cv2.imread(img_rgb)
     ob2=PreprocessorWithAspect(800,1000)
     img_rgb = ob2.preprocess(img_rgb)
     numDownSamples = 1  # number of downscaling steps
     numBilateralFilters = 50  # number of bilateral filtering steps

     # -- STEP 1 --
     # downsample image using Gaussian pyramid
     img_color = img_rgb
     for _ in xrange(numDownSamples):
         img_color = cv2.pyrDown(img_color)
     # cv2.imshow("downcolor",img_color)
     # cv2.waitKey(0)
     # repeatedly apply small bilateral filter instead of applying
     # one large filter
     for _ in xrange(numBilateralFilters):
         img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
     # cv2.imshow("bilateral filter",img_color)
     # cv2.waitKey(0)
     # upsample image to original size
     for _ in xrange(numDownSamples):
         img_color = cv2.pyrUp(img_color)
     # cv2.imshow("upscaling",img_color)
     # cv2.waitKey(0)
     # -- STEPS 2 and 3 --
     # convert to grayscale and apply median blur
     img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
     img_blur = cv2.medianBlur(img_gray, 3)
     # cv2.imshow("grayscale+median blur",img_color)
     # cv2.waitKey(0)
     # -- STEP 4 --
     # detect and enhance edges
     img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 9)
     #img_edge=cv2.medianBlur(img_edge,3)

     # cv2.imshow("edge",img_edge)
     # cv2.waitKey(0)

     # -- STEP 5 --
     # convert back to color so that it can be bit-ANDed with color image
     (x, y, z) = img_color.shape
     ob1=PreprocessorWithAspect(y,x)
     img_edge = ob1.preprocess(img_edge)
     img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
     cv2.imwrite("edge.png", img_edge)
     # cv2.imshow("step 5", img_edge)
     # cv2.waitKey(0)
     # img_edge = cv2.resize(img_edge,(i for i in img_color.shape[:2]))
     # print img_edge.shape, img_color.shape
     return cv2.bitwise_and(img_color, img_edge)
ob=PreprocessorWithAspect(800,1000)
img=cv2.imread("img1.jpg");
img=ob.render(img)
cv2.imshow("P1",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
