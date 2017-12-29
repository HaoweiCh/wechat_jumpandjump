# 用鼠标玩微信跳一跳

## 缘起
微信刚刚更新了一个版本，主推了一个叫跳一跳的小程序。无奈手残，于是想办法提高自己的好友排名，于是有了这个。

## 最近更新
* 加入对 MIUI 系统的更新

## 原理
用usb调试安卓手机，用adb截图并用鼠标标记然后计算距离，再计算按压时间后模拟按压。

```
adb shell input swipe <x1> <y1> <x2> <y2> [duration(ms)] (Default: touchscreen) # 模拟长按
adb shell screencap <filename> # 保存截屏到手机
adb pull /sdcard/screen.png # 下载截屏文件到本地
```

## 使用方法
1. 在电脑上下载好adb
2. 打开安卓手机的usb调试模式并授权连接的电脑
    1.如果是小米手机，在USB调试下方有 USB调试（安全设置）打开(允许模拟点击)
3. 打开微信跳一跳，并点击开始
4. 在Constans.java中配置好adb路径与截图路径，运行BackgroundImage4Panel.java的main方法
5. 在弹出的窗口中先点击小人底部适当位置，然后再点想要跳的箱子的位置即可完成


