#!/usr/bin/python3
# _*_ coding: UTF-8 _*_

# Created by Mario Chen, 01.01.2022, Shenzhen
# My Github site: https://github.com/Mario-Hero

import codecs
import os
import platform
import sys
from shutil import copyfile
import subprocess
import win32api
import win32con

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

INI_STR = '''[.ShellClassInfo]\r\n
IconResource=icon.ico,0\r\n
[ViewState]\r\n
Mode=\r\n
Vid=\r\n
FolderType=Pictures\r\n'''
PIC_EXT = [".jpg", ".jpeg", ".png", ".ico", ".bmp", ".gif"]
VID_EXT = ['.mp4', '.webm', '.avi', '.mov', '.mkv', '.wmv', '.3g2', '.3gp', '.3gp2', '.3gpp', '.amv',
           '.drc', '.dv', '.f4v', '.flv', '.m2ts',
           '.m4v', '.mp2', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg2', '.mpeg4', '.mpg', '.mpv2', '.mts',
           '.mxf', '.mxg', '.nsv', '.nuv', '.ogg', '.ogm', '.ogv', '.ps', '.rec', '.rm', '.rmvb', '.rpl', '.thp',
           '.tod', '.ts', '.tts', '.txd', '.vob', '.vro', '.wm', '.wtv', ]
rootFolder = ''


def toolIconChanger(root):
    try:
        print(os.path.split(root)[1])
    except:
        pass
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


def tranIco(jpgPath, funIcoPath):
    return subprocess.call(
        [".\\convert.exe", jpgPath, '-resize', '256x256', '-background', 'white', '-gravity', 'center', '-extent',
         '256x256', funIcoPath], shell=False) == 0


def setIcon(parent):
    try:
        win32api.SetFileAttributes(os.path.join(parent, "icon.ico"),
                                   win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)
        desktop_ini = os.path.join(parent, "desktop.ini")
        if os.path.exists(desktop_ini):
            os.remove(desktop_ini)
        f = codecs.open(desktop_ini, 'w', 'utf-8')
        f.write(INI_STR)
        f.close()
        win32api.SetFileAttributes(desktop_ini, win32con.FILE_ATTRIBUTE_HIDDEN + win32con.FILE_ATTRIBUTE_SYSTEM)
        # win32api.SetFileAttributes(parent, win32con.FILE_ATTRIBUTE_READONLY + win32con.FILE_ATTRIBUTE_SYSTEM)
        win32api.SetFileAttributes(parent, win32con.FILE_ATTRIBUTE_READONLY)
        return True
    except:
        return False


def findIconFile(parent):
    filenames = os.listdir(parent)
    foundIcon = ''
    iconFile = ''
    iconVideoFile = ''
    for file in filenames:
        if os.path.isfile(os.path.join(parent, file)):
            fileIsPic = False
            fileLower = file.lower()
            for extTemp in PIC_EXT:
                if fileLower.endswith(extTemp):
                    if fileLower.endswith(".ico"):
                        if file != "icon.ico":
                            if os.path.exists(os.path.join(parent, "icon.ico")):
                                os.remove(os.path.join(parent, "icon.ico"))
                            os.rename(os.path.join(parent, file), os.path.join(parent, "icon.ico"))
                            return True
                        else:
                            if REBUILD_ICON or rootFolder == parent:
                                os.remove(os.path.join(parent, "icon.ico"))
                            else:
                                return True

                    else:
                        if file.startswith('cover.'):
                            foundIcon = file
                        else:
                            if not iconFile:
                                iconFile = file
                    fileIsPic = True
                    break
            if not fileIsPic and not iconVideoFile and CAPTURE_VIDEO_SCREENSHOT:
                for extTemp in VID_EXT:
                    if fileLower.endswith(extTemp):
                        iconVideoFile = os.path.join(parent, file)
                        break

    if foundIcon:
        iconFile = foundIcon

    if iconFile:
        # cmd = ".\\convert.exe \"" + os.path.join(parent,iconFile) + "\" -resize 256x256 -background white -gravity center -extent 256x256 \"" + os.path.join(parent, "icon.ico") + "\""
        # img = PythonMagick.Image(os.path.join(parent, iconFile))
        # img.sample('256x256',"white")
        # img.write(os.path.join(parent, "icon.ico"))
        return tranIco(os.path.join(parent, iconFile), os.path.join(parent, "icon.ico"))
        # return subprocess.call([".\\convert.exe",os.path.join(parent,iconFile),"-resize 256x256 -background white -gravity center -extent 256x256",os.path.join(parent, "icon.ico")]) == 0
    else:
        if iconVideoFile and CAPTURE_VIDEO_SCREENSHOT:
            if os.path.exists(os.path.join(parent, "cover.jpg")):
                os.remove(os.path.join(parent, "cover.jpg"))
            if getFrame(iconVideoFile, os.path.join(parent, "cover.jpg")):
                return tranIco(os.path.join(parent, "cover.jpg"), os.path.join(parent, "icon.ico"))
                # cmd = ".\\convert.exe \"" + os.path.join(parent,"cover.jpg") + "\" -resize 256x256 -background white -gravity center -extent 256x256 \"" + os.path.join(parent, "icon.ico") + "\""
                # return subprocess.call([".\\convert.exe",os.path.join(parent,"cover.jpg"),"-resize 256x256 -background white -gravity center -extent 256x256",os.path.join(parent, "icon.ico")]) == 0
            else:
                return False
        else:
            return False


