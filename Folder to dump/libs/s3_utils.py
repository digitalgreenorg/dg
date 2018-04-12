from boto.s3.key import Key

def add_to_s3(bucket, key, filepath):
    k = Key(bucket)
    k.key = key
    k.set_contents_from_filename(filepath)
    k.make_public()