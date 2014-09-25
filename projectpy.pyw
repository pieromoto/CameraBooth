import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import uic
import PIL
import cv2.cv as cv
import cv2
import time
from PIL import Image,ImageQt,ImageEnhance,ImageChops
import os.path

class About(QDialog):
    def __init__(self):
        QDialog.__init__(self,None)
        abo_win = uic.loadUi('about_ui.ui', self)

        self.label = abo_win.findChild(QLabel, "label")
        self.label.setText("""
                        ========== Camera-Booth ============
                                    Developed by Puriwat Khantiviriya
                                     E-mail: piero.moto@hotmail.com



                                                       ---NEX---

""")

class Setting(QWidget):
    def __init__(self):
        QWidget.__init__(self,None)
        set_win = uic.loadUi('settings.ui', self)

        self.entry = set_win.findChild(QLineEdit, "entry")
        self.bro_bt = set_win.findChild(QPushButton, "browsebt")
        self.bro_bt.connect(self.bro_bt, SIGNAL("clicked()"), self.browse_dir)
        
        try:
            file_dir = open("directory.txt","r")
            self.filedir = file_dir.read()
            self.entry.setText(self.filedir)
        except IOError:
            self.filename = "C:\Users\puriwat\Pictures"
            self.entry.setText(self.filedir)
            dir_file = open("directory.txt","w")
            dir_file.write(self.filedir)
            dir_file.close()
            
    def browse_dir(self):
        self.filetemp = QFileDialog.getSaveFileName(self, "Save file", "image",".png")
        self.filedir = self.filetemp.replace("image.png","")
        self.entry.setText(self.filedir)
        dir_file = open("directory.txt","w")
        dir_file.write(self.filedir)
        dir_file.close()
            
