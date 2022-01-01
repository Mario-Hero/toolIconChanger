#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Mario Chen, 01.01.2022, Shenzhen
# My Github site: https://github.com/Mario-Hero

import os, codecs, sys
import win32con, win32api
from shutil import copyfile

# you can change it >>>>>

REBUILD_ICON = False  # Set it True to rebuild icons of all select folders
IGNORE_CHILD_FOLDERS = False  # Set it True to not change icons of child folders
CAPTURE_VIDEO_SCREENSHOT = True  # Set it True to capture screenshot of videos in order to make icons of folders

# <<<<< you can change it

if CAPTURE_VIDEO_SCREENSHOT:
    try:
        import cv2
    except ImportError:
        os.system("pip install opencv-python")
        import cv2

ini_str = '''[.ShellClassInfo]\r\n
IconResource=icon.ico,0\r\n
[ViewState]\r\n
Mode=\r\n
Vid=\r\n
FolderType=Pictures\r\n'''
picExt = [".jpg", ".jpeg", ".png", ".ico", "bmp", ".gif"]
vidExt = ['mp4', 'webm', 'avi', 'mov', '.mkv', '.wmv', '.3g2', '.3gp', '.3gp2', '.3gpp', '.amv',
          '.drc', '.dv', '.f4v', '.flv', '.m2ts',
          '.m4v', '.mp2', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg2', '.mpeg4', '.mpg', '.mpv2', '.mts',
          '.mxf', '.mxg', '.nsv', '.nuv', '.ogg', '.ogm', '.ogv', '.ps', '.rec', '.rm', '.rmvb', '.rpl', '.thp',
          '.tod', '.ts', '.tts', '.txd', '.vob', '.vro', '.wm', '.wtv', ]
rootFolder = ""


def toolIconChanger(root):
    print(os.path.split(root)[1])
    rootHaveIcon = False
    childHaveIcon = False
    fileList = os.listdir(root)
    if (not REBUILD_ICON) and rootFolder != root:
        existPart = 0
        for file in fileList:
            if file == "desktop.ini":
                existPart += 1
            elif file == "icon.ico":
                existPart += 1
            if existPart >= 2:
                return True

    if findIconFile(root):
        setIcon(root)
        rootHaveIcon = True

    if not IGNORE_CHILD_FOLDERS:
        for file in fileList:
            if os.path.isdir(os.path.join(root, file)):
                if toolIconChanger(os.path.join(root, file)):
                    if (not childHaveIcon) and (not rootHaveIcon):
                        try:
                            copyfile(os.path.join(os.path.join(root, file), "icon.ico"), os.path.join(root, "icon.ico"))
                            childHaveIcon = True
                        except:
                            continue
        if childHaveIcon:
            setIcon(root)
    return rootHaveIcon or childHaveIcon


def setIcon(parent):
    try:
        win32api.SetFileAttributes(os.path.join(parent, "icon.ico"),
                                   win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)
        desktop_ini = os.path.join(parent, "desktop.ini")
        if os.path.exists(desktop_ini):
            os.remove(desktop_ini)
        f = codecs.open(desktop_ini, 'w', 'utf-8')
        f.write(ini_str)
        f.close()
        win32api.SetFileAttributes(desktop_ini, win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)
        # win32api.SetFileAttributes(parent, win32con.FILE_ATTRIBUTE_READONLY + win32con.FILE_ATTRIBUTE_SYSTEM)
        win32api.SetFileAttributes(parent, win32con.FILE_ATTRIBUTE_READONLY)
    except:
        return


def findIconFile(parent):
    filenames = os.listdir(parent)
    foundIcon = ""
    iconFile = ""
    iconVideoFile = ""
    for file in filenames:
        if os.path.isfile(os.path.join(parent, file)):
            isPic = False
            for ext in picExt:
                if file.endswith(ext):
                    if file.endswith(".ico"):
                        if file != "icon.ico":
                            if os.path.exists(os.path.join(parent, "icon.ico")):
                                os.remove(os.path.join(parent, "icon.ico"))
                            os.rename(os.path.join(parent, file), os.path.join(parent, "icon.ico"))
                            return True
                        else:
                            if REBUILD_ICON:
                                os.remove(os.path.join(parent, "icon.ico"))
                            else:
                                return True

                    else:
                        if "cover" in file:
                            foundIcon = file
                        else:
                            if not iconFile:
                                iconFile = file
                    isPic = True
                    break
            if not isPic and not iconVideoFile and CAPTURE_VIDEO_SCREENSHOT:
                for ext in vidExt:
                    if file.endswith(ext):
                        iconVideoFile = os.path.join(parent, file)
                        break

    if foundIcon:
        iconFile = foundIcon

    if iconFile:
        cmd = ".\\convert.exe \"" + os.path.join(parent,
                                                 iconFile) + "\" -resize 256x256 -background white -gravity center -extent 256x256 \"" + os.path.join(
            parent, "icon.ico") + "\""
        # img = PythonMagick.Image(os.path.join(parent, iconFile))
        # img.sample('256x256',"white")
        # img.write(os.path.join(parent, "icon.ico"))
        return os.system(cmd) == 0
    else:
        if iconVideoFile and CAPTURE_VIDEO_SCREENSHOT:
            if os.path.exists(os.path.join(parent, "cover.jpg")):
                os.remove(os.path.join(parent, "cover.jpg"))
            if getFrame(iconVideoFile, os.path.join(parent, "cover.jpg")):
                cmd = ".\\convert.exe \"" + os.path.join(parent,
                                                         "cover.jpg") + "\" -resize 256x256 -background white -gravity center -extent 256x256 \"" + os.path.join(
                    parent, "icon.ico") + "\""
                return os.system(cmd) == 0
            else:
                return False
        else:
            return False


def getFrame(video_name, img_name):
    vidcap = cv2.VideoCapture(video_name)
    if vidcap.isOpened():
        frame_num = vidcap.get(7)
        # rate = vidcap.get(5)
    else:
        return False
    cutN = 6
    frames = []
    lightEst = 1
    lightValue = 0
    notSuccessNumber = 0
    for i in range(1, cutN):
        vidcap.set(cv2.CAP_PROP_POS_MSEC, int((frame_num / cutN) * i))
        # print("f: "+str(int((frame_num/cutN)*i)))
        success, image = vidcap.read()
        if success:
            frames.append(image)
            # cv2.imshow("img",image)
            # cv2.waitKey()
            # meanValue = cv2.mean(image)
            meanValue = cv2.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))[0]
            # print(meanValue)
            if meanValue > lightValue:
                lightValue = meanValue
                lightEst = i
        else:
            notSuccessNumber += 1
    if notSuccessNumber >= cutN - 1:
        return False
    if os.path.exists(img_name):
        os.remove(img_name)
    cv2.imencode('.jpg', frames[lightEst - 1 - notSuccessNumber])[1].tofile(img_name)
    return True
    # print(cv2.imwrite(img_name, image))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # toolIconChanger("./")
        pass
    else:
        for folder in sys.argv[1:]:
            # print(folder)
            if os.path.isdir(folder):
                rootFolder = folder
                toolIconChanger(folder)
    # os.system("pause")