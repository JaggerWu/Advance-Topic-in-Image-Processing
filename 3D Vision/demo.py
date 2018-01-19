import cv2
from matplotlib import pyplot as plt
import numpy as np

from compute import *
from sift_match import find_correspondence_points
from FmatrixModel import FundamentalMatrixModel
from Fmatrix import *
from ransac import *


def demo():
    im_1 = plt.imread('./rigidSfM/DSCN0974.JPG')
    im_2 = plt.imread('./rigidSfM/DSCN0975.JPG')

    pts1, pts2 = find_correspondence_points(im_1, im_2)

    num = pts1.shape[1]
    print('Totally {} points correspondence'.format(num))

    points1 = cart2hom(pts1)
    points2 = cart2hom(pts2)

    fig, ax = plt.subplots(1, 2)
    ax[0].autoscale_view('tight')
    ax[0].imshow(cv2.cvtColor(im_1, cv2.COLOR_BGR2RGB))
    ax[0].plot(points1[0], points1[1], 'r.')
    ax[1].autoscale_view('tight')
    ax[1].imshow(cv2.cvtColor(im_2, cv2.COLOR_BGR2RGB))
    ax[1].plot(points2[0], points2[1], 'r.')

    # compute F
    model = FundamentalMatrixModel()
    F, good_idxs = ransac(
        model=model, x=points1, y=points2, nsamples=5, threshold=10,
        maxiter =1000, desiredprob=0.9, debug=False)
    print(good_idxs)

    print('The number of inliner is {}'.format(len(good_idxs)))
    if good_idxs is None:
        raise ValueError('Failing in RANSAC')

    plot_epipolar_lines(im_1, im_2, points1[:, good_idxs], points2[:, good_idxs], F, show_epipole=False)

    # Using cv2 to find
    F, mask = cv2.findFundamentalMat(
        points1[:2].T, points2[:2].T, cv2.FM_RANSAC)
    print('The number of inliner by OpenCV is {}'.format(len(mask.ravel()==1)))
    plot_epipolar_lines(
        im_1, im_2, points1[:, mask.ravel()==1], points2[:, mask.ravel()==1], F, show_epipole=False)

    plt.show()

if __name__ == '__main__':
    demo()
