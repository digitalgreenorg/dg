from userfile_functions import upload_file
import os, shutil

scripts_dir = os.path.dirname(__file__)
dir = scripts_dir + "\case_update"
completed_dir = scripts_dir + "\uploaded"
if not os.path.exists(completed_dir):
    os.makedirs(completed_dir)
files = os.listdir(dir)
uploaded = []
for file in files:
    filename = os.path.join(dir,file)
    try : 
        response = upload_file(filename)
        if response == 201 or response == 200:
            uploaded.append(filename)
            shutil.move(filename, completed_dir)
    except Exception as ex:
        pass
    