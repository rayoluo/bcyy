# bcyy
## what does this program do
In order not to be a "卷王/奋斗逼", this program can help you to reserve a shuttle bus from Monday to Friday at 8:30 PM. In more detail, this program automatically check the time period when the bus reservation is avaliable (eg. 2020-11-07~2020-11-09), and it will reserve the shuttle bus from yiyuan to zhangyicun at the maxselldate(2020-11-09) 8:30 PM for you(**Attention**: not on Saturday!).

## usage
You need to fill in your id、password and reservation id in `demo.py`.

![image-20201108165440392](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201108165440392.png)

You also need to put this program on your server and use **crontab** to execute this python program at a fixed time(such as 12:00 PM every day).

### install crontab and start crontab service

```shell
# ubuntu
sudo apt install cron
service cron start
```

### edit cron task

```shell
crontab -e
```

![image-20201107211556873](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107211556873.png)

### add cron task

```shell
 1 0 * * * PYTHONIOENCODING=utf-8 python /yourpath/demo.py >> /yourpath/bcyy/bcyy.log 2>&1
```

![image-20201107232527292](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107232527292.png)

This command means executing this python program every day at 00:01 and append the output to the log file `bcyy.log`.

Don't lose **PYTHONIOENCODING=utf-8** ! Or some conflicts with `crontab` may happen!

### info in bcyy.log

![image-20201107212151027](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107212151027.png)

### update: add mail sending function

Fill in relevant information in `send_mail.py`. **Attention**：`mail_pass` is not your qq password, and you need to set smtp in you qq mail. Here is a teaching [page](http://www.jspxcms.com/documentation/351.html).

![image-20201108163919443](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201108163919443.png)



## Another version

If u don't need the mail notifying feature, u can try another version of this code (`ccliBcyy.py`), which provides a CLI and allows you to set the day of the week to book a roud trip.