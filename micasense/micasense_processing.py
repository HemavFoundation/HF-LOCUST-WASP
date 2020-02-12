import cv2
import numpy as np
import os, os.path
import pandas as pd
import json
import time


##############################################################
### FUNCTIONS TO LOAD IMAGES
##############################################################


def load_image(directory):

    imgs = []
    path = directory

    valid_images = [".tif", ".tiff"]

    for f in sorted(os.listdir(path)):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        img = cv2.imread(os.path.join(path, f), 0)
        imgs.append(img)

    print(len(imgs))

    return imgs


def get_nir(imgs):

    nir = []
    num = 4

    while num < len(imgs):
        nir.append(imgs[num])
        num += 5
    print('@@@@length nir:', len(nir))
    return nir


def get_red(imgs):

    red = []
    num = 2

    while num < len(imgs):
        red.append(imgs[num])
        num += 5

    print('@@@@length red:', len(red))
    return red


##############################################################
### FUNCTIONS TO GET A GOOD OUTPUT IMAGES
##############################################################

def edit_json(newFlight):

    with open("get_results.json", "r+") as f:
        data = []
        try:
            data = json.load(f)
        except:
            print("Empty json")
        data.append(newFlight)
        f.seek(0)
        json.dump(data, f)
        f.truncate()
        f.close()


def write_json(timestamp, num, percentage, coordinates):
    results = []
    results.append(
        {
                "image_id": num,
                "percentage": percentage,
                "coordinates": coordinates,
            }
    )

    flight = {
        "id": timestamp,
        "results": results
    }

    return flight


def create_directory(path):  # tested and working

     # this returns actual directory as a string (should be modify to a raspberry directory)

    # we need to convert numbers to string to be able to create the new path
    year = str(pd.datetime.now().year)
    month = str(pd.datetime.now().month)
    day = str(pd.datetime.now().day)
    hour = str(pd.datetime.now().hour)
    minute = str(pd.datetime.now().minute)

    newpath = path + "/" + year + "_" + month + "_" + day + "-" + hour + "_" + minute  # we create the string for the new directory

    try:
        os.mkdir(newpath)        # creates a directory
    except:
        time.sleep(30)

    return newpath


##############################################################
### FUNCTIONS TO EXTRACTS FEATURES FOR MERGING
##############################################################

# 1. Extract ORB keypoints and descriptors from a gray image


def extract_features(gray):

    orb = cv2.ORB_create()
    kp, desc = orb.detectAndCompute(gray, None)

    return kp, desc


# 2. Find corresponding features between the images

def find_matches(kp1, desc1, kp2, desc2):

    # create BFMatcher object (for ORB features)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # Match descriptors
    matchess = bf.match(desc1, desc2)

    # Sort them in the order of their distance.
    matches = sorted(matchess, key=lambda x: x.distance)

    # convert first 10 matches from KeyPoint objects to NumPy arrays
    points1 = np.float32([kp1[m.queryIdx].pt for m in matches[0:50]])
    points2 = np.float32([kp2[m.trainIdx].pt for m in matches[0:50]])

    return points1, points2


# 3. Find homography between the points

def find_homography(points1, points2):

    # convert the keypoints from KeyPoint objects to NumPy arrays
    src_pts = points2.reshape(-1, 1, 2)
    dst_pts = points1.reshape(-1, 1, 2)

    # find homography
    homography, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    return homography


# 4.1 Calculate the size and offset of the stitched panorama

def calculate_size(img1, img2, homography):

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]

    corners2 = np.float32([[[0, 0], [0, h2 - 1], [w2 - 1, h2 - 1], [w2 - 1, 0]]])

    # remap the coordinates of the projected image onto the panorama image space
    transformedCorners2 = cv2.perspectiveTransform(corners2, homography)
    #print(transformedCorners2)

    #offset = (transformedCorners2[0][0][0], transformedCorners2[0][0][1])

    offset = (0, np.abs(transformedCorners2[0][3,1]))

    size = (np.ceil(transformedCorners2[0][3,0]), np.ceil(transformedCorners2[0][2,1]-transformedCorners2[0][3,1]))

    homography[0:2, 2] += offset
    #print(offset)
    #print(size)

    return size, offset


# 4.2 Combine images into a panorama
def merge_images(image1, image2, homography, size, offset):

    size = (image1.shape[1], image1.shape[0])

    dst = cv2.warpPerspective(image2, homography, size)

    #dst[int(offset[1]): (image1.shape[0] + int(offset[1])), 0:image1.shape[1]] = image1

    # left = 0
    # top = 0
    # bottom = image1.shape[0]
    # right = image1.shape[1]

    #panorama = dst.crop((left, top, right, bottom))
    panorama = dst
    return panorama

