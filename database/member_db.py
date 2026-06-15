from database.base_db import BaseDB

class MemberDB(BaseDB):

    def create_member(self, data:dict) -> int:
        data['is_active'] = True
        data['total_borrows'] = 0
        return self.create(data)

    def get_all_members(self) -> list[dict]:
        return self.get_all()

    def get_member_by_id(self, id:int) -> dict | None:
        return self.get_by_id(id)

    def update_member(self, id:int, data:dict) -> bool:
        return self.update(id, data)

    def deactivate_member(self, id:int) -> bool:
        return self.update(id, {"is_active": False})

    def activate_member(self, id:int) -> bool:
        return self.update(id, {"is_active": True})

    @staticmethod
    def increment_borrows(id:int) -> bool:
        connection = __class__().connection
        with connection.cursor() as cursor:
            cursor.execute("""UPDATE books SET total_borrows
                            = total_borrows + 1 WHERE id = %s""", (id,))
            connection.commit()
            return cursor.rowcount > 0

    def count_active_members(self) -> int:
        return self.count(" WHERE is_active = true")

    def get_top_member(self) -> list[dict]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("""SELECT id AS member_id, total_borrows AS borrowed
            FROM members WHERE total_borrows = (SELECT MAX(total_borrows) FROM books )""")
            return cursor.fetchall()
        
member_db = MemberDB('members')