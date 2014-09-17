# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backGroundC.ui'
#
# Created: Sat Jun 21 13:16:32 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4 import QtCore
import urllib
import os
import getpass
from xml.etree import ElementTree as ET

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


#定义主URL
bingURL = 'http://cn.bing.com'
#定义RSSURL
rssURL = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=8'
#定义图片地址URL
imageURL = ''

'''
通过BING的RSS得到DOM对象,获取节点
后拼接IMAGE路径保存到本地然后调用
Terminal执行设定BACKGROUND的命令
'''


def updateBack():
    #获取RSS源
    root = ET.fromstring(urllib.urlopen(rssURL).read())
    #查到最新的一张BING壁纸URL
    img = root.getiterator('image')[0].find('url').text
    #获取用户名，用来拼接图片路径
    user_name = getpass.getuser()
    #获取图片编号用来当作本地图片的名称
    name = root.getiterator('image')[0].find('fullstartdate').text
    #拼接图片
    imageURL = bingURL + img
    #下载图片
    urllib.urlretrieve(imageURL, r'/home/%s/%s.jpg' % ( user_name, name))
    #设置背景
    os.system('gsettings set org.gnome.desktop.background picture-uri "file:///home/%s/%s.jpg"' % (user_name, name ))


class Ui_MainWindow(QtGui.QMainWindow):
    def setupUi(self, MainWindow):
        try:
            #测试是否是开机启动，是的话直接更新背景完成后退出程序
            sys.argv[1]
            updateBack()
            sys.exit()

        except Exception, e:
            #否则判定为手动启动
            MainWindow.setObjectName(_fromUtf8("MainWindow"))
            MainWindow.resize(297, 130)
            self.centralwidget = QtGui.QWidget(MainWindow)
            self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
            self.pushButton = QtGui.QPushButton(self.centralwidget)
            self.pushButton.setGeometry(QtCore.QRect(10, 10, 281, 41))
            self.pushButton.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            self.pushButton.setObjectName(_fromUtf8("pushButton"))
            self.pushButton2 = QtGui.QPushButton(self.centralwidget)
            self.pushButton2.setGeometry(QtCore.QRect(10, 60, 281, 41))
            self.pushButton2.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
            self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
            MainWindow.setCentralWidget(self.centralwidget)
            self.statusbar = QtGui.QStatusBar(MainWindow)
            self.statusbar.setObjectName(_fromUtf8("statusbar"))
            MainWindow.setStatusBar(self.statusbar)
            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
            #链接点击事件
            self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.OnButtonFrush)
            self.connect(self.pushButton2, QtCore.SIGNAL('clicked()'), self.OnButtonAutoFrush)


    #点击自动更新按钮事件
    def OnButtonAutoFrush(self):
        try:
            #创建desktop文件放在启动文件夹下
            file = open("/home/%s/.config/autostart/autobing.desktop" % (getpass.getuser()), 'w')
            desktop = """[Desktop Entry]
Version=1.0
Encoding=UTF-8
Name=AutoBing
Type=Application
Exec=python "%s/%s" one
Terminal=false
Comment=auto change systembackground from bingimage
NoDisplay=false
Categories=Utility; """ % (os.getcwd(), os.path.basename(__file__))
            file.write(desktop)
            file.close()
            QtGui.QMessageBox.information(self, u'提示', u'自动更新设置成功\n如果移动了程序路径请重新设置')

        except Exception, e:
            QtGui.QMessageBox.information(self, u'提示', u'''设置自动更新失败''')
            raise e

    #点击刷新桌面壁纸
    def OnButtonFrush(self):
        try:
            updateBack()
            QtGui.QMessageBox.information(self, u'提示', u'''BING壁纸更新成功''')
            pass
        except Exception, e:
            QtGui.QMessageBox.information(self, u'提示', u'''更新失败''')
            raise

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "BING壁纸自动更换", None))
        self.pushButton.setText(_translate("MainWindow", "手动刷新", 'pushButton'))
        self.pushButton2.setText(_translate("MainWindow", "登陆自动刷新", 'pushButton2'))


class BingWindow(QtGui.QMainWindow):
    #初始化界面
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.madWindow()

    def madWindow(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


import sys

app = QtGui.QApplication(sys.argv)
myqq = BingWindow()
myqq.show()
sys.exit(app.exec_())