def contrast_stretch(im):
    """
    Performs a simple contrast stretch of the given image, from 5-95%.
    """
    in_min = np.percentile(im, 5)
    in_max = np.percentile(im, 95)

    out_min = 0.0
    out_max = 255.0

    out = im - in_min
    out *= ((out_min - out_max) / (in_min - in_max))
    out += in_min

    return out

### --- No need to change anything below this point ---

### Connects corresponding features in the two images using yellow lines
def draw_matches(image1, image2, points1, points2):

  # Put images side-by-side into 'image'
    (h1, w1) = image1.shape[:2]
    (h2, w2) = image2.shape[:2]
    image = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    image[:h1, :w1] = image1
    image[:h2, w1:w1 + w2] = image2

  # Draw yellow lines connecting corresponding features.
    for (x1, y1), (x2, y2) in zip(np.int32(points1), np.int32(points2)):
        cv2.line(image, (x1, y1), (x2 + w1, y2), (0, 255, 255))

    return image


##############################################################
### MAIN PROGRAM
##############################################################

def main_loop(nir, red, path, num):

    img1 = red.astype(np.uint16)
    img2 = nir.astype(np.uint16)

    # Convert images to grayscale (for ORB detector).
    #gray1 = cv2.cvtColor(red, cv2.COLOR_RGB2GRAY)
    #gray2 = cv2.cvtColor(nir, cv2.COLOR_RGB2GRAY)

    # print('@@@@@ gray', gray1)

    # 1. Detect features and compute descriptors.

    kp1, desc1 = extract_features(red)
    kp2, desc2 = extract_features(nir)
    # print('{0} features detected in image1').format(len(kp1))
    # print('{0} features detected in image2').format(len(kp2))

    #orb1 = cv2.drawKeypoints(gray1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #orb2 = cv2.drawKeypoints(gray2, kp2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imwrite('Image1_orf.JPG', orb1)
    #cv2.imwrite('Image2_orb.JPG', orb2)
    # cv2.imshow('Features 1', orb1)
    # cv2.imshow('Features 2', orb2)
    # cv2.waitKey(0)

    # 2. Find corresponding features

    points1, points2 = find_matches(kp1, desc1, kp2, desc2)
    # print('{0} features matched').format(len(points1))

    # match = draw_matches(img1, img2, points1, points2)
    # cv2.imwrite('matching.JPG', match)
    # cv2.imshow('Matching', match)
    # cv2.waitKey(0)

    # 3. Find homgraphy

    H = find_homography(points1, points2)
    # print(H)
    # 4. Combine images into a panorama

    (size, offset) = calculate_size(img1, img2, H)

    # print('output size: {0}  offset: {1}').format(size, offset)

    panorama = merge_images(img1, img2, H, size, offset)

    nir = panorama.astype(np.uint8)
    nir[np.isnan(nir)] = 0

    print('@@@@@ nir shape', nir.shape)
    print('@@@@@ red shape', red.shape)

    np.seterr(divide='ignore', invalid='ignore')
    ndvi = ((nir - red) / (nir + red)).astype(float)

    ndvi[np.isnan(ndvi)] = 0

    ndvi_new = contrast_stretch(ndvi).astype(np.uint8)

    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(ndvi_new, kernel, iterations=1)

    kernel = np.ones((2, 2), np.uint8)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    #ndvi_new = dilation

    ndvi_values = np.count_nonzero(ndvi_new > 163)
    ndvi_new[ndvi_new < 163] = 0

    total_values = ndvi_new.shape[0] * ndvi_new.shape[1]
    percent = np.round((ndvi_values / total_values) * 100, 2)
    # kernel = np.ones((2, 2), np.uint8)
    # opening = cv2.morphologyEx(ndvi, cv2.MORPH_OPEN, kernel)
    # ndvi = opening

    if percent > 5:
        # kernel = np.ones((2, 2), np.uint8)
        # opening = cv2.morphologyEx(ndvi, cv2.MORPH_OPEN, kernel)
        # ndvi = opening

        name = path + '/' + 'image' + str(num) + '.jpg'

        print('@@@@@@ ', name)
        cv2.imwrite(name, ndvi_new)


def main():
    #global images

    directory = "/Volumes/BALAGUER/goodvegetation"

    output_path = "/Users/XavierBalaguer/Desktop/"

    new_path = create_directory(output_path)

    images = load_image(directory)

    nir = get_nir(images)
    red = get_red(images)

    # now we need to process the images of those both arrays

    i = 0
    while i < len(nir):

        img1 = red[i]
        img2 = nir[i]
        #nir, red = convert_images(img1, img2)  # array of nir and converted red images
        nirr = img2
        redd = img1
        try:
            main_loop(nirr, redd, new_path, i)
            i += 1
        except:
            i += 1

if __name__ == '__main__':
    main()






