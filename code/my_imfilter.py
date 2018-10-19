import numpy as np
import time


def my_imfilter(image, imfilter):
    """function which imitates the default behavior of the build in scipy.misc.imfilter function.

    Input:
        image: A 3d array represent the input image.
        imfilter: The gaussian filter.
    Output:
        output: The filtered image.
    """
    ###################################################################################
    # TODO:                                                                           #
    # This function is intended to behave like the scipy.ndimage.filters.correlate    #
    # (2-D correlation is related to 2-D convolution by a 180 degree rotation         #
    # of the filter matrix.)                                                          #
    # Your function should work for color images. Simply filter each color            #
    # channel independently.                                                          #
    # Your function should work for filters of any width and height                   #
    # combination, as long as the width and height are odd (e.g. 1, 7, 9). This       #
    # restriction makes it unambigious which pixel in the filter is the center        #
    # pixel.                                                                          #
    # Boundary handling can be tricky. The filter can't be centered on pixels         #
    # at the image boundary without parts of the filter being out of bounds. You      #
    # should simply recreate the default behavior of scipy.signal.convolve2d --       #
    # pad the input image with zeros, and return a filtered image which matches the   #
    # input resolution. A better approach is to mirror the image content over the     #
    # boundaries for padding.                                                         #
    # Uncomment if you want to simply call scipy.ndimage.filters.correlate so you can #
    # see the desired behavior.                                                       #
    # When you write your actual solution, you can't use the convolution functions    #
    # from numpy scipy ... etc. (e.g. numpy.convolve, scipy.signal)                   #
    # Simply loop over all the pixels and do the actual computation.                  #
    # It might be slow.                                                               #
    ###################################################################################
    ###################################################################################
    # NOTE:                                                                           #
    # Some useful functions                                                           #
    #     numpy.pad or numpy.lib.pad                                                  #
    # #################################################################################

    # Uncomment if you want to simply call scipy.ndimage.filters.correlate so you can
    # see the desired behavior.
    output = np.zeros_like(image)
    #import scipy.ndimage as ndimage
    #output = np.zeros_like(image)
    #for ch in range(image.shape[2]):
    #    output[:,:,ch] = ndimage.filters.correlate(image[:,:,ch], imfilter, mode='constant')
    x_pad = int((imfilter.shape[1] - 1) / 2)
    y_pad = int((imfilter.shape[0] - 1) / 2)
    if len(image.shape) == 2:
        image = np.pad(image, ((y_pad, y_pad),(x_pad, x_pad)), \
                        'constant', constant_values=((0,0),(0,0)))
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                im_part = image[i:i+imfilter.shape[0], j:j+imfilter.shape[1]]
                output[i, j] = (impart * imfilter).sum()
    else:
        assert len(image.shape) == 3, 'dims error'
        image = np.pad(image, ((y_pad, y_pad),(x_pad, x_pad),(0, 0)), 'constant')

        #version1
        start = time.time()
        for c in range(3):
            for i in range(output.shape[0]):
                for j in range(output.shape[1]):
                    im_part = image[i:i+imfilter.shape[0], j:j+imfilter.shape[1], c]
                    output[i, j, c] = (im_part * imfilter).sum()
        end = time.time()

        '''
        #version2
        start = time.time()
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                im_part = np.transpose(image[i:i+imfilter.shape[0], j:j+imfilter.shape[1], :], (2,0,1))
                temp = np.transpose(im_part*imfilter, (1,2,0))
                output[i, j, :] = temp.sum(axis=0).sum(axis=0)
        end = time.time()
        '''
        '''
        #version3
        start = time.time()
        filter = np.repeat(imfilter[:,:,np.newaxis], 3, axis=2)
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                im_part = image[i:i+imfilter.shape[0], j:j+imfilter.shape[1], :]
                output[i, j, :] = (im_part * filter).sum(axis=0).sum(axis=0)

        end = time.time()
        '''
        print('Time: {}secs'.format(end-start))
    ###################################################################################
    #                                 END OF YOUR CODE                                #
    ###################################################################################
    return output
