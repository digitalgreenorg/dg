import urllib
from math import ceil, floor
from PIL import Image

class ProcessedImage(Image):
    def __init__(self, image=image):
        self.image = image
    
    def set_image_from_url(self, url, filepath):
        urllib.urlretrieve(url, filepath)
        self.image = Image.open(filepath)
    
    def save(self, filepath):
        self.image.save(filepath)
    
    def remove_border(self):
        size = (0, 0, self.image.size[0], self.image.size[1])
        # Several thumbnails had bright white lines along the sides
        # As a hack, we are cropping the sides so that these lines may get cropped at the outset.
        image = self.image.crop((size[0] + 10, size[1] + 10, size[2] - 10, size[3] - 10))
        # Convert image to grayscale
        img_gray = self.image.convert('L')
        # Convert dark areas to black, on a 127 threshold
        img_dull = img_gray.point(lambda x: 0 if x < 127 else x)
        box = img_dull.getbbox()
        return ProcessedImage(image=self.image.crop(box))
    
    def crop(self, new_width, new_height):
        ratio = new_width * 1.0 / new_height
        width, height = self.image.size
        region = {
            'l': 0,
            'r': width,
            'upper': 0,
            'lower': height,
        }
        if width > height * ratio:
            crop = (width - height * ratio) / 2.0
            region['l'] = int(floor(crop))
            region['r'] = int(ceil(width - crop))
        else:
            crop = (height - width / ratio) / 2.0
            region['upper'] = int(floor(crop))
            region['lower'] = int(ceil(height - crop))
        img_crop = self.image.crop((region['l'], region['upper'], region['r'], region['lower']))
        img_resized = img_crop.resize((new_width, new_height), Image.ANTIALIAS)
        return ProcessedImage(image=img_resized)
