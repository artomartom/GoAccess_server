import sqlite3

def store_and_retrieve_binary():
    # Connect to database
    conn = sqlite3.connect('binary_db.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS files
                      (name TEXT, content BLOB)''')
    
    # Sample binary data - could be an image, PDF, etc.
    file_content = b'\x89PNG\x0D\x0A\x1A\x0A\x00\x00\x00\x0DIHDR...'  # truncated example
    
    # Store binary data
    cursor.execute("INSERT INTO files (name, content) VALUES (?, ?)", 
                   ('sample.png', file_content))
    
    # Retrieve binary data
    cursor.execute("SELECT content FROM files WHERE name = ?", ('sample.png',))
    retrieved_data = cursor.fetchone()[0]
    
    # Verify the data
    print("Original equals retrieved:", file_content == retrieved_data)
    
    # Clean up
    conn.commit()
    conn.close()

    
class Database:
    

    def __init__(self):
        self.conn = sqlite3.connect('log_files.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS log_files
                      (id TEXT, data BLOB)''')
        
    def  __del__(self):
        self.conn.commit()
        self.conn.close()
        
    def add_logfile(self,filename,data):
        self.cursor.execute("INSERT INTO log_files (id, data) VALUES (?, ?)", 
                   (filename, data))
        
    def id_exists(self,id):
        self.cursor.execute("SELECT COUNT(*) FROM log_files WHERE id = ?", (id,))
        res = self.count = self.cursor.fetchone()[0]
        assert res == 1
        return res == 1
        
    def get_logfile(self,id ):    
        self.cursor.execute("SELECT data FROM log_files WHERE id = ?", (id,))
        return  self.cursor.fetchone()[0]


if __name__ == '__main__':
    db = Database()
    id = "swpeitjfguisaaasd"
    data = "rpwsigjsoigjpifsjdg"
    db.add_logfile(id,data)
    db.id_exists(id)
    data_res = db.get_logfile(id)  
    
    if data_res == data and db.id_exists(id):
        print("OK")