# 用鼠标玩微信跳一跳

## 缘起
微信刚刚更新了一个版本，主推了一个叫跳一跳的小程序。无奈手残，于是想办法提高自己的好友排名，于是有了这个。  
*项目灵感来源于网络*，增加对MIUI(包括 xiaomi.eu)的支持，增加自动识别起点

## 使用方法
1. 在电脑上下载好adb
2. 配置好 Python 的环境 (安装python3.6，安装依赖包 `pip install -r requirments.txt`)
2. 打开安卓手机的usb调试模式并授权连接的电脑
    * 如果是小米手机，在USB调试下方有 USB调试（安全设置）打开(允许模拟点击)
3. 打开微信跳一跳，并点击开始
5. **点想要跳的箱子的位置即可**

## 截屏
![](https://raw.githubusercontent.com/Chaaang/wechat_jumpandjump/master/screen.png)

## 最近更新
* 加入对 MIUI 系统的更新
* 结构更新，程序直接运行
* 加入对起点自动识别，用户只需要点击最后一步

## 原理
用usb调试安卓手机，用adb截图并用鼠标标记然后计算距离，再计算按压时间后模拟按压。

```
adb shell input swipe 
adb shell screencap
adb pull 
```


