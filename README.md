# AI-novel
起因是一个愿意用kindle阅读玄幻小说的朋友随口一说，然后计划利用ChatGPT，以问答的形式，开发一个小说阅读网站，并具备一些简单的功能，作为练手。
通过Kindle的浏览器可以访问即可。

基于python3.11
运行：
**python app.py** 即可通过浏览器打开 127.0.0.1:5000 访问。
**python import.py** 用来导入本地硬盘中txt格式的小说。

录入功能没有详细做，只是个Demo，目前可以正常访问，并具备简单的筛选、搜索功能，页面写了CSS做了简单的优化。

以下是数据库的表结构
```
CREATE TABLE Authors (
    author_id INT PRIMARY KEY AUTO_INCREMENT,
    author_name VARCHAR(255)
);

CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(255)
);

CREATE TABLE Novels (
    novel_id INT PRIMARY KEY AUTO_INCREMENT,
    novel_title VARCHAR(255),
    novel_content MEDIUMTEXT,
    author_id INT,
    category_id INT,
    rating INT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES Authors(author_id),
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);
```
