from db_connection import ConnectionDB

class BaseDB:
    table_name= None

    @staticmethod
    def get_connection():
        return ConnectionDB.get_connection()

    @classmethod
    def get_all(cls):
        with cls.get_connection().cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {cls.table_name}")
            return cursor.fetchall()

    @classmethod
    def get_by_id(cls, id:int):
        with cls.get_connection().cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {cls.table_name} WHERE id = %s", (id,))
            return cursor.fetchall()

    @classmethod
    def create(cls, data:dict):
        keys = ', '.join(data)
        with cls.get_connection().cursor() as cursor:
            cursor.execute(f"""INSERT INTO {cls.table_name}(
                           {keys}) VALUES({'%s' * len(data)})""", list(data.values()))
            return cursor.lastrowid

    @classmethod
    def update(cls, id:int, data:dict):
        keys_list = [f'{key} = %s' for key in data]
        keys = ', '.join(keys_list)
        with cls.get_connection().cursor() as cursor:
            cursor.execute(f"""UPDATE {cls.table_name} SET {keys}
                            WHERE id = %s""", list(data.values()) + [id])
            return cursor.rowcount > 0

    @classmethod
    def delete(cls, id:int):
        with cls.get_connection().cursor() as cursor:
            cursor.execute(f"DELETE FROM {cls.table_name} WHERE id = %s", (id,))
            cls.connection.commit()
            return cursor.rowcount > 0
        
    @classmethod
    def count(cls, condition:str=None):
        sql_cmd = f"SELECT COUNT(*) AS amount FROM {cls.table_name}"
        if condition:
            sql_cmd += f" WHERE {condition}"
        with cls.get_connection().cursor() as cursor:
            cursor.execute(sql_cmd)
            return cursor.fetchall()