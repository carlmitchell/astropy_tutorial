# This is a short tutorial for learning the basics of the package astropy,
# in particular the modules astropy.io.fits and astropy.wcs. There will also
# be a short introduction to the numpy package.

# The first thing we'll need to do is to import those packages.
from astropy.io import fits
from astropy import wcs
import numpy as np  # Here we've renamed numpy for convenience


# I'm going to define a "pause" function to pause the execution of the script
# at a handful of points to allow you to step through it, but you can ignore
# this part of the code. If you want to stop it from pausing, comment out the
# line "raw_input('Press Enter to continue:')
def pause():
    print('')
    raw_input('Press Enter to continue:')
    return

# You can learn about any python object by calling the help() function on it.
# You can un-comment this next line to see what "help(fits)" looks like.

# help(fits)

# To open an image file, we can use the fits.open() function
im1 = fits.open('N2280_B.fits')

# The variable "im1" now stores the open FITS file. FITS files are a *list*
# of objects called "header-data units" or "HDUs," so named because each unit
# can contain a header and a data array. The first (and in our case, only)
# HDU in our open image is "im1[0]"

# You can use the type() function to find out what kind of object a variable
# is. The next line shows that im1[0] is a HDU object using the type()
# function. You can un-comment the help() line to look at the documentation
# for HDU objects.

print(type(im1[0]))
pause()
# help(im1[0])

# We can also look at the header and data components of the HDU:
print(type(im1[0].data))
print(type(im1[0].header))
pause()

# Note that the data is an object called a "numpy.ndarray." The astropy
# package is built on top of the numpy package and uses its arrays to store
# image data. We can look at the image data as an array:

print(im1[0].data)
pause()

# Note that python doesn't print the whole array, since that would be HUGE.
# We can also look at the value of the data in a specific pixel, say (100,100):

print(im1[0].data[100, 100])
pause()

# Note that a lot of older programs start numbering arrays and lists at 1, but
# python starts numbering at 0. So pixel (100,100) in python is actually pixel
# (101,101) in DS9, IRAF, and Fortran.

# Another weird thing to note is that pixel (x,y) is represented by
# im1[0].data[y,x]. The arguments are backwards. It's unfortunate.

# Numpy arrays allow for lots of fancy "slicing" and here's where things start
# to get fun. What if we want to look at the entire 100th row of our image?
print(im1[0].data[100, :])
pause()

# Or the 100th column?
print(im1[0].data[:, 100])
pause()

# Or a 5x5 array containing the first 5 rows of the last 5 columns:
print(im1[0].data[:5, -5:])
pause()

# We can look at the "shape" of our data array:
print(im1[0].data.shape)
pause()

# This shows that our data array is 2049 x 2150 pixels. We can get at each of
# these numbers individually:
print(im1[0].data.shape[0])
print(im1[0].data.shape[1])
pause()

# Numpy has a few VERY useful functions for dealing with image coordinates,
# 'np.arange()' and 'np.meshgrid().' Let's look at np.arange() first. It
# creates an array which is N-long and contains the numbers 0 to (N-1). To get
# an array containing 0 through 9:
print(np.arange(10))
pause()

# np.meshgrid() takes two 1-D arrays as arguments and returns two 2-D arrays
# in a really clever way. The rows of the first array are all the same and
# each row is equal to the first argument. The columns of the second array are
# all the same and each is equal to the second array. For example:
a = np.array([1, 2, 3])
b = np.array([5, 6])
c, d = np.meshgrid(a, b)
print(c)
print(d)
pause()

# c is now a 2x3 array and each row is 1, 2, 3.
# d is now a 2x3 array and each column is 5, 6.

# Why is this useful? We can use these two functions along with the "shape"
# property of our data to get coordinate arrays!
xarray, yarray = np.meshgrid(np.arange(im1[0].data.shape[1]),
                             np.arange(im1[0].data.shape[0]))

print(xarray)
print(yarray)
pause()

# xarray[y,x] will now return x, and yarray[y,x] will return y. Conveniently,
# these arrays are the same shape as our image data:

print(im1[0].data.shape)
print(xarray.shape)
print(yarray.shape)
pause()