class ShowImage(QWidget):
    def __init__(self):
        QWidget.__init__(self,None)
        fil_win = uic.loadUi('showfilter.ui', self)
        self.i=0
        
        self.photo = fil_win.findChild(QGraphicsView, "photo")
        self.save_bt = fil_win.findChild(QPushButton, "save_bt")
        self.save_bt.connect(self.save_bt, SIGNAL("clicked()"), self.saveimg)
        self.lomo_bt = fil_win.findChild(QPushButton, "lomo_bt")
        self.lomo_bt.connect(self.lomo_bt, SIGNAL("clicked()"), self.lomo)
        self.neg_bt = fil_win.findChild(QPushButton, "neg_bt")
        self.neg_bt.connect(self.neg_bt, SIGNAL("clicked()"), self.negative)
        self.blur_bt = fil_win.findChild(QPushButton, "blur_bt")
        self.blur_bt.connect(self.blur_bt, SIGNAL("clicked()"), self.blur)
        self.bw_bt = fil_win.findChild(QPushButton, "bk_bt")
        self.bw_bt.connect(self.bw_bt, SIGNAL("clicked()"), self.blackwhite)
        self.red_bt = fil_win.findChild(QPushButton, "red_bt")
        self.red_bt.connect(self.red_bt, SIGNAL("clicked()"), self.redtone)
        self.blue_bt = fil_win.findChild(QPushButton, "blue_bt")
        self.blue_bt.connect(self.blue_bt, SIGNAL("clicked()"), self.bluetone)
        self.green_bt = fil_win.findChild(QPushButton, "green_bt")
        self.green_bt.connect(self.green_bt, SIGNAL("clicked()"), self.greentone)
        self.con_bt = fil_win.findChild(QPushButton, "con_bt")
        self.con_bt.connect(self.con_bt, SIGNAL("clicked()"), self.contour)
        self.em_bt = fil_win.findChild(QPushButton, "emboss_bt")
        self.em_bt.connect(self.em_bt, SIGNAL("clicked()"), self.emboss)
        self.pic_scene = QGraphicsScene()

        
        
        files = open("directory.txt","r")
        dirs = files.read()
        self.img = PIL.Image.open(dirs+"temp.png")
        self.outimg = self.img
        self.width, self.height = self.img.size
        files.close()
        self.imgQ = ImageQt.ImageQt(self.img)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)
        self.photo.fitInView(0, 0, 46, 27, Qt.KeepAspectRatio)
        
    def saveimg(self):
        files = open("directory.txt","r")
        dirs = files.read()
        filename = dirs+"image"+str(format(self.i,"02d"))+".png"
        while(os.path.isfile(filename)):
            self.i+=1
            filename = dirs+"image"+str(format(self.i,"02d"))+".png"
        self.outimg.save(filename)
        self.i+=1
        files.close()

    def lomo(self):
        self.imgr = self.img.resize((640,480))
        r, g, b = self.imgr.split()
        out_r = r
        out_g = g.point(lambda i: i*2)
        out_b = b
        source = [out_r, out_g, out_b]
        self.imgr = PIL.Image.merge( self.imgr.mode, source)
        
        vignette = PIL.Image.open("vignette.png")
        vignette = vignette.convert("RGBA")
        vignette = vignette.resize((640,480))

        self.imgr = self.imgr.convert("RGBA")

        r, g, b, alpha = vignette.split()
        alpha = alpha.point(lambda i: i*0.8)

        self.imgr = PIL.Image.composite(vignette, self.imgr, alpha)
        enchancer = PIL.ImageEnhance.Contrast(self.imgr)
        self.imgr = enchancer.enhance(1.25)
        self.lomopic = self.imgr.resize((self.width,self.height))
        self.outimg = self.lomopic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.lomopic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)
        

    def negative(self):
        self.negpic = ImageChops.invert(self.img)
        self.outimg = self.negpic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.negpic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)
    
    def blur(self):
        self.blurpic = self.img.filter(PIL.ImageFilter.BLUR)
        self.outimg = self.blurpic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.blurpic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)

    def blackwhite(self):
        self.imgr = self.img.resize((640,480))
        self.imgr = self.imgr.convert('RGBA')
        
        r, g, b, alpha = self.imgr.split()
        self.imgr = Image.merge( "RGBA", (r, r, r, alpha))
        self.bwpic = self.imgr.resize((self.width,self.height))
        self.outimg = self.bwpic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.bwpic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)
        
    def redtone(self):
        self.imgr = self.img.resize((640,480))
        r, g, b = self.imgr.split()
        out_r = r.point(lambda i: i*2)
        out_g = g.point(lambda i: i*0.0)
        out_b = b.point(lambda i: i*0.0)
        source = [out_r, out_g, out_b]
        self.imgr = PIL.Image.merge( self.imgr.mode, source)
        
        self.redpic = self.imgr.resize((self.width,self.height))
        self.outimg = self.redpic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.redpic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)

    def bluetone(self):
        self.imgr = self.img.resize((640,480))
        r, g, b = self.imgr.split()
        out_r = r.point(lambda i: i*0.0)
        out_g = g.point(lambda i: i*0.0)
        out_b = b.point(lambda i: i*2)
        source = [out_r, out_g, out_b]
        self.imgr = PIL.Image.merge( self.imgr.mode, source)
        
        self.bluepic = self.imgr.resize((self.width,self.height))
        self.outimg = self.bluepic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.bluepic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)

    def greentone(self):
        self.imgr = self.img.resize((640,480))
        r, g, b = self.imgr.split()
        out_r = r.point(lambda i: i*0.0)
        out_g = g.point(lambda i: i*2)
        out_b = b.point(lambda i: i*0.0)
        source = [out_r, out_g, out_b]
        self.imgr = PIL.Image.merge( self.imgr.mode, source)
        
        self.greenpic = self.imgr.resize((self.width,self.height))
        self.outimg = self.greenpic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.greenpic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)

    def contour(self):
        self.contourpic = self.img.filter(PIL.ImageFilter.CONTOUR)
        self.outimg = self.contourpic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.contourpic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)

    def emboss(self):
        self.embosspic = self.img.filter(PIL.ImageFilter.EMBOSS)
        self.outimg = self.embosspic
        self.pic_scene.clear()
        self.imgQ = PIL.ImageQt.ImageQt(self.embosspic)
        pixMap = QPixmap.fromImage(self.imgQ)
        self.pic_scene.addPixmap(pixMap)
        self.photo.setScene(self.pic_scene)

    

