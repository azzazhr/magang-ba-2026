import pandas as pd

def search_comments(conn, keyword):
    sql = """SELECT c.comment_id, p.platform, c.published_at AS commented_at,
                c.text_original, p.text_content AS context_text
                FROM comments c JOIN posts p ON p.post_id = c.post_id
                WHERE LOWER(c.text_original) LIKE ?"""
    return pd.read_sql(sql, conn, params=[f"%{keyword.lower()}%"])
