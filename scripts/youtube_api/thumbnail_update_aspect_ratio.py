import os
from PIL import Image
from math import floor, ceil


def crop_thumbnail (img, ratio, filename):
    width, height = img.size
    left = 0
    upper = 0
    right = width
    lower = height
    
    if (width > height):
        new_width = (float) (ratio[0] * height) / ratio[1]
        if (new_width < width):
            left = (width - new_width)/2.0
            right = right -  (width - new_width) / 2.0
        else:
            new_height = (float) (ratio[1] * width) / ratio[0]
            upper = (height - new_height) / 2.0
            lower = lower - (height - new_height) / 2.0
    else:
        new_height = (float) (ratio[1] * width) / ratio[0]
        if (new_height < height):
            upper = (height - new_height) / 2.0
            lower = lower - (height - new_height) / 2.0
        else:
            new_width = (float) (ratio[0] * height) / ratio[1]
            left = (width - new_width)/2.0
            right = right -  (width - new_width) / 2.0
    print((int(floor(left)), int(floor(upper)), int(floor(right)), int(floor(lower))))
    img_crop = img.crop((int(floor(left)), int(floor(upper)), int(ceil(right)), int(ceil(lower))))
    #img_crop.show()
    img_crop.save(filename)
    print img_crop.size        


files_list = os.listdir(r'C:\Users\Aadish\Desktop\image_upload_video_id')
dir = (r'C:\Users\Aadish\Desktop\image_upload_video_id')
for file in files_list:
    print (file)
    try:
        img = Image.open( dir + '//' +file )
        width, height = img.size
        if ((float (width) / height) != 16.0/9 ):
            crop_thumbnail(img, (16, 9), (dir + '//16//' +file))
        else:
            img.save(dir + '//6//' +file)
         
        if ((float (width) / height) != 4.0/3 ):
            crop_thumbnail(img, (4, 3),(dir + '//4//' +file))
        else:
            img.save(dir + '//4//' +file)
    except:
        continue

img = Image.open (r'C:\Users\Aadish\Desktop\home_carousel_image.jpg')
crop_thumbnail(img, (128, 53), (r'C:\Users\Aadish\Desktop\home_carousel_image_crop.jpg'))    
         

    
