###钉钉自动打卡

在设定的时间进行轮询，直到手机连上公司wiff，自动解锁并打开钉钉极速打卡

需要开通极速打卡功能

###使用


sudo docker build -t clockin .

sudo docker run -d --restart=always --name dtalk_clockin -v "$PWD":/opt clockin python autoClockin.py

初次需要使手机♾链接到电脑。
手机usb链接电脑。adb devices 能够检测到手机后执行
adb tcpip 5555

