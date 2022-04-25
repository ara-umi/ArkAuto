<h1><div align=center>明日方舟后台脚本</div></h1>

<div align=center>
  <img src="https://github.com/ara-umi/ArkAuto/blob/main/READMEIMAGE/immediately.jpg" width=600 height=550></br>他们说第一张图一定要吸引人
  </div>
  

<h2>想说的话</h2>

- 之前考察过很多其他明日方舟的脚本，大部分还是用**ADB**或者**pyautogui**控制的。ADB我也装过，配置起来稍微麻烦了一点，但是很好用，基本上所有模拟器上的操作都可以用ADB来实现；相对来说pyautogui就不那么理想，因为它始终是前台的，会时时刻刻征用你的鼠标和键盘。我想做出一款能后台运行的且适用于大部分Windows窗口(不仅仅是模拟器)的后台操作库，并基于它来完成脚本的运行，因此诞生了用win32gui发送消息实现后台模拟键鼠的mywin32，我也在此基础上搭建起了该脚本。

- 功能上，因为我的第一个实验对象是我自己，所以开发的大部分功能的宗旨是：**简便/快捷/常用**。不需要繁琐的设定或者敲命令行，打开一个bat就能实现一个固定的功能，而这个功能往往是日常中最常用到的。对于一些特别个性化的需求，我觉得，投入精力和获得的收益不成正比，甲方的要求我们总是需要慎重对待的。

- 如果真的说这个脚本带来了什么改变，那就是它真的可以实现一边看直播一边刷。

<h2>测试环境</h2>

- Windows 10

- python3.9

- Nox(夜神模拟器)/LeiDian(雷电模拟器)

<h2>运行前我该注意什么？</h2>


- 首先你需要拥有一个漂亮的Python，我会在后续更新中将完善对于没有Python的小伙伴的帮助

- 目前我还没有更新resize功能，一切运行都是基于1600:900比例的窗口来进行的，后续完善后就不需要担心窗口大小的事情了

- 脚本运行是后台的，但不可以最小化，最小化的程序系统是不渲染画面的，所以是没办法截图和识别的

- 如果截图功能出现了问题，请检查Nox是否开启了OpenGL,若开启了请关闭；若还是不行，请通过dxdiag查看dx运行状态，这一部分我会写个文档

<h2>更新日志</h2>
- 2022 4.25</br>
更新了重复刷图和基建的批处理文件</br>
更新了自适应模拟器分辨率的功能</br>
