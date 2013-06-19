import site, sys
sys.path.append(r'C:\Users\Aadish\Documents\dg')
#site.addsitedir('/home/ubuntu/.virtualenv/dg_production/lib/python2.7/site-packages/')
from django.core.management import setup_environ
import settings
setup_environ(settings)


import gdata.youtube
import gdata.youtube.service
import urllib
import os
from PIL import Image
from PIL import ImageFilter
import string
from dashboard.models import Video
from boto.s3.connection import S3Connection


def get_thumbnail_from_id(id,videoid):
    try:
        yt_service = gdata.youtube.service.YouTubeService()
        entry = yt_service.GetYouTubeVideoEntry(video_id=id)
    
        file_save_dir = os.path.dirname(os.path.abspath(__file__))
    
        for thumbnail in entry.media.thumbnail:
            urllib.urlretrieve (thumbnail.url, 
                    os.path.join(file_save_dir, thumbnail.url.split("/")[-1]))
            img=Image.open( os.path.join(file_save_dir, thumbnail.url.split("/")[-1]))
            remove_border(img,videoid)
            break
            
    except:
        print("error in youtube id %s",id)
    

def remove_border(image,id):
    sz = image.size
    size = (0,0,sz[0],sz[1])
    image = image.crop((size[0]+10,size[1]+10,size[2]-10,size[3]-10))
    img = image.convert('L')
    
    img1 = img.point(lambda x: 0 if x < 127 else x)
    
    dir = (r'C:\Users\Aadish\Desktop\image_upload_video_id//')
    filename = ''
    filename = dir +str(id) + '.jpg'
    
    box = img1.getbbox()
    im_border_removed = image.crop(box)
    im_border_removed.save(filename)

def upload_thumbnail(id):
    pass

def statistics(id):
    dir = (r'C:\Users\Aadish\Desktop\image_upload_video_id//')
    filename = ''
    filename = dir + id + '.jpg'
    try:
        img=Image.open(filename)
        sz=img.size
        res=(sz[0]*9/sz[1], sz[0]*3/sz[1])
        return res
    except:
        print("error in opening file")
        return (0,0)
    


list_youtube_id = Video.objects.exclude(youtubeid = "").values_list('youtubeid','id')
dict_16={}
dict_4={}

for id in list_youtube_id:
    get_thumbnail_from_id(id[0], id[1]) # fetched image from url and crops the border
    tup = statistics(id)
     
    if tup[0] in dict_16:
                dict_16[tup[0]] += 1
    else:
                dict_16[tup[0]] = 1
       
    if tup[1] in dict_4:      
                dict_4[tup[1]] += 1
    else:
                dict_4[tup[1]] = 1
print (dict_16)
print (dict_4)
