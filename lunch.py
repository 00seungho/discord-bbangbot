import database

class lunch(database.con):
    def get_lunch(self):
        try:    
            conn,cur = self.connectDB()
            menu = "김치찌개"
            sql = "SELECT * FROM lunch ORDER BY RAND() LIMIT 1;"
            self.cur.execute(sql)
            row = self.cur.fetchone()
            if row:
                menu = row[0]
            return menu
        except Exception as e:
            print(f"Error: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
