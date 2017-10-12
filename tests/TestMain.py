"""MainクラスのTestモジュール"""

import os
import shutil
import sys
import unittest
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
try:
    from main import ResizeImage
except:
    raise


class TestMain(unittest.TestCase):
    """test class main.py"""

    """セットアップ"""
    @classmethod
    def setUpClass(self):
        if not os.path.exists('./tests/img'):
            os.mkdir('./tests/img')
        img = Image.new('RGB', (2000, 768), (0xdd, 0xdd, 0xdd))
        img2 = Image.new('RGB', (450, 768), (0xdd, 0xdd, 0xdd))
        img.save('./tests/img/big.jpg')
        img2.save('./tests/img/small.png')
        if not os.path.exists('./tests/img/child'):
            os.mkdir('./tests/img/child')
        img.save('./tests/img/child/big.jpg')
        img2.save('./tests/img/child/small.gif')
        if not os.path.exists('./tests/img/child/child'):
            os.mkdir('./tests/img/child/child')
        img.save('./tests/img/child/child/big.jpg')
        img2.save('./tests/img/child/child/small.png')

        self.nowdir = os.path.dirname(os.path.abspath(__file__))
        img_dirname = 'img'
        dist_dirname = 'dist_img'
        self.ri = ResizeImage(self.nowdir, img_dirname, dist_dirname)

    """後処理"""
    @classmethod
    def tearDownClass(self):
        shutil.rmtree(self.nowdir + '/img')
        shutil.rmtree(self.nowdir + '/dist_img')

    """init"""
    def test_init(self):
        self.assertEqual(self.ri.org_dir,
                         self.nowdir + '/img', "org_dir is img")
        self.assertEqual(self.ri.dist_dir,
                         self.nowdir + '/dist_img', "dist_dir is dist_img")
        self.assertEqual(self.ri.pb, None, "pb is None")
        self.assertEqual(self.ri.img_dirname, 'img', "img_dirname is img")
        self.assertEqual(self.ri.dist_dirname, 'dist_img',
                         "dist_dirname is dist_img")

    """get_image_list"""
    def test_get_image_list(self):
        self.assertEqual(len(self.ri.get_image_list(self.ri.org_dir)),
                         6, "imglen is 6")

    """get_filelist"""
    def test_get_filelist(self):
        self.assertEqual(self.ri.get_filelist(self.ri.org_dir),
                         ['big.jpg', 'small.png'],
                         "filelist is ['big.jpg', 'small.png']")

    """get_dirlist"""
    def test_get_dirlist(self):
        self.assertEqual(self.ri.get_dirlist(self.ri.org_dir),
                         [self.nowdir + '/img/child'],
                         "dirlist is [child]")

    """fire"""
    def test_fire(self):
        self.ri.imglen = len(self.ri.get_image_list(self.ri.org_dir))
        self.ri.resize_roop(self.ri.org_dir)
        img = Image.open(self.nowdir + '/dist_img/big.jpg')
        img2 = Image.open(self.nowdir + '/dist_img/small.png')
        self.assertEqual(img.size, (1000, 384),
                         "dirlist is (1000, 384)")
        self.assertEqual(img2.size, (450, 768),
                         "dirlist is (450, 768)")


if __name__ == "__main__":
    unittest.main()
