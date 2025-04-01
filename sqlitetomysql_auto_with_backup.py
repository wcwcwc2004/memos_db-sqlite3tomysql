import sqlite3
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# SQLite3 连接
sqlite_db_path = '/sqlite3path/memos_prod.db'
sqlite_conn = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_conn.cursor()

# MySQL 连接
mysql_config = {
    'host': 'localhost',
    'user': 'mysqlusername',
    'password': 'mysqlpassowrd',
    'database': 'memos_db'
}

try:
    mysql_conn = mysql.connector.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor()
except Error as e:
    print(f"连接 MySQL 失败: {e}")
    exit()

# 获取 MySQL 中的所有表
mysql_cursor.execute("SHOW TABLES;")
mysql_tables = [row[0] for row in mysql_cursor.fetchall()]
print("MySQL 中的表:", mysql_tables)

# 获取 SQLite3 中的所有表
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
sqlite_tables = [row[0] for row in sqlite_cursor.fetchall() if row[0] != 'sqlite_sequence']
print("SQLite3 中的表:", sqlite_tables)

# 找到公共表（需要迁移的表）
common_tables = set(mysql_tables).intersection(set(sqlite_tables))
print("需要迁移的表:", common_tables)

# 需要转换时间戳的列
timestamp_columns = {'created_ts', 'updated_ts'}

# 迁移数据
for table_name in common_tables:
    print(f"\n处理表: {table_name}")
    
    # 获取 MySQL 表结构
    mysql_cursor.execute(f"SHOW COLUMNS FROM {table_name};")
    mysql_columns = [row[0] for row in mysql_cursor.fetchall()]
    print(f"MySQL {table_name} 列:", mysql_columns)
    
    # 获取 SQLite3 表结构
    sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
    sqlite_columns = [col[1] for col in sqlite_cursor.fetchall()]
    print(f"SQLite3 {table_name} 列:", sqlite_columns)
    
    # 找到公共列
    common_columns = set(mysql_columns).intersection(set(sqlite_columns))
    if not common_columns:
        print(f"表 {table_name} 无公共列，跳过")
        continue
    print(f"公共列:", common_columns)
    
    # 从 SQLite3 读取数据
    sqlite_cursor.execute(f"SELECT {','.join(common_columns)} FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    # 处理时间戳列，转换为 MySQL DATETIME 格式
    processed_rows = []
    for row in rows:
        row_dict = dict(zip(common_columns, row))
        for col in timestamp_columns & common_columns:
            if row_dict[col] is not None:
                row_dict[col] = datetime.fromtimestamp(row_dict[col]).strftime('%Y-%m-%d %H:%M:%S')
        processed_rows.append(tuple(row_dict[col] for col in common_columns))
    
    # 构造插入语句
    placeholders = ','.join(['%s'] * len(common_columns))
    safe_columns = [f"`{col}`" if col in ['key', 'blob'] else col for col in common_columns]
    insert_query = f"INSERT IGNORE INTO {table_name} ({','.join(safe_columns)}) VALUES ({placeholders})"
    
    # 插入数据到 MySQL
    try:
        mysql_cursor.executemany(insert_query, processed_rows)
        mysql_conn.commit()
        print(f"{table_name} 迁移完成，行数: {len(processed_rows)}")
    except Error as e:
        print(f"迁移 {table_name} 数据失败: {e}")

# 导出 MySQL 数据到 SQL 文件
backup_file = '/root/dl/.memos/20250401/memos_db_backup.sql'
print(f"\n开始导出 MySQL 数据到备份文件: {backup_file}")

with open(backup_file, 'w', encoding='utf-8') as f:
    # 写入数据库创建语句（可选）
    f.write(f"DROP DATABASE IF EXISTS `memos_db`;\n")
    f.write(f"CREATE DATABASE `memos_db`;\n")
    f.write(f"USE `memos_db`;\n\n")
    
    for table_name in mysql_tables:
        # 获取表创建语句
        mysql_cursor.execute(f"SHOW CREATE TABLE {table_name};")
        create_table_stmt = mysql_cursor.fetchone()[1]
        f.write(f"{create_table_stmt};\n\n")
        
        # 获取表数据
        mysql_cursor.execute(f"SELECT * FROM {table_name};")
        rows = mysql_cursor.fetchall()
        if rows:
            # 获取列名
            mysql_cursor.execute(f"SHOW COLUMNS FROM {table_name};")
            columns = [row[0] for row in mysql_cursor.fetchall()]
            safe_columns = [f"`{col}`" for col in columns]  # 所有列名加反引号
            
            # 写入 INSERT 语句
            f.write(f"INSERT INTO `{table_name}` ({','.join(safe_columns)}) VALUES\n")
            values = []
            for row in rows:
                formatted_row = []
                for val in row:
                    if val is None:
                        formatted_row.append("NULL")
                    elif isinstance(val, (int, float)):
                        formatted_row.append(str(val))
                    elif isinstance(val, bytes):
                        formatted_row.append(f"X'{val.hex()}'")  # BLOB 数据用十六进制
                    else:
                        formatted_row.append(f"'{str(val).replace('\'', '\\\'')}'")  # 转义单引号
                values.append(f"({','.join(formatted_row)})")
            f.write(",\n".join(values) + ";\n\n")
        else:
            f.write(f"-- 表 `{table_name}` 无数据\n\n")

print(f"备份完成，文件保存为: {backup_file}")

# 关闭连接
sqlite_conn.close()
mysql_conn.close()
print("\n迁移和备份完成！")
