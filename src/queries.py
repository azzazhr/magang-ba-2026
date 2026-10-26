import pandas as pd

BASE_SQL = """
SELECT c.comment_id, p.platform, c.published_at AS commented_at,
       c.text_content AS text_original, 
       p.text_content AS context_text
FROM comments c 
JOIN posts p ON p.post_id = c.post_id
"""

def get_category_column(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(posts);")
    columns = [col[1] for col in cursor.fetchall()]
    for col_name in ['content_category', 'category', 'post_category', 'kategori', 'topic']:
        if col_name in columns:
            return col_name
    return None

def filter_comments(conn, platforms=None, date_from=None, date_to=None, categories=None, keyword=None):
    where, params = ["1=1"], []
    
    if platforms:
        where.append(f"p.platform IN ({','.join(['?'] * len(platforms))})")
        params += platforms
        
    if date_from:
        where.append("date(c.published_at) >= date(?)")
        params.append(str(date_from))
        
    if date_to:
        where.append("date(c.published_at) <= date(?)")
        params.append(str(date_to))
        
    if categories:
        cat_col = get_category_column(conn)
        if cat_col:
            where.append(f"p.{cat_col} IN ({','.join(['?'] * len(categories))})")
            params += categories
            
    if keyword:
        where.append("LOWER(c.text_content) LIKE ?")
        params.append(f"%{keyword.lower()}%")
        
    sql = BASE_SQL + " WHERE " + " AND ".join(where)
    
    return pd.read_sql(sql, conn, params=params)
