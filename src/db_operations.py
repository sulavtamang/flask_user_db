import sqlite3

class DBOperations:
    db_path = '../database/users.db'

    @staticmethod
    def make_db_conn():
        conn = sqlite3.connect(DBOperations.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    

    @staticmethod
    def table_exists(table_name):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT name 
                FROM sqlite_master
                WHERE type= 'table' AND name=?;
            ''', (table_name,))

            return bool(cursor.fetchone())
        

    @staticmethod
    def create_table(table_name):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name} (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT NOT NULL
                );
            ''')

            conn.commit()

    @staticmethod
    def clear_table(table_name):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute(f'''
                DELETE FROM {table_name};
            ''')
            conn.commit()

    
    @staticmethod
    def drop_table(table_name):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute(f'''
                DROP TABLE IF EXISTS {table_name}; 
            ''')
            conn.commit()
            
    
    @staticmethod
    def user_exists(name, address):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT 1 FROM users WHERE name = (?)
                AND address = (?)
                LIMIT 1;
            ''', (name, address))

            return bool(cursor.fetchone())
        
    
    @staticmethod
    def get_all_users():
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT name, address
                FROM users
            ''')

            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
        
    
    @staticmethod
    def get_user(name, address):
        if DBOperations.table_exists('users') and DBOperations.user_exists(name, address):
            with DBOperations.make_db_conn() as conn:
                cursor = conn.cursor()

                cursor.execute('''
                    SELECT name, address
                    FROM users
                    WHERE name = (?) AND address = (?)
                ''', (name, address))

                user_rows = cursor.fetchall()
                
                user_data = [dict(row) for row in user_rows]

                return user_data
            

    @staticmethod
    def insert_user(name, address):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()
        
            cursor.execute('''
                INSERT INTO users (name, address)
                VALUES (?, ?)
            ''', (name, address))
            conn.commit()
            
    
    @staticmethod
    def remove_user(name, address):
        with DBOperations.make_db_conn() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM users
                WHERE name=(?) AND address=(?)
            ''', (name, address))
            
            conn.commit()