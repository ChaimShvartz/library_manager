from database.db_connection import db

class BaseDB:
    def __init__(self, table_name):
        self.db = db
        self.table_name = table_name

    @property
    def connection(self):
        return self.db.connection

    def get_all(self):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            return cursor.fetchall()

    def get_by_id(self, id:int):
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (id,))
            return cursor.fetchone()

    def create(self, data:dict):
        connection = self.connection
        keys = ', '.join(data)
        place_holders = ', '.join(['%s'] * len(data))
        with connection.cursor() as cursor:
            cursor.execute(f"""INSERT INTO {self.table_name}(
                           {keys}) VALUES({place_holders})""", [*data.values()])
            connection.commit()
            return cursor.lastrowid

    def update(self, id:int, data:dict):
        connection = self.connection
        keys_list = [f'{key} = %s' for key in data]
        keys = ', '.join(keys_list)
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE {self.table_name} SET {keys}
                            WHERE id = %s""", [*data.values(), id])
            connection.commit()
            return cursor.rowcount > 0
        
    def count(self, condition:str=None):
        condition = condition or ''
        sql_cmd = f"SELECT COUNT(*) AS count FROM {self.table_name}" + condition
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql_cmd)
            return cursor.fetchone()