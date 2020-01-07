FROM python:3.6

WORKDIR /opt

COPY requirements.txt ./

RUN mkdir -p /root/.pip&&echo "[global]" > /root/.pip/pip.conf&&echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple">> /root/.pip/pip.conf

RUN echo "deb https://mirrors.aliyun.com/debian  stable main contrib non-free" > /etc/apt/sources.list
RUN echo "deb https://mirrors.aliyun.com/debian  stable-updates main contrib non-free" >> /etc/apt/sources.list

RUN apt-get update
RUN TZ=Asia/Shanghai&&ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#COPY sources.list /etc/apt/
# RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /usr/local/lib/python3.6/site-packages/airtest/core/android/static/adb/linux/adb 
CMD [ "python", "autoClockin.py" ]
