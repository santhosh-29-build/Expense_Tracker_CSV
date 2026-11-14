import csv
from pathlib import Path

class account:
    def __init__(self,id:int,user_name:str,password:str):
        self.__id=id
        self.__user_name=user_name
        self.__password=password
        self.__balance=0
        
        self.create_new_csv()
        
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