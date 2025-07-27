import os 
    
class Database:
    
    dir = "/tmp/ga_tmp/"

    def __init__(self):
        if os.path.exists(self.dir) == False:
            os.makedirs(self.dir) 
    
        
    def add_logfile(self,filename,data):
        with open(f"{self.dir}/{filename}" , 'wb') as file: 
            file.write(data)
        
    def id_exists(self,id):
        return os.path.isfile(f"{self.dir}/{id}")
        
    def get_logfile(self,id ):    
        
        with  open(f"{self.dir}/{id}" , 'r') as file: 
            return file.read()   
            


if __name__ == '__main__':
    
    #with open("/home/kiwi/logs/nasha-set_access.log-20250718", 'r') as f:
    with open("/home/kiwi/logs/test.log", 'r') as f:
        db = Database()
        id = "sxgsdgdfgsdg"[0:20]
        assert db.id_exists(id) == False
        data = f.read()
        db.add_logfile(id,data)
        assert db.id_exists(id) == True
        data_res = db.get_logfile(id)
        
        if data_res  == data and db.id_exists(id):
            print("OK")
            
        os.remove("/tmp/ga_tmp/sxgsdgdfgsdg")