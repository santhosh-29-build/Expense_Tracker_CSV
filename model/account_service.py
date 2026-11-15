import csv
import secrets
import string
import pandas as pd
from pathlib import Path
from model.account import Account

class Service(Account):
    
    def login(id : int,password : str):
        file_path=Path(r"S:\2026\Data Science\Expense_Tracker\DB\RecordDB.csv")
        with open(file_path,"r",newline="") as file:
            reader=csv.DictReader(file)
            
            if(any(int(row["Id"])==id and row["Password"]==password for row in reader)):
                print("Success")
                return True
            else:
                print("Unsuccess")
                
            
    def credit(id : int,amount : int):
        transaction_id=Service.generate_id(id)
        type="credit"
        file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{id}.csv")
        with open(file_path,"a+",newline="") as file:
            writer=csv.DictWriter(file,fieldnames=["Transaction_Id","Credit/Debit","Amount","Balance"])
            reader = csv.DictReader(file)
            
            file.seek(0)
            
            last_record=None
            amount=float(amount)
            for row in reader:
                last_record=row
                
            if last_record==None:
                balance=amount
            else:
                balance=float(last_record["Balance"])+amount
            data={"Transaction_Id":transaction_id,"Credit/Debit":type,"Amount":amount,"Balance":balance}
            writer.writerow(data)
            
            return True
            
            
            
    def debit(id : int,amount : int):
        transaction_id=Service.generate_id(id)
        type="debit"
        file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{id}.csv")
        with open(file_path,"a+",newline="") as file:
            writer=csv.DictWriter(file,fieldnames=["Transaction_Id","Credit/Debit","Amount","Balance"])
            reader = csv.DictReader(file)
            
            file.seek(0)
            
            last_record=None
            
            amount=float(amount)
            for row in reader:
                last_record=row
                
            if float(last_record["Balance"])<1000:
                print("No Transaction can be done Minimum Balance Needed")
                return False
            
            if float(last_record["Balance"])<amount:
                print("No Transaction can be done Minimum Balance Needed")
                return False
            
            if last_record==None:
                print("required Minimum Balance")
                return False
            else:
                balance=float(last_record["Balance"])-amount
            data={"Transaction_Id":transaction_id,"Credit/Debit":type,"Amount":amount,"Balance":balance}
            writer.writerow(data)
            
            return True
        
    
    def generate_id(id : int):
        characters = string.ascii_letters + string.digits
        while True:
            new_id = ''.join(secrets.choice(characters) for _ in range(15))
            
            file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{id}.csv")
            with open(file_path,"r",newline="") as file:
                reader=csv.DictReader(file)
                
                if(any(row["Transaction_Id"]==new_id for row in reader)):
                    pass
                else:
                    break
                
        return new_id
    
    def transaction_history(id : int):
        file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{id}.csv")
        df=pd.read_csv(file_path)
        return df
        
        
    def recent_transaction_history(id : int):
        file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{id}.csv")
        df=pd.read_csv(file_path)
        return df.tail()
        
    def register(id : int,user_name : str,password : str):
        file_path=Path(r"S:\2026\Data Science\Expense_Tracker\DB\RecordDB.csv")
        with open(file_path,"r",newline="") as file:
            reader=csv.DictReader(file)
            if(any(int(row["Id"])==id for row in reader)):
                return False
            else:
                a=Account(id,user_name,password)
                return True
    
    def account_info(id : int):
        file_path=Path(r"S:\2026\Data Science\Expense_Tracker\DB\RecordDB.csv")
        with open(file_path,"r",newline="") as file:
            reader=csv.DictReader(file)
            
            for row in reader:
                if row["Id"]==id:
                    return row
            
    def check_balance(user_id: int):
        file_path = Path(
            rf"S:\2026\Data Science\Expense_Tracker\DB\{user_id}.csv"
        )
        
        df = pd.read_csv(file_path)
        
        if df.empty:
            return 0
        
        last_record = df.iloc[-1]
        balance = float(last_record["Balance"])
        return balance