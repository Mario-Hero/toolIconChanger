# toolIconChanger 文件夹图标修改脚本

自己写了一个文件图标修改的Python脚本，只要把文件夹拖动到这个脚本上，就可以用文件夹中的图片和视频作为文件夹的封面。把图片或视频拖到脚本上，就可以把这个图片或视频用作其所在文件夹的封面。

I wrote a python script to modify the file icon. If you drag the folder onto this script, the pictures and videos in the folder will be set as the icon of the folder. If you drag a picture or a video onto this script, they will be set as the icon of the parent folder of them. 

<img src="https://img2020.cnblogs.com/blog/1640902/202201/1640902-20220101144451489-1269406116.jpg" alt="Screenshot 2022-01-01 095804" style="zoom:50%;" />

# 依赖 Dependency 

Windows.

Python 3.x

截取视频截图作为封面需要安装 opencv-python

In order to capture screenshot of videos, you need to install opencv-python.

# 用法 Usage

打包下载我的这个项目所有文件。我一般给脚本建一个桌面快捷方式，方便使用。

Download all the files of this project.

一般情况下，用户只要把所需的封面图片放入文件夹下，再把图片拖入脚本或快捷方式即可给文件夹添加封面。

Put the cover photo into the folder, and then drag it onto the script or shortcut of script to add a cover to the folder.

如果文件夹封面没有变化，可以右键C盘->属性->磁盘清理->删除缩略图，来清除缩略图缓存。

If the cover of folder has not changed, you can clear the thumbnail cache by right-clicking disk C -> Properties -> Disk cleanup -> Delete thumbnail.

对于本来就装满了图片的文件夹，不需要特意去找个cover图片，直接自动添加封面后也更美观、更好区分。

For a folder which is already full of pictures, you don't need to find a cover picture. Just drag the folder to the script directly will make the folder more beautiful and better distinguished.

封面选取的优先级是这样的：

名为“icon.ico”的文件>名为"cover"的图片>第一张图片>第一个视频>第一个子文件夹的封面

The priority of cover selection is as follows:
File named "icon. ico" > picture named "cover" > the first picture > the first video > cover of the first subfolder

默认情况下，即IGNORE_CHILD_FOLDERS = False时，该脚本会给子文件夹也都加上封面。IGNORE_CHILD_FOLDERS = True时不会修改子文件夹封面。

By default,IGNORE_CHILD_FOLDERS = False, the script will also cover all subfolders. If IGNORE_CHILD_FOLDERS = True, the covers of subfolder will not be modified.

截取视频截图作为封面需要安装opencv-python，并设置脚本的CAPTURE_VIDEO_SCREENSHOT = True . 如果没有安装opencv-python，该脚本会自动安装。

To capture a video screenshot as a cover, you need to install opencv python and set CAPTURE_VIDEO_SCREENSHOT  to True .  If opencv python is not installed, the script will install it automatically.

视频截图的效果只能说聊胜于无，《老友记》的封面如下图所示。我还是建议自己给视频找封面，命名为cover.jpg放到文件夹下即可。

Capturing the video screenshot is not very effective. The cover of *Friends* is shown as the figure below. I suggest finding a cover for videos by yourselves.

<img src="https://img2020.cnblogs.com/blog/1640902/202201/1640902-20220101144609747-1491579716.jpg" alt="Screenshot 2022-01-01 095622" style="zoom:50%;" />

当REBUILD_ICON = False时，假如子文件夹已经有了封面，就不会修改子文件夹的封面，但用户所拖入的文件夹的封面仍会修改。当REBUILD_ICON = True时，就会修改子文件夹和用户拖入的文件夹的封面。

When REBUILD_ICON = false, if the subfolder already has a cover, the cover of the subfolder will not be modified, but the cover of the folder dragged into the script by the user will still be modified. When REBUILD_ICON = true, the covers of subfolders and folders dragged by users will still be modified.

当SET_LAST_IMG_AS_ICON = True时，在找不到名为cover的图片时，会使用名称顺序的最后一张图片为封面； 为False时会使用名称顺序第一张图片为封面。When SET_LAST_IMG_AS_ICON = True, when the picture named *cover* cannot be found, the last picture in order of name will be set as the cover; When it is false, the first picture is the cover.

# 实现原理 Principles of implementing 

把用户的图片通过ImageMagick的convert.exe转换成ico格式。或者用OpenCV读取视频的帧，导出图片，转换成ico格式。再修改文件夹下的desktop.ini，添加封面路径为"icon.ico"即可。

Through *convert.exe* from ImageMagick, we convert image into ICO format. Or we use OpenCV to read the video frame, export the picture, convert it into ICO format. Then modify the *desktop.ini*, add the cover image path as "icon. ico".

# License

The MIT License (MIT)


# 欢迎打赏！感谢支持！Thank you for your support!

<img src="https://files-cdn.cnblogs.com/files/mariocanfly/wechat.bmp" style="zoom:30%;" />
