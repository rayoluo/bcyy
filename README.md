# bcyy
### what does this program do
In order not to be a "卷王/奋斗逼", this program can help you to reserve a shuttle bus from Monday to Friday at 8:30 PM. In more detail, this program automatically check the time period when the bus reservation is avaliable (eg. 2020-11-07~2020-11-09), and it will reserve the shuttle bus from yiyuan to zhangyicun at the maxselldate(2020-11-09) 8:30 PM for you(**Attention**: not on Saturday!).

### usage
You need to fill in your id and password.

![image-20201107174130109](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107174130109.png)

You also need to put this program on your server and use **crontab** to execute this python program at a fixed time(such as 12:00 PM every day).

##### install crontab and start crontab service

```shell
# ubuntu
sudo apt install cron
service cron start
```

##### edit cron task

```shell
crontab -e
```

![image-20201107211556873](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107211556873.png)

##### add cron task

```shell
 59 23 * * * PYTHONIOENCODING=utf-8 python /yourpath/demo.py >> /yourpath/bcyy/bcyy.log 2>&1
```

![image-20201107211707771](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107211707771.png)

This command means executing this python program every day at 23:59 and append the output to the log file `bcyy.log`.

Don't lose **PYTHONIOENCODING=utf-8** ! Or some conflicts with `crontab` may happen!

##### info in bcyy.log

![image-20201107212151027](https://gitee.com/oluoluo/typoraImage/raw/master/img/image-20201107212151027.png)