from django.core.management import setup_environ
import dg.settings
setup_environ(dg.settings)
import sys, os, glob , string
from PIL import Image

def make_contact_sheet(fnames,(ncols,nrows),(photow,photoh),
                       (marl,mart,marr,marb),
                       padding):
    """\
    Make a contact sheet from a group of filenames:

    fnames       A list of names of the image files
    
    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marl         The left margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """

    # Read in all images and resize appropriately
    imgs = [Image.open(fn).resize((photow,photoh),Image.ANTIALIAS) for fn in fnames]
    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl+marr
    marh = mart+ marb

    padw = (ncols-1)*padding
    padh = (nrows-1)*padding
    isize = (ncols*photow+marw+padw,nrows*photoh+marh+padh)

    # Create the new image. The background doesn't have to be white
    white = (255,255,255)
    inew = Image.new('RGB',isize,white)

    # Insert each thumb:
    for irow in range(nrows):
        for icol in range(ncols):
            left = marl + icol*(photow+padding)
            right = left + photow
            upper = mart + irow*(photoh+padding)
            lower = upper + photoh
            bbox = (left,upper,right,lower)
            try:
                img = imgs.pop(0)
            except:
                break
            inew.paste(img,bbox)
    return inew

def get_immediate_subdirectories(dir):
    return [os.path.join(dir, name) for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]
    
    
root_dir =  r'C:\Users\Yash\Desktop\DG\scripts\village_wise'
dirs = get_immediate_subdirectories(root_dir)

collage_made = 0
for dir in dirs:
    image_list = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            filename = os.path.join(root, name)
            image_list.extend(glob.glob(filename))
    files = image_list
    ncols = 3
    nrows = 3
    photow,photoh = 50,50
    # Don't bother reading in files we aren't going to use
    if len(files) > ncols*nrows: files = files[:ncols*nrows]
    
    # These are all in terms of pixels:
    if len(files) < 9:
        ncols = nrows = 2 
        photow,photoh = 75,75
    if len(files) < 4:
        ncols = nrows = 1 
        photow,photoh = 150,150
        
    photo = (photow,photoh)
    
    margins = [0,0,0,0]
    
    padding = 0
    
    inew = make_contact_sheet(files,(ncols,nrows),photo,margins,padding)
    image_name = str(dir) + ".jpg"
    dst_file = os.path.join(root_dir,image_name)
    inew.save(dst_file)
    collage_made += 1
    #os.system('display bs.png')
    
print str(collage_made) + " images made"
