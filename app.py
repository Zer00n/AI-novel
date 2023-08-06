from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='bookdb',  # 替换为你的数据库名称
            user='username',      # 替换为你的数据库用户名
            password='123123'   # 替换为你的数据库密码
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(e)
    return connection

@app.route('/')

def index():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        # 获取分类列表
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        
        # 处理分类筛选
        selected_category = request.args.get('category')
        if selected_category:
            query = '''
                SELECT n.novel_id, n.novel_title, n.rating, n.upload_date
                FROM novels n
                WHERE n.category_id = %s
            '''
            cursor.execute(query, (selected_category,))
        else:
            query = '''
                SELECT n.novel_id, n.novel_title, n.rating, n.upload_date
                FROM novels n
            '''
            cursor.execute(query)
    


        novels = cursor.fetchall()
        # 格式化日期为年月日格式
        for novel in novels:
            novel['upload_date'] = novel['upload_date'].strftime('%Y-%m-%d')
        
        cursor.close()
        connection.close()
        return render_template('index.html', categories=categories, novels=novels)


@app.route('/add_novel', methods=['GET', 'POST'])
def add_novel():
    if request.method == 'POST':
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            novel_title = request.form['title']
            novel_content = request.form['content']
            author_id = int(request.form['author'])
            category_id = int(request.form['category'])
            rating = int(request.form['rating'])
            
            insert_query = '''
                INSERT INTO novels (novel_title, novel_content, author_id, category_id, rating)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(insert_query, (novel_title, novel_content, author_id, category_id, rating))
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('index'))
    
    # Fetch authors and categories for dropdowns
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM authors')
        authors = cursor.fetchall()
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('add_novel.html', authors=authors, categories=categories)
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        
        if request.method == 'POST':
            keyword = request.form.get('keyword', '')
            search_query = '''
                SELECT n.novel_id, n.novel_title, n.novel_content, n.rating, n.category_id, a.author_name, c.category_name, n.upload_date
                FROM novels n
                JOIN authors a ON n.author_id = a.author_id
                JOIN categories c ON n.category_id = c.category_id
                WHERE n.novel_title LIKE %s
            '''
            cursor.execute(search_query, ('%' + keyword + '%',))
            novels = cursor.fetchall()
            cursor.close()
            connection.close()
            return render_template('search_novel.html', novels=novels)

        cursor.close()
        connection.close()
    
    return render_template('search_novel.html', novels=[])

@app.route('/read_novel/<int:novel_id>', methods=['GET', 'POST'])
def read_novel(novel_id):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = '''
            SELECT n.novel_id, n.novel_title, n.novel_content, n.rating, n.category_id, a.author_name, c.category_name, n.upload_date
            FROM novels n
            JOIN authors a ON n.author_id = a.author_id
            JOIN categories c ON n.category_id = c.category_id
            WHERE n.novel_id = %s
        '''
        cursor.execute(query, (novel_id,))
        novel = cursor.fetchone()

        # 获取分类列表
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()

        if request.method == 'POST':
            if 'rating' in request.form:
                # 处理修改评分表单提交
                new_rating = int(request.form['rating'])
                update_rating_query = '''
                    UPDATE novels
                    SET rating = %s
                    WHERE novel_id = %s
                '''
                cursor.execute(update_rating_query, (new_rating, novel_id))
                connection.commit()
                novel['rating'] = new_rating
            elif 'new_category' in request.form:
                # 处理修改分类表单提交
                new_category_id = int(request.form['new_category'])
                update_category_query = '''
                    UPDATE novels
                    SET category_id = %s
                    WHERE novel_id = %s
                '''
                cursor.execute(update_category_query, (new_category_id, novel_id))
                connection.commit()
                novel['category_id'] = new_category_id

        # 将小说内容解码为字符串
        novel_content = novel['novel_content'].decode('utf-8')

        cursor.close()
        connection.close()

        # 更新 novel 字典中的小说内容为解码后的字符串
        novel['novel_content'] = novel_content

        return render_template('read_novel.html', novel=novel, categories=categories)

if __name__ == '__main__':
    app.run(debug=True)
