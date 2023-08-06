import os
import mysql.connector
from mysql.connector import Error

BATCH_SIZE = 1  # 每批导入的小说数量

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='bookdb',  # 替换为你的数据库名称
            user='username',      # 替换为你的数据库用户名
            password='123123',   # 替换为你的数据库密码
            charset='utf8mb4',
            connection_timeout=120
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(e)
    return connection

def import_txt_files(directory):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        
        novels = []
        batch_count = 0
        
        for filename in os.listdir(directory):
            if filename.endswith('.txt'):
                with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                    content = file.read()
                    novel_title = os.path.splitext(filename)[0]
                    author_id = 1
                    category_id = 1
                    rating = 3
                    
                    novels.append((novel_title, content, author_id, category_id, rating))
                    batch_count += 1
                    
                    if batch_count >= BATCH_SIZE:
                        insert_query = '''
                            INSERT INTO novels (novel_title, novel_content, author_id, category_id, rating)
                            VALUES (%s, %s, %s, %s, %s)
                        '''
                        cursor.executemany(insert_query, novels)
                        connection.commit()
                        batch_count = 0
                        novels = []
        
        if novels:  # 处理剩余未处理的小说
            insert_query = '''
                INSERT INTO novels (novel_title, novel_content, author_id, category_id, rating)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.executemany(insert_query, novels)
            connection.commit()
        
        cursor.close()
        connection.close()
        print('Imported .txt files to database')

if __name__ == '__main__':
    import_txt_files('小说TXT所在的目录')  # 替换为你的.txt文件所在目录的路径
