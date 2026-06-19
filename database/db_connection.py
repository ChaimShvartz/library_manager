import mysql.connector
from logs.config import logger

class ConnectionDB:
    def __init__(self):
        self.connect()

    def connect(self):
        self._connection = mysql.connector.connect(host='localhost', user='root',
         password='root')
    
    @property
    def connection(self):
        if not self._connection.is_connected():
            logger.warning('connection was lost, creating a new one')
            self.connect()
            self.create_database()
        return self._connection

    def create_database(self):
        with self.connection.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS library_db')
            cursor.execute('USE library_db')

    def create_tables(self):
        self.create_books_table()
        self.create_memers_table()

    def create_books_table(self):
        sql_create_books = """CREATE TABLE IF NOT EXISTS books(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        author VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'Non-Fiction',
                            'Science', 'History', 'Other') NOT NULL,
                        is_available BOOLEAN NOT NULL,
                        borrowed_by_member_id INT)
                    """
        with self.connection.cursor() as cursor:
            cursor.execute(sql_create_books)
        
    def create_memers_table(self):
        sql_create_members = """CREATE TABLE IF NOT EXISTS members(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        is_active BOOLEAN NOT NULL,
                        total_borrows INT NOT NULL)
                        """
        with self.connection.cursor() as cursor:
            cursor.execute(sql_create_members)

    def close(self):
        logger.info('closing connection')
        self.connection.close()

db = ConnectionDB()