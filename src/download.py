from urllib.request import urlopen
from urllib.request import urlretrieve
import cv2
import numpy as np
import os

def store_raw_images():
    # the link of negative images
    neg_images_link = \
        'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152'
    # Open the link of negative images / decoded because byte
    neg_images_urls = urlopen(neg_images_link).read().decode()

    # Create directory for negative training set
    if not os.path.exists('neg'):
        os.makedirs('neg')

    # the starting suffix for the images we will save
    pic_num = 0

    for i in neg_images_urls.split('\n'):
        try:
            print(i)
            imgName = "neg/"+str(pic_num)+'.jpg'
            # download image
            urlretrieve(i, imgName)
            # Convert image to grayscale
            img = cv2.imread(imgName, cv2.IMREAD_GRAYSCALE)
            # Resize image
            resized_image = cv2.resize(img, (800,800))
            cv2.imwrite(imgName, resized_image)
            pic_num += 1

        except Exception as e:
            print(str(e))

def find_uglies():
    # iterate over all negative images
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            # Iterate over all unwanted images in the ugly folder
            for ugly in os.listdir('uglies'):
                try:
                    # get the path of the current image
                    current_image_path = str(file_type)+'/'+str(img)
                    # Read the ugly and the current image
                    ugly = cv2.imread('uglies/'+str(ugly))
                    isItUgly = cv2.imread(current_image_path)

                    # check if the 2 images has the same size and are not the same
                    if ugly.shape == isItUgly.shape and not(np.any(np.bitwise_xor(ugly, isItUgly))):
                        print('dayyyyyummmmmm girl you ugly!')
                        print(current_image_path)
                        # Remove the image
                        os.remove(current_image_path)

                except Exception as e:
                    print(str(e))


# Create description for negative and positive training sets
def create_pos_n_neg():
    for file_type in ['../samples/neg']:
        for img in os.listdir(file_type):
            if file_type == 'neg':
                # Negative image description is only its path
                line = file_type + '/' + img + '\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)
            """
            elif file_type == 'pos':
                # Positive image description is its path,
                #nbr of objects in the image, position and size of the object
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info.dat', 'a') as f:
                    f.write(line)
            """

#find_uglies()
#store_raw_images()
create_pos_n_neg()
