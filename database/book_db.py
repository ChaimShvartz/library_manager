from database.base_db import BaseDB

class BookDB(BaseDB):
    
    def create_book(self, data:dict) -> int:
        data['is_available'] = True
        data['borrowed_by_member_id'] = None
        return self.create(data)

    def get_all_books(self) -> list:
        return self.get_all()
    
    def get_book_by_id(self, id:int) -> dict | None:
        return self.get_by_id(id)

    def update_book(self, id:int, data:dict) -> bool:
        return self.update(id, data)
    
    def set_availability(self, id:int, val:bool, member_id:int=None) -> bool:
        data = {"is_available": val, "borrowed_by_member_id": member_id}
        return self.update(id, data)

    def count_total_books(self) -> int:
        return self.count()

    def count_available_books(self) -> int:
        return self.count(" WHERE is_available = true")

    def count_borrowed_books(self) -> int:
        return self.count(" WHERE is_available = false")

    def count_by_genre(self) -> list[dict]:
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT genre, COUNT(*) AS count FROM books GROUP BY genre") 
            return cursor.fetchall()

    def count_active_borrows_by_member(self, member_id:int) -> int:
        return self.count(f" WHERE borrowed_by_member_id = {member_id}")['count']
    
book_db = BookDB('books')