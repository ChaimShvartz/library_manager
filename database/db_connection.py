import mysql.connector

class ConnectionDB:
    def __init__(self):
        self.connect()
        self.create_books_table()
        self.create_memers_table()

    def connect(self):
        self._connection = mysql.connector.connect(host='localhost', user='root',
         password='root', database='library_db')
    
    @property
    def connection(self):
        if not self._connection.is_connected():
            self.connect()
        return self._connection

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

db = ConnectionDB()