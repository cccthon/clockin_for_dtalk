###钉钉自动打卡

#在设定的时间进行轮询，直到手机连上公司wiff，自动解锁并打开钉钉自动极速打卡

#需要开通极速打开功能

###使用

git clone ......

sudo docker build -t clockin .

sudo docker run -d --restart=always --name dtalk_clockin -v "$PWD":/opt clockin python autoClockin.py