# You can act on entire numpy arrays as if they were individual numbers in
# complex ways. For example. let's say we want to know how far every pixel is
# from the point (5, 5). The formula for this should be:
# ( (x-5)^2 + (y-5)^2 )^(1/2).
# For taking the square root, we'll use the np.sqrt() function.
radius_array = np.sqrt((xarray - 5)**2 +
                       (yarray - 5)**2)
print(radius_array)
pause()

# We can now start asking questions like "which points are within 14 pixels of
# (10, 10).
print(radius_array <= 7)
pause()

# What you just saw was a "boolean array" full of Trues and Falses. Note that
# there's a handful of pixels in the upper-left of the array (which,
# confusingly, is the BOTTOM-left of the image) which give "True" and the rest
# give "False." What if we wanted to know how many of these pixels there are?
# The np.sum() function conveniently interprets "True" as a "1" and "False" as
# a "0", so we can do:
print(np.sum(radius_array <= 7))
pause()

# We can also start doing logical combinations of multiple conditions like
# this. For example, how many pixels are both within 7 pixels of (5, 5) AND
# have pixel values less than 10? The np.logical_and() function accomplishes
# this. There's similar functions for "not" and "or" operators.
print(np.sum(np.logical_and(radius_array <= 7,
                            im1[0].data < 10)))
pause()

# Note that we were ONLY able to do this because "radius_array" had the same
# shape as "im1[0].data". And it only had that shape because "xarray" and
# "yarray" did earlier. That's the power of np.meshgrid()!

# Numpy arrays allow for even fancier "slicing" than we've done so far. What
# if we waned to know the pixel values of all pixels within 7 pixels of (5, 5)
# which have pixel values less than 10? What if we want their coordinates? We
# can slice "im1[0].data" or "xarray" using a boolean array.

boolean_array = np.logical_and(radius_array <= 7,
                               im1[0].data < 10)
print(im1[0].data[boolean_array])
pause()

# We just printed all of the values of im1[0].data which satisfy that
# condition. We can get their coordinates in a similar way:
print(xarray[boolean_array])
print(yarray[boolean_array])
pause()

# All three of these arrays are in the same order and can be matched. Let's
# list all of the pixels that satisfy that condition above with their X
# coordinate, Y coordinate, and pixel value. This will be easiest in a loop,
# and we'll use the len() function to figure out how big that loop should be.
pix_values = im1[0].data[boolean_array]
x_coordinates = xarray[boolean_array]
y_coordinates = yarray[boolean_array]
for i in range(len(pix_values)):
    print(x_coordinates[i], y_coordinates[i], pix_values[i])
pause()

# Now let's switch gears and start looking at "world coordinate system" stuff,
# or WCS. The WCS information for our image is contained in the "header" part
# of the HDU, and we can generate a WCS object from it. You might also want to
# look at the help() documentation for WCS objects.
w1 = wcs.WCS(im1[0].header)
print(type(w1))
pause()
# help(w1)

# WCS objects have a "method" called "all_pix2world()" which lets you convert
# from pixel coordinates X and Y to sky coordinates RA and Dec. Let's find out
# where pixel (100, 100) is on the sky:
print(w1.all_pix2world(100, 100, 0))
pause()

# The units of what this function returns are degrees. RA is often quoted in
# hours rather than degrees, so be careful with that.

# That third argument (0) by the way is to tell it that we start counting our
# pixels from 0. Remember that DS9 and other old programs start counting from
# 1. If you're looking at pixel (100, 100) in DS9 and want to know where on the
# sky it is, use "w1.all_pix2world(100, 100, 1)"

# Now let's get ambitious. What if we want to know where *EVERY* pixel in our
# image is on the sky? Well thankfully, numpy arrays are black magic:
ra_array, dec_array = w1.all_pix2world(xarray, yarray, 0)
print(ra_array)
print(dec_array)
pause()

# We now have two arrays which are the same shape as our image, and those
# arrays contain the RA and Dec of every pixel in our image. That's awesome!

# Now let's get another image and start trying to match coordinates between the
# two. Note that our second image isn't even the same shape as the other; it's
# missing a few pixels.
im2 = fits.open('N2280_R.fits')
print(im1[0].data.shape)
print(im2[0].data.shape)
w2 = wcs.WCS(im2[0].header)
pause()

