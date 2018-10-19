# Before trying to construct hybrid images, it is suggested that you
# implement my_imfilter.m and then debug it using proj1_test_filtering.py
import os
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from PIL import Image

from my_imfilter import my_imfilter
from vis_hybrid_image import vis_hybrid_image
from normalize import normalize
from gauss2D import gauss2D

def main():
    """ function to create hybrid images """
    # read images and convert to floating point format
    main_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    image1 = mpimg.imread(os.path.join(main_path, 'data', 'submarine.bmp'))
    image2 = mpimg.imread(os.path.join(main_path, 'data', 'fish.bmp'))
    image1 = image1.astype(np.float32)/255
    image2 = image2.astype(np.float32)/255

    # Several additional test cases are provided for you, but feel free to make
    # your own (you'll need to align the images in a photo editor such as
    # Photoshop). The hybrid images will differ depending on which image you
    # assign as image1 (which will provide the low frequencies) and which image
    # you asign as image2 (which will provide the high frequencies)

    ### Filtering and Hybrid Image construction ###
    cutoff_frequency = 7 # This is the standard deviation, in pixels, of the
    # Gaussian blur that will remove the high frequencies from one image and
    # remove the low frequencies from another image (by subtracting a blurred
    # version from the original version). You will want to tune this for every
    # image pair to get the best results.
    gaussian_filter = gauss2D(shape=(cutoff_frequency*4+1,cutoff_frequency*4+1), sigma = cutoff_frequency)


    #########################################################################
    # TODO: Use my_imfilter create 'low_frequencies' and                    #
    # 'high_frequencies' and then combine them to create 'hybrid_image'     #
    #########################################################################
    #########################################################################
    # Remove the high frequencies from image1 by blurring it. The amount of #
    # blur that works best will vary with different image pairs             #
    #########################################################################
    low_frequencies = my_imfilter(image1, gaussian_filter)

    ############################################################################
    # Remove the low frequencies from image2. The easiest way to do this is to #
    # subtract a blurred version of image2 from the original version of image2.#
    # This will give you an image centered at zero with negative values.       #
    ############################################################################
    high_frequencies = image2 - my_imfilter(image2, gaussian_filter)


    ############################################################################
    # Combine the high frequencies and low frequencies                         #
    ############################################################################
    hybrid_image = normalize(low_frequencies + high_frequencies)



    ### Visualize and save outputs ###
    plt.figure(1)
    plt.imshow(low_frequencies)
    plt.figure(2)
    plt.imshow(normalize(high_frequencies+0.5))
    vis = vis_hybrid_image(hybrid_image)
    plt.figure(3)
    plt.imshow(vis)
    plt.imsave(os.path.join(main_path, 'results/submarine_fish', 'low_frequencies.png'), low_frequencies, dpi=95)
    plt.imsave(os.path.join(main_path, 'results/submarine_fish', 'high_frequencies.png'), normalize(high_frequencies + 0.5), dpi=95)
    plt.imsave(os.path.join(main_path, 'results/submarine_fish', 'hybrid_image.png'), hybrid_image, dpi=95)
    plt.imsave(os.path.join(main_path, 'results/submarine_fish', 'hybrid_image_scales.png'), vis, dpi=95)
    plt.show()

if __name__ == '__main__':
    main()
