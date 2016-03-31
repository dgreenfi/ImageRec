import numpy
def main():
    from skimage import data, io, filters
    testfolder='/Users/davidgreenfield/Downloads/pics_boots/'
    testimage='B00A0GVP8A.jpg'
    image = io.imread(testfolder+testimage,flatten=True) # or any NumPy array!
    edges = filters.sobel(image)
    io.imshow(edges)
    io.show()



if __name__ == '__main__':
    main()
