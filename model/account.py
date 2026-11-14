import csv
from pathlib import Path

class account:
    def __init__(self,id:int,user_name:str,password:str):
        self.__id=id
        self.__user_name=user_name
        self.__password=password
        self.__balance=0
        
        self.record_DB()
        self.create_new_csv()
        
        
    def record_DB(self):
        file_path = r"S:\2026\Data Science\Expense_Tracker\DB\RecordDB.csv"
        id_exists = False
        with open(file_path, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                if row[0] == str(self.__id):
                    id_exists = True
                    break
            if not id_exists:
                with open(file_path, "a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        self.__id,
                        self.__user_name,
                        self.__password
                        ])
                    
        
    def create_new_csv(self):
        file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{self.__id}.csv")
        if not file_path.exists():
            with open(file_path,"w",newline="") as file:
                writer=csv.writer(file)
                writer.writerow(["Transaction_Id","Credit/Debit","Amount","Balance"])
        
    def getUserById(self):
        print(self.__id)
        print(self.__user_name)
        print(self.__password)
        print(self.__balance)
        


a=account(101,"santhosh","san2905")
a.getUserById()