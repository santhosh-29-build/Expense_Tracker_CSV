import csv
import secrets
import string
from pathlib import Path
from account import Account

class Service(Account):
    
    def login(id : int,password : str):
        file_path=Path(r"S:\2026\Data Science\Expense_Tracker\DB\RecordDB.csv")
        with open(file_path,"r",newline="") as file:
            reader=csv.DictReader(file)
            
            if(any(int(row["Id"])==id and row["Password"]==password for row in reader)):
                print("Success")
            else:
                print("Unsuccess")
            
    def credit(account : Account,amount : int):
        transaction_id=Service.generate_id(account.getId())
        type="credit"
        file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{account.getId()}.csv")
        with open(file_path,"a+",newline="") as file:
            writer=csv.DictWriter(file,fieldnames=["Transaction_Id","Credit/Debit","Amount","Balance"])
            reader = csv.DictReader(file)
            file.seek(0)
            last_record = list(reader)[-1]
            balance=int(last_record["Balance"])+amount
            account.setBalance(balance)
            data={"Transaction_Id":transaction_id,"Credit/Debit":type,"Amount":amount,"Balance":balance}
            writer.writerow(data)
        
    
    def generate_id(id : int):
        characters = string.ascii_letters + string.digits
        while True:
            new_id = ''.join(secrets.choice(characters) for _ in range(6))
            
            file_path=Path(rf"S:\2026\Data Science\Expense_Tracker\DB\{id}.csv")
            with open(file_path,"r",newline="") as file:
                reader=csv.DictReader(file)
                
                if(any(row["Transaction_Id"]==new_id for row in reader)):
                    pass
                else:
                    break
                
        return new_id
            
            
a=Account(101,"santhosh","san2905") 
b=Account(102,"sanjai","san3399")
Service.credit(a,11532)
                    