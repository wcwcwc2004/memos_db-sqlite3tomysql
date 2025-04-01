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
 通过memos 的 docker 去创建基础的 memos 的数据库的表格
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

 目前我使用过程中的内容都完整  

![image](https://github.com/user-attachments/assets/0de21836-92cb-4549-99aa-7d9268281035)
![image](https://github.com/user-attachments/assets/f42b838f-ec94-4e4d-b4fb-7fb1dd1f89fa)

以下内容是执行日志
```bash
python3.12  ./sql.py 
MySQL 中的表: ['activity', 'idp', 'inbox', 'memo', 'memo_organizer', 'memo_relation', 'migration_history', 'reaction', 'resource', 'system_setting', 'user', 'user_setting', 'webhook']
SQLite3 中的表: ['migration_history', 'system_setting', 'user', 'user_setting', 'memo', 'memo_organizer', 'memo_relation', 'resource', 'activity', 'storage', 'idp', 'inbox', 'webhook', 'reaction']
需要迁移的表: {'system_setting', 'inbox', 'reaction', 'user_setting', 'migration_history', 'resource', 'memo', 'memo_relation', 'memo_organizer', 'idp', 'user', 'webhook', 'activity'}
已清空 MySQL 中的 system_setting 表
已清空 MySQL 中的 inbox 表
已清空 MySQL 中的 reaction 表
已清空 MySQL 中的 user_setting 表
已清空 MySQL 中的 migration_history 表
已清空 MySQL 中的 resource 表
已清空 MySQL 中的 memo 表
已清空 MySQL 中的 memo_relation 表
已清空 MySQL 中的 memo_organizer 表
已清空 MySQL 中的 idp 表
已清空 MySQL 中的 user 表
已清空 MySQL 中的 webhook 表
已清空 MySQL 中的 activity 表

处理表: system_setting
MySQL system_setting 列: ['name', 'value', 'description']
SQLite3 system_setting 列: ['name', 'value', 'description']
公共列: {'description', 'name', 'value'}
system_setting 迁移完成，行数: 9
system_setting 行数对比: SQLite3=9, MySQL=9

处理表: inbox
MySQL inbox 列: ['id', 'created_ts', 'sender_id', 'receiver_id', 'status', 'message']
SQLite3 inbox 列: ['id', 'created_ts', 'sender_id', 'receiver_id', 'status', 'message']
公共列: {'message', 'status', 'sender_id', 'receiver_id', 'id', 'created_ts'}
inbox 迁移完成，行数: 7
inbox 行数对比: SQLite3=7, MySQL=7

处理表: reaction
MySQL reaction 列: ['id', 'created_ts', 'creator_id', 'content_id', 'reaction_type']
SQLite3 reaction 列: ['id', 'created_ts', 'creator_id', 'content_id', 'reaction_type']
公共列: {'content_id', 'creator_id', 'id', 'created_ts', 'reaction_type'}
reaction 迁移完成，行数: 3
reaction 行数对比: SQLite3=3, MySQL=2

处理表: user_setting
MySQL user_setting 列: ['user_id', 'key', 'value']
SQLite3 user_setting 列: ['user_id', 'key', 'value']
公共列: {'user_id', 'value', 'key'}
user_setting 迁移完成，行数: 12
user_setting 行数对比: SQLite3=12, MySQL=12

处理表: migration_history
MySQL migration_history 列: ['version', 'created_ts']
SQLite3 migration_history 列: ['version', 'created_ts']
公共列: {'created_ts', 'version'}
migration_history 迁移完成，行数: 8
migration_history 行数对比: SQLite3=8, MySQL=8

处理表: resource
MySQL resource 列: ['id', 'uid', 'creator_id', 'created_ts', 'updated_ts', 'filename', 'blob', 'type', 'size', 'memo_id', 'storage_type', 'reference', 'payload']
SQLite3 resource 列: ['id', 'creator_id', 'created_ts', 'updated_ts', 'filename', 'blob', 'type', 'size', 'memo_id', 'uid', 'storage_type', 'reference', 'payload']
公共列: {'blob', 'reference', 'storage_type', 'memo_id', 'filename', 'payload', 'size', 'uid', 'creator_id', 'id', 'updated_ts', 'created_ts', 'type'}
resource 迁移完成，行数: 64
resource 行数对比: SQLite3=64, MySQL=64
resource BLOB 数据大小对比: SQLite3=273305833 字节, MySQL=273305833 字节

处理表: memo
MySQL memo 列: ['id', 'uid', 'creator_id', 'created_ts', 'updated_ts', 'row_status', 'content', 'visibility', 'pinned', 'payload']
SQLite3 memo 列: ['id', 'creator_id', 'created_ts', 'updated_ts', 'row_status', 'content', 'visibility', 'uid', 'payload', 'pinned']
公共列: {'content', 'row_status', 'updated_ts', 'payload', 'uid', 'creator_id', 'id', 'visibility', 'created_ts', 'pinned'}
memo 迁移完成，行数: 118
memo 行数对比: SQLite3=118, MySQL=118

处理表: memo_relation
MySQL memo_relation 列: ['memo_id', 'related_memo_id', 'type']
SQLite3 memo_relation 列: ['memo_id', 'related_memo_id', 'type']
公共列: {'type', 'memo_id', 'related_memo_id'}
memo_relation 迁移完成，行数: 0
memo_relation 行数对比: SQLite3=0, MySQL=0

处理表: memo_organizer
MySQL memo_organizer 列: ['memo_id', 'user_id', 'pinned']
SQLite3 memo_organizer 列: ['memo_id', 'user_id', 'pinned']
公共列: {'pinned', 'memo_id', 'user_id'}
memo_organizer 迁移完成，行数: 11
memo_organizer 行数对比: SQLite3=11, MySQL=11

处理表: idp
MySQL idp 列: ['id', 'name', 'type', 'identifier_filter', 'config']
SQLite3 idp 列: ['id', 'name', 'type', 'identifier_filter', 'config']
公共列: {'name', 'config', 'identifier_filter', 'id', 'type'}
idp 迁移完成，行数: 0
idp 行数对比: SQLite3=0, MySQL=0

处理表: user
MySQL user 列: ['id', 'created_ts', 'updated_ts', 'row_status', 'username', 'role', 'email', 'nickname', 'password_hash', 'avatar_url', 'description']
SQLite3 user 列: ['id', 'created_ts', 'updated_ts', 'row_status', 'username', 'role', 'email', 'nickname', 'password_hash', 'avatar_url', 'description']
公共列: {'avatar_url', 'password_hash', 'role', 'row_status', 'description', 'username', 'id', 'updated_ts', 'created_ts', 'email', 'nickname'}
user 迁移完成，行数: 6
user 行数对比: SQLite3=6, MySQL=6

处理表: webhook
MySQL webhook 列: ['id', 'created_ts', 'updated_ts', 'row_status', 'creator_id', 'name', 'url']
SQLite3 webhook 列: ['id', 'created_ts', 'updated_ts', 'row_status', 'creator_id', 'name', 'url']
公共列: {'name', 'row_status', 'creator_id', 'id', 'updated_ts', 'created_ts', 'url'}
webhook 迁移完成，行数: 0
webhook 行数对比: SQLite3=0, MySQL=0

处理表: activity
MySQL activity 列: ['id', 'creator_id', 'created_ts', 'type', 'level', 'payload']
SQLite3 activity 列: ['id', 'creator_id', 'created_ts', 'type', 'level', 'payload']
公共列: {'payload', 'level', 'creator_id', 'id', 'created_ts', 'type'}
activity 迁移完成，行数: 18
activity 行数对比: SQLite3=18, MySQL=18

开始导出 MySQL 数据到备份文件: /root/dl/.memos/20250401/memos_db_backup.sql
备份完成，文件保存为: /root/dl/.memos/20250401/memos_db_backup.sql

迁移和备份完成！
```
有一处 （处理表: reaction
MySQL reaction 列: ['id', 'created_ts', 'creator_id', 'content_id', 'reaction_type']
SQLite3 reaction 列: ['id', 'created_ts', 'creator_id', 'content_id', 'reaction_type']
公共列: {'content_id', 'creator_id', 'id', 'created_ts', 'reaction_type'}
reaction 迁移完成，行数: 3
reaction 行数对比: SQLite3=3, MySQL=2）
少一个是少的点赞👍表情 我感觉影响不大就没处理了


