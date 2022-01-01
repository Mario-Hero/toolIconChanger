# toolIconChanger 文件夹图标修改脚本

自己写了一个文件图标修改的Python脚本，只要把文件夹拖到这个脚本上，就可以用文件夹中的图片和视频作为文件夹的封面。如下图所示：

<img src="https://img2020.cnblogs.com/blog/1640902/202201/1640902-20220101144451489-1269406116.jpg" alt="Screenshot 2022-01-01 095804" style="zoom:50%;" />

# 依赖

Windows 系统

Python 3.x

截取视频截图作为封面需要安装opencv-python

# 用法

打包下载我的这个[GITHUB项目](https://github.com/Mario-Hero/toolIconChanger)所有文件。我一般给脚本建一个桌面快捷方式，方便使用。

一般情况下，用户只要把所需的封面图片命名为"cover.jpg"或"cover.png"，放入文件夹下，再把文件夹拖入脚本或快捷方式即可给文件夹添加封面。

对于本来就装满了图片的文件夹，不需要特意去找个cover图片，直接自动添加封面后也更美观、更好区分。

封面选取的优先级是这样的：

名为“icon.ico”的文件>名为"cover"的图片>第一张图片>第一个视频>第一个子文件夹的封面

默认情况下，即IGNORE_CHILD_FOLDERS = False时，该脚本会给子文件夹也都加上封面。IGNORE_CHILD_FOLDERS = True时不会修改子文件夹封面。

截取视频截图作为封面需要安装opencv-python，并设置脚本的CAPTURE_VIDEO_SCREENSHOT = True . 如果没有安装opencv-python，该脚本会自动安装。

视频截图的效果只能说聊胜于无，《老友记》的封面如下图所示。我还是建议自己给视频找封面，命名为cover.jpg放到文件夹下即可。

<img src="https://img2020.cnblogs.com/blog/1640902/202201/1640902-20220101144609747-1491579716.jpg" alt="Screenshot 2022-01-01 095622" style="zoom:50%;" />

当REBUILD_ICON = False时，假如子文件夹已经有了封面，就不会修改子文件夹的封面，但用户所拖入脚本的文件夹的封面仍会修改。当REBUILD_ICON = True时，就仍然会修改子文件夹和用户拖入的文件夹的封面。

# 实现原理

把用户的图片通过ImageMagick的convert.exe转换成ico格式，放入文件夹下。或者用OpenCV读取视频的帧，导出图片，转换成ico格式放入文件夹下。再修改文件夹下的desktop.ini，添加封面路径为"icon.ico"即可。

# License

The MIT License (MIT)


# 欢迎打赏！感谢支持！

<img src="https://files-cdn.cnblogs.com/files/mariocanfly/wechat.bmp" style="zoom:30%;" />
