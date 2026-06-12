from base_db import BaseDB

class MemberDB(BaseDB):
    table_name = 'members'

    @classmethod
    def create_member(cls, data:dict):
        data['is_active'] = True
        data['total_borrows'] = 0
        id = cls.create(data)
        cls.get_connection().commit()
        return id

    @classmethod
    def get_all_members(cls):
        return cls.get_all()

    @classmethod
    def get_member_by_id(cls, id:int):
        return cls.get_by_id(id) or None

    @classmethod
    def update_member(cls, id:int, data:dict):
        updated = cls.update(id, data)
        cls.get_connection().commit()
        return updated

    @classmethod
    def deactivate_member(cls, id:int):
        updated = cls.update(id, {"is_active": False})
        cls.get_connection().commit()
        return updated

    @classmethod
    def activate_member(cls, id:int):
        updated = cls.update(id, {"is_active": False})
        cls.get_connection().commit()
        return updated

    @classmethod
    def increment_borrows(cls, id:int):
        connection = cls.get_connection()
        with connection.cursor() as cursor:
            cursor.execute(f"""UPDATE books SET total_borrows
                            = total_borrows + 1 WHERE id = {id}""")
            connection.commit()
            return cursor.rowcount > 0

    @classmethod
    def count_active_members(cls):
        return cls.count("is_active = TRUE")

    @classmethod
    def get_top_member(cls):
        with cls.get_connection().cursor() as cursor:
            cursor.execute("SELECT * FROM books ORDER BY total_borrows DESC LIMIT 1")
            return cursor.fetchall()