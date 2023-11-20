select_all_articles = """
        SELECT *
        FROM articles
        """
select_article_by_id = """
        SELECT *
        FROM articles
        WHERE id = %s
        """
select_user_login = """
        SELECT * 
        FROM users 
        WHERE username = %s
        """

insert_user_data = """
        INSERT INTO users(name, email, username, password) 
        VALUES(%s, %s, %s, %s)
        """
insert_new_article = """
        insert into articles(title, body, author)
        values(%s, %s, %s)
        """

update_article = """
        UPDATE articles 
        SET title = %s, body = %s 
        WHERE id = %s
        """

delete_article_by_id = """
        DELETE FROM articles 
        WHERE id = %s
        """