def getFrame(vidName, imgName):
    vidCapture = cv2.VideoCapture(vidName)
    if vidCapture.isOpened():
        frameNumber = vidCapture.get(7)
        # rate = vidCapture.get(5)
    else:
        return False
    cutTime = 5
    frames = []
    lightestTime = 1
    lightValue = 0
    notSuccessNumber = 0
    for i in range(1, cutTime):
        vidCapture.set(cv2.CAP_PROP_POS_MSEC, int((frameNumber / cutTime) * i))
        # print("f: "+str(int((frameNumber/cutTime)*i)))
        success, image = vidCapture.read()
        if success:
            frames.append(image)
            # cv2.imshow("img",image)
            # cv2.waitKey()
            # meanValue = cv2.mean(image)
            meanValue = cv2.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))[0]
            # print(meanValue)
            if meanValue > lightValue:
                lightValue = meanValue
                lightestTime = i
        else:
            notSuccessNumber += 1
    if notSuccessNumber >= cutTime - 1:
        return False
    if os.path.exists(imgName):
        os.remove(imgName)
    cv2.imencode('.jpg', frames[lightestTime - 1 - notSuccessNumber])[1].tofile(imgName)
    return True
    # print(cv2.imwrite(imgName, image))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for folder in sys.argv[1:]:
            # print(folder)
            if os.path.isdir(folder):
                rootFolder = folder
                toolIconChanger(folder)
            elif os.path.isfile(folder):
                parentFolder = os.path.split(folder)[0]
                icoPath = os.path.join(parentFolder, "icon.ico")
                isPic = False
                folderLower = folder.lower()
                for ext in PIC_EXT:
                    if folderLower.endswith(ext):
                        if os.path.exists(icoPath):
                            os.remove(icoPath)
                        # cmd = ".\\convert.exe \"" + folder + "\" -resize 256x256 -background white -gravity center -extent 256x256 \"" + icoPath + "\""
                        # img = PythonMagick.Image(os.path.join(parentFolder, iconFile))
                        # img.sample('256x256',"white")
                        # img.write(os.path.join(parentFolder, "icon.ico"))
                        if tranIco(folder, icoPath):
                            print(parentFolder)
                            setIcon(parentFolder)
                            isPic = True
                        break
                if not isPic and CAPTURE_VIDEO_SCREENSHOT:
                    for ext in VID_EXT:
                        if folderLower.endswith(ext):
                            if os.path.exists(os.path.join(parentFolder, "cover.jpg")):
                                os.remove(os.path.join(parentFolder, "cover.jpg"))
                            if getFrame(folder, os.path.join(parentFolder, "cover.jpg")):
                                # cmd = ".\\convert.exe \"" + os.path.join(parentFolder,"cover.jpg") + "\" -resize 256x256 -background white -gravity center -extent 256x256 \"" + icoPath + "\""
                                if os.path.exists(icoPath):
                                    os.remove(icoPath)
                                if tranIco(os.path.join(parentFolder, "cover.jpg"), icoPath):
                                    print(parentFolder)
                                    setIcon(parentFolder)
                            break

    platformName = platform.platform()
    if platformName.startswith("Windows-10"):  # also include Windows-11
        subprocess.call("ie4uinit.exe -show")  # Clear Icon Cache
    elif platformName.startswith("Windows-7"):
        subprocess.call("ie4uinit.exe -ClearIconCache")  # Clear Icon Cache
    # os.system("pause")
