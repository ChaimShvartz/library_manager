from database.base_db import BaseDB

class BookDB(BaseDB):
    table_name = 'books'
    
    @classmethod
    def create_book(cls, data:dict) -> int:
        data['is_available'] = True
        data['borrowed_by'] = None
        id = cls.create(data)
        cls.get_connection().commit()
        return id

    @classmethod
    def get_all_books(cls) -> list:
        return cls.get_all()
    
    @classmethod
    def get_book_by_id(cls, id:int) -> list:
        return cls.get_by_id(id)

    @classmethod
    def update_book(cls, id:int, data:dict) -> bool:
        updated = cls.update(id, data)
        cls.get_connection().commit()
        return updated
    
    @classmethod
    def set_availability(cls, id:int, val:bool, member_id:int=None) -> bool:
        data = {"is_available": True, "borrowed_by_member_id": member_id}
        updated = cls.update(id, data)
        cls.get_connection().commit()
        return updated

    @classmethod
    def count_total_books(cls) -> int:
        return cls.count()

    @classmethod
    def count_available_books(cls):
        return cls.count("is_available = TRUE")

    @classmethod
    def count_borrowed_books(cls):
        return cls.count("is_available = FALSE")

    @classmethod
    def count_by_genre(cls):
        with cls.get_connection().cursor(dictionary=True) as cursor:
            cursor.execute("SELECT genre, COUNT(*) AS amount FROM books GROUP BY genre") 
            return cursor.fetchall()

    @classmethod
    def count_active_borrows_by_member(cls, member_id:int):
        return cls.count(f"borrowed_by_member_id = {member_id}")
    