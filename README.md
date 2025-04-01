# memos_db-sqlite3tomysql
use python3  and sqlite3 detabase to mysql database

最开始我使用了这个大佬 https://github.com/tigerzioo/memos_sqlite2mysql  
的脚本 但是我的数据库太大了 4G 导致迁移过来的数据不完整 我上传的文件和图片等并不能转换过来 
由于我使用 sqlite3 的加载速度太慢了 我重新写了一个python脚本 使用这个脚本 可以把sqlite3 的数据库的数据迁移到 mysql 中来 我使用的 mysql5.7  python3.12

The migration scripts are for Memos
https://github.com/usememos/memos

我测试的环境是 memos0.24版本 转0.24版本 其他的没有测试过 另外之前脚本前请先备份自己的数据哦！ 
```bash
cp -r /memos/memos_prod.db ./memos_prod.db.bk
```
one 
安装 python and mysql 我在本地搭建的 mysql 然后通过 docker 搭建的 memos
two
```bash
docker run -d \
  --name memos-m \
  -p 5320:5230 \
  -v ~/.memos/:/var/opt/memos neosmemo/memos \
  --driver mysql \
  --dsn  'mysqlusername:mysqlpassword@tcp(ip:3306)/memos'
```
ip = ifconfig 然后看 docker o 网卡的 IP 地址即可 
three
这个脚本也会输出一个 sql 文件出来 可以自行只用一下命令导出
```bash
mysql -u memos -p memos_db < /mysqlpath/memos_db_backup.sql
```
这个脚本几乎包括了所有的内容比如这些文件和文章的时间 以及上传的文件的时间轴 
![image](https://github.com/user-attachments/assets/6ac22ac6-27b4-413e-a17e-742c29bf7566)

然后我发现系统设置的这些数据确实导入进 mysql了但是并没有生效 我也不清楚为什么  这个只有自己手动设置一下 但是用户信息等都是完整的 内容都完整 

![image](https://github.com/user-attachments/assets/0de21836-92cb-4549-99aa-7d9268281035)
![image](https://github.com/user-attachments/assets/f42b838f-ec94-4e4d-b4fb-7fb1dd1f89fa)


