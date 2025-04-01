# memos_db-sqlite3tomysql
use python3  and sqlite3 detabase to mysql database

最开始我使用了这个大佬（https://github.com/tigerzioo/memos_sqlite2mysql）的脚本 但是我的数据库太大了 4G 导致迁移过来的数据不完整 
然后重新写了一个脚本 使用这个脚本 可以把sqlite3 的数据库的数据迁移到 mysql 中来 我使用的 mysql5.7  python3.12
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
