import mysql.connector

class ConnectionDB:

    @staticmethod
    def connect():
        return mysql.connector.connect(host='localhost', user='root', password='root', database='library_db')
    
    @staticmethod
    def get_connection():
        global connection
        if not connection.is_connected():
            connection = ConnectionDB().connect()
        return connection

    @staticmethod
    def create_tables():
        sql_create_books = """CREATE TABLE IF NOT EXISTS books(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(50) NOT NULL,
                        auther VARCHAR(50) NOT NULL,
                        genre ENUM('Fiction', 'Non-Fiction',
                            'Science', 'History', 'Other') NOT NULL,
                        is_available BOOLEAN DEFAULT TRUE,
                        borrowed_by_member_id INT DEFAULT NULL) 
                    """
        sql_create_members = """CREATE TABLE IF NOT EXISTS members(
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        total_borrows INT DEFAULT 0)
                        """
        with ConnectionDB.get_connection().cursor() as cursor:
            cursor.execute(sql_create_books)
            cursor.execute(sql_create_members)

connection = ConnectionDB.connect()