# WCS objects have another method called "all_world2pix()" which does the
# reverse of "all_pix2world()", i.e. they convert RA and Dec back into Xs and
# Ys. We can use this to convert im1's RA and Dec into coordinates in im2!
newxarray, newyarray = w2.all_world2pix(ra_array, dec_array, 0)
print(newxarray)
print(newyarray)
pause()

# Note that these new coordinate arrays aren't integers. Some of them are
# even outside the boundaries of our first image, because they don't fully
# overlap each other. Let's take care of the non-integer part first. np.rint()
# rounds a number to the nearest integer, and we can convert these values to
# integers using np.array() and an optional argument 'dtype':
newxarray = np.array(np.rint(newxarray), dtype='int')
newyarray = np.array(np.rint(newyarray), dtype='int')
print(newxarray)
print(newyarray)
pause()

# Ideally, we want to be able to do the following:
# newdata = im2[0].data[newyarray, newxarray]

# This would create an array the same shape as im1[0].data (because 'newxarray'
# and 'newyarray' have that shape, but containing the data of im2, shifted to
# the proper location.

# But we still can't, because 'newxarray' and 'newyarray' contain coordinate
# values that im2[0].data doesn't have. Feel free to uncomment that line to
# see the error message we get.

# So we'll have to do something a little trickier. Let's create an array of
# zeros which is the size we want. As usual, numpy has a convenient function
# for this:
newdata = np.zeros_like(im1[0].data)
print(newdata)
print(newdata.shape)
pause()

# We can start filling this array with data from im2[0].data using boolean
# arrays like we did before. Let's make the boolean array first. There are
# six things that might make a pixel "bad":
bad1 = newxarray < 0  # X is too small (less than 0)
bad2 = newyarray < 0  # Y is too small
bad3 = newxarray > newdata.shape[1]-1  # X is too large (above newdata's size)
bad4 = newyarray > newdata.shape[0]-1  # Y is too large
bad5 = newxarray > im2[0].data.shape[1]-1  # X is too large (above im2's size)
bad6 = newyarray > im2[0].data.shape[0]-1  # Y is too large

# Any one of these conditions will make a pixel "bad", so we want to combine
# them with an OR function.
boolean_array = np.logical_or(bad1, bad2)
boolean_array = np.logical_or(boolean_array, bad3)
boolean_array = np.logical_or(boolean_array, bad4)
boolean_array = np.logical_or(boolean_array, bad5)
boolean_array = np.logical_or(boolean_array, bad6)

# Finally, we actually care about good pixels, not bad ones. So we want to
# negate this.
boolean_array = np.logical_not(boolean_array)

# Slicing the "newxarray" coordinate array using this boolean array will
# return only the X coordinates of pixels which satisfy this "good" condition.
# The same will be true for the sliced y array: "newyarray[boolean_array]"

# Slicing im2[0].data using these sliced coordinate arrays will give us only
# the data values from those good pixels

# Now we can replace a "slice" of "newdata" with the same sized "slice" of
# im2[0].data using this boolean array and our "new" coordinate arrays!
newdata[boolean_array] = im2[0].data[newyarray[boolean_array],
                                     newxarray[boolean_array]]

# "newdata" now contains the data from image 2 shifted to the coordinate
# system of image 1, filled in with zeros wherever the data doesn't overlap.
# We might want to replace those zeros with "not a number" or "NaN", since
# that shows up as blank space in DS9. We can do that with more slicing and
# np.nan():
newdata[newdata == 0] = np.nan

# Or we can convert the NaN's back to zeros using the np.isnan() function to
# slice the array. np.isnan() returns "True" if a value is NaN and "False"
# otherwise.
newdata[np.isnan(newdata)] = 0

# I like to use NaNs instead of 0, but it's somewhat up to personal preference,
# so here I'm going to convert back to NaNs:
newdata[newdata == 0] = np.nan

# Finally, we need to save our new data array to a file! We can do that with
# fits.writeto() which is an astropy function. The "clobber=True" argument
# tells the function to overwrite a file if it already exists.
fits.writeto(filename='N2280_R_shifted.fits', data=newdata, clobber=True)

# Last but not least, we should always remember to close files we have opened.
im1.close()
im2.close()

# You now might want to pull up both N2280_B.fits and N2280_R_shifted.fits in
# ds9 and confirm that they are indeed aligned to each other now, whereas
# before they were several hundred pixels shifted from each other.
