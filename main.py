from PIL import Image
import os
import glob
import imghdr
import traceback
from memory_profiler import profile
from tqdm import tqdm
Image.LOAD_TRUNCATED_IMAGES = True


class ResizeImage:
    @profile
    def __init__(self, nowdir, img_dirname, dist_dirname):
        org_dir = nowdir + '/' + img_dirname
        self.imglen = len(self.get_image_list(org_dir))
        self.dist_dir = org_dir.replace(img_dirname, dist_dirname)
        self.pb = tqdm(total=self.imglen)
        self.resize_roop(org_dir)

    def resize_image(self, width, filename, org_dir, dist_dir):
        img = Image.open(org_dir + filename, 'r')
        if img.size[0] > width:
            after_width = width
        else:
            after_width = img.size[0]

        after_height = int(after_width / img.size[0] * img.size[1])

        resize_img = img.resize((after_width, after_height))
        try:
            resize_img.save(dist_dir + filename, quality=70)
        except:
            # traceback.print_exc()
            print('圧縮失敗:' + filename)

    def get_filelist(self, dir):
        return [r.split('/')[-1] for r in glob.glob(dir + '/*.*')]

    def get_dirlist(self, dirc):
        dirlist = []
        for r in glob.glob(dirc + '/*'):
            if os.path.isdir(r):
                dirlist.append(r)
        return dirlist

    def resize_roop(self, dirc):
        filelist = self.get_filelist(dirc)
        dirchildlist = self.get_dirlist(dirc)
        if not len(filelist) == 0:
            dist_dir = dirc.replace(img_dirname, dist_dirname)
            if not os.path.exists(self.dist_dir):
                os.mkdir(self.dist_dir + '/')
            if not os.path.exists(dist_dir):
                os.mkdir(dist_dir + '/')
            for f in filelist:
                if os.path.isfile(dirc
                                  + '/' + f) and imghdr.what(dirc + '/' + f):
                    self.resize_image(1000, f, dirc + '/', dist_dir + '/')
                    # print(str(self.count) + '/' + str(self.imglen)
                    #       + '  done: ' + dirc + '/' + f)
                    # self.pb.set_description("Processing %s" % f)
                    self.pb.update(1)
        if not len(dirchildlist) == 0:
            for d in dirchildlist:
                self.resize_roop(d)

    def get_image_list(self, path):
        file_list = []
        for (root, dirs, files) in os.walk(path):
            for file in files:
                target = os.path.join(root, file).replace("\\", "/")  # フルパス取得
                if os.path.isfile(target):
                    if imghdr.what(target):
                        file_list.append(target)
        return file_list


if __name__ == '__main__':
    nowdir = os.getcwd()
    img_dirname = '2012'
    dist_dirname = '2012'
    ri = ResizeImage(nowdir, img_dirname, dist_dirname)