class HideFile(QWidget):
    def __init__(self):
        QWidget.__init__(self,None)
        hide_win = uic.loadUi('hidefile.ui', self)
        self.setWindowTitle("Hidden Feature(Hide File)")
        
        self.text_entry = hide_win.findChild(QLineEdit, "lineEdit")
        self.img_entry = hide_win.findChild(QLineEdit, "lineEdit_2")
        self.text_bro_bt = hide_win.findChild(QPushButton, "pushButton")
        self.text_bro_bt.connect(self.text_bro_bt, SIGNAL("clicked()"), self.browse_text)
        self.img_bro_bt = hide_win.findChild(QPushButton, "pushButton_2")
        self.img_bro_bt.connect(self.img_bro_bt, SIGNAL("clicked()"), self.browse_img)
        self.hide_bt = hide_win.findChild(QPushButton, "pushButton_3")
        self.hide_bt.connect(self.hide_bt, SIGNAL("clicked()"), self.hide)

    def browse_text(self):
        self.file_dir = QFileDialog.getOpenFileName(self, 'Open file', "")
        self.text_file = open(self.file_dir, "rb")
        self.text_entry.setText(self.file_dir)
        
    def browse_img(self):
        self.img_dir = QFileDialog.getOpenFileName(self, 'Open file', "")
        self.img_file = open(self.img_dir, "a+b")
        self.img_entry.setText(self.img_dir)
        
    def hide(self):
            self.img_file.write("\n\n")
            self.img_file.write(self.text_file.read())
            self.text_file.close()
            self.img_file.close()
            
        
class UI(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self,None)
        main_win = uic.loadUi('proj.ui', self)

        self.mainwindow = main_win.findChild(QWidget, "centralwidget")
        self.view = main_win.findChild(QGraphicsView, "img")
        self.cap_bt = main_win.findChild(QPushButton, "capturebt")
        self.cap_bt.connect(self.cap_bt, SIGNAL("clicked()"), self.show_image)
        self.set_bt = main_win.findChild(QPushButton, "settingbt")
        self.set_bt.connect(self.set_bt, SIGNAL("clicked()"), self.show_setting)
        self.abo_bt = main_win.findChild(QPushButton, "aboutbt")
        self.abo_bt.connect(self.abo_bt, SIGNAL("clicked()"), self.show_about)
        self.se_img = main_win.findChild(QPushButton, "sebt")
        self.se_img.connect(self.se_img, SIGNAL("clicked()"), self.show_secret)
        self.img_scene = QGraphicsScene()

        self.camcapture = cv.CaptureFromCAM(0)
        t=QTimer(self)
        t.timeout.connect(self.update_cap)
        t.start(0)

    def update_cap(self):
        self.frame = cv.QueryFrame(self.camcapture)
        width = self.frame.width
        height = self.frame.height
        self.image = QImage(self.frame.tostring(), width, height, QImage.Format_RGB888).rgbSwapped()
        self.imgQ = self.image.scaled(779,459)
        pixmap = QPixmap.fromImage(self.imgQ)
        self.img_scene.addPixmap(pixmap)
        self.view.setScene(self.img_scene)
        time.sleep(1/10)
        
    def show_about(self):
        self.about = About()
        self.about.show()
    def show_setting(self):
        self.setting = Setting()
        self.setting.show()
    def show_secret(self):
        self.secret = HideFile()
        self.secret.show()
    def show_image(self):
        files = open("directory.txt","r")
        dirs = files.read()
        self.imgQ.save(dirs+"temp.png")
        files.close()
        self.cap = ShowImage()
        self.cap.show()
        
def main():
    app=QApplication(sys.argv)
    window=UI()
    window.show()
    return app.exec_()

    

if __name__ == "__main__":
    sys.exit(main())
    cv.DestroyWindow('camera')

    sys.exit(app.exec_())

            
