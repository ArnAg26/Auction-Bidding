# Project Title   : Auction Bidding System
# Version           : 1.0 2020-2021
# Developed By  : Krish Chugh and Arnav Agarwal
# Guide              : Ms. Hema Jain
# Last Updated On   : 2021-01-28

import random
import MySQLdb


db=MySQLdb.connect(host="localhost",user="root",password="ArnaV2602")
MyCur=db.cursor()

try:
   MyCur.execute("Create Database Auct")
   MyCur.execute("Use Auct")
except:    
   MyCur.execute("Use Auct")


    
try:
   MyCur.execute("Create Table Bidders(ID INTEGER(4), NAME CHAR(24) NOT NULL, AGE INTEGER(4) NOT NULL, USERNAME VARCHAR(25) PRIMARY KEY, PASSWORD VARCHAR(10) NOT NULL, QTY INTEGER(6),TOTAL_AMOUNT INTEGER(10), DOP DATE, EMAIL VARCHAR(40), MOBILE VARCHAR(11,UNIQUE (ID)) )")
except:
   print("Table already exists")  
  
  

'''''''''''''''''''''''''''''''''''''''''
To add a bidder to the list 
'''''''''''''''''''''''''''''''''''''''''

def Add_Bidder():
    biddername=input("Enter name of bidder")
    choice = 'Y'
    Z='True'
    while choice == 'Y' or choice == 'y':
          bid_username=input("Enter username of bidder (The username can only be a combination of alphabets, numbers and underscores without any spaces)")
          S = "SELECT * FROM BIDDERS WHERE USERNAME = '" + bid_username + "'"
          N = MyCur.execute(S)
          if N>0:
             print("Username already taken. Please try again!")
          else:
             age = int(input("Enter age of bidder"))
             if age > 18:
                password=input("Enter password")
                bidder_id = random.randint(100,1000) #check and add validation
                email = input("Enter you email id")
                mobile = input("Enter your mobile number")
                try:
                   MyCur.execute("CREATE TABLE "+bid_username+"(ID INTEGER(2) PRIMARY KEY,NAME CHAR(24) NOT NULL, BASE_PRICE INTEGER(10), BID_PRICE INTEGER(10), CATEGORY CHAR(10), DOP DATE, BILL_PAID CHAR(5))")
                   print("Table created")
                   MyCur.execute("INSERT INTO BIDDERS VALUES("+str(bidder_id)+",'"+biddername+"',"+str(age)+",'"+bid_username+"','"+password+"',0,0,NULL,'"+email+"','"+mobile+"')")
                   print("Bidder added")
                   db.commit()
                except:
                   MyCur.execute("SHOW COLUMNS FROM "+bid_username)
                   R=MyCur.fetchall()
                   for r in R:
                      print(r)
             else:
                print("Sorry, you are under age for bidding!")
          choice = input("Do you want to add another bidder(Y/N)?") 
			
 
 
'''''''''''''''''''''''''''''''''''''''''
To upload any item for bidding
'''''''''''''''''''''''''''''''''''''''''  

def Upload_Item():
   try:
       MyCur.execute("Create Table Items(ID INTEGER(4) PRIMARY KEY,NAME CHAR(24) NOT NULL, CATEGORY CHAR(20), BASE_PRICE INTEGER(10) NOT NULL,BID_AMOUNT  INTEGER(10), STATUS CHAR(5), DOP DATE, BUYER CHAR(20),UNIQUE (ID))")
   except:
       print("Table already exists")
   choice = 'Y'   
   while choice == 'Y' or choice == 'y':
        Id=input("Enter the Id")
    
        #S = "SELECT * FROM Items WHERE ID ="+Id
        N = MyCur.execute("SELECT * FROM Items WHERE ID ="+Id)
        if N>0:
            print("ID already taken")
            break
        else:  
           item=input("Enter the name of item")
           category = input ("Enter the item's category")
           base_price=input("Enter base price")
     #Incrementval=input("Enter the increment val")
           status= "Open"
           SQL="INSERT INTO ITEMS VALUES("+Id+",'"+item+"','"+category+"',"+base_price+",NULL,'"+status+"',NULL,NULL)"
           MyCur.execute(SQL)
           db.commit()
           choice = input("Do you want to upload another item(Y/N)?") 
           
     
     
'''''''''''''''''''''''''''''''''
To search any item
'''''''''''''''''''''''''''''''''

def SearchItem(a='ITEMS'):
    type = input("Do you want to search on item ID or name(ID/NAME)?")
    if type == "ID":
        S=input("Enter Id of item to search for")
        SQL="SELECT * FROM "+a+" WHERE ID="+S+""
    elif type == "NAME":
        S=input("Enter Name of item to search for")
        SQL="SELECT * FROM "+a+" WHERE NAME='"+S+"'"
    N=MyCur.execute(SQL)
    if N>0:
        MyCur.execute(SQL)
        R=MyCur.fetchone()
        for i in R:
            print(i,end = "   |   ")
    else:
        print("Result not Found")

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
To search any bidder and view items purchased by them
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#>>>>This is the function I have added<<<<

def ViewBidder(a="BIDDERS"):
    type=(input("Do you want to search on bidder ID or name(ID/NAME)?")).upper()
    if type=="ID":
      S=input("Enter Id of bidder to search for")
      SQL="SELECT * FROM "+a+" WHERE ID="+S+""
    elif type == "NAME":
        S=input("Enter Name of bidder to search for")
        SQL="SELECT * FROM "+a+" WHERE NAME='"+S+"'"
    N=MyCur.execute(SQL)
    if N>0:
        MyCur.execute(SQL)
        R=MyCur.fetchone()
        bid_username=R[3]
        S="SELECT * FROM "+bid_username+""
        MyCur.execute(S)
        H=MyCur.fetchall()
        for i in R:
            print(i,end = "   |   ")
        for j in H:
           print(j)
    else:
        print("Result not Found")
   
   
'''''''''''''''''''''''''''''''''''''''''
To view any item under a certain category
'''''''''''''''''''''''''''''''''''''''''

def View(status = 'Open'):
    cat = input("Enter the category of the items that you to view/bid - Artwork, Antiques, Furniture, Electronics")
    SQL = "SELECT * FROM ITEMS WHERE CATEGORY = '"+cat+"' AND STATUS='"+status+"'" 
    N = MyCur.execute(SQL)
    if N>0:
        MyCur.execute(SQL)
        R=MyCur.fetchall()
        for i in R:
            print (i)
        return True
    else:
        print("No items for the searched criteria")
        return False
 

 
'''''''''''''''''''''''''''''''''''''''''
To initiate the process of bidding
'''''''''''''''''''''''''''''''''''''''''   
        
def Bidding():
    A = View('Open')
    if A is True:
        I=input("Enter ID of item to bid for")
        SQL="SELECT * FROM ITEMS WHERE ID="+I+" AND STATUS = 'Open'"
        N=MyCur.execute(SQL)
        if N>0:
            R=MyCur.fetchone()
            print("Item ID:     "+R[0])
            print("Item Name:   "+R[1])
            print("Category:    "+R[2])
            print("Base Price:  "+R[3])
            print("Start Bidding")
            print("Opening Bid: "+R[3])
            choice="Y"
            latest_bid = R[3]
            B=0
            while choice=='Y' or choice=='y':
                try: 
                    bid_username=input("Enter the username of the bidder")
                    bid_user_password=input("Enter the password of the bidder")
                    A = "SELECT * FROM BIDDERS WHERE USERNAME = '"+bid_username+"'"
                    MyCur.execute(A)
                    P = MyCur.fetchone()
                    if P[4]==bid_user_password:
                        print("The password entered is correct. Welcome, Mr./Ms. "+P[1]+"!")
                        bid_amt=int(input("Enter your bidding amount"))
                        if bid_amt<=latest_bid:
                            print("The bid amount entered is lesser than or equal to the latest bid! Please try again.")
                        else:
                            print("Latest bid by "+bid_username+" for "+bid_amt)
                            latest_bidder = bid_username
                            latest_bid = bid_amt 
                            B+=1
                    else: 
                        print("The password entered is incorrect. Please try again!") 
                except:
                    print("The username entered does not exists!")
                choice = input("Do you want to continue bidding?(Y/N)")           
            if B>0: 
                print("Item "+R[1]+" sold for "+latest_bid+" to "+latest_bidder)
                A = "UPDATE ITEMS SET STATUS = 'Closed', DOP = CURDATE(), BUYER = '"+P[1]+"' WHERE ID="+I
                MyCur.execute(A)
                A = "UPDATE BIDDERS SET QTY=QTY+1, TOTAL_AMOUNT=TOTAL_AMOUNT+"+latest_bid+", DOP=CURDATE()"
                MyCur.execute(A)
                A = "INSERT INTO " + latest_bidder + " VALUES(" + R[0] + ", '" + R[1] + "', " + R[3] + ", " + latest_bid + ", '" + R[2] + "', CURDATE(), 'NO'"
                MyCur.execute(A)
                db.commit()
            elif B==0: 
                print("Item "+R[1]+" not sold!")
        else:
            print("Item not available for bidding!")
    else:
        print("Please try again!")
  
      

'''''''''''''''''''''''''''''''''''''''''
To generate a bill for final payment
'''''''''''''''''''''''''''''''''''''''''
      
def Generate_Bill():
    username = input("Enter the username for which the payment has to be made")
    attempts = 0
    var = 'True'
    while var=='True':
        password = input("Enter the password associated to the entered username")
        S = "SELECT * FROM BIDDERS WHERE USERNAME = '"+username+"'"
        MyCur.execute(S)
        P = MyCur.fetchone()
        if P[4]==password:
            print("The password entered is correct. Welcome, Mr/Ms "+P[1]+"!")
            print("The quantity of items you purchased is: "+P[5])
            print("The total amount that you need to pay is Rs."+P[6])
            mode = input("What will be the mode of payment(Credit Card/Debit Card/Mobile Wallets/Amazon Pay)?")
            A = "UPDATE BIDDERS SET QTY = 0, TOTAL_AMOUNT = 0, DOP = CURDATE()"
            MyCur.execute(A)
            A = "UPDATE "+username+" SET MODE_OF_PAYMENT = "+mode+", BILL_PAID = 'Yes' WHERE BILL_PAID = 'No'"
            MyCur.execute(A)
            db.commit()
            print("The payment has been done. Thank you Mr./Ms. "+P[1]+" for shopping with us!")
            var='False'
    else:
        print("The password entered is wrong!")
        attempts+=1
        if attempts==3:
            print("The number of wrong password attempts has been exhausted. Please try again after some time!")
            var = 'False'
          
          
          
'''''''''''''''''''''''''''''''''''''''''
To remove any items from the cart
''''''''''''''''''''''''''''''''''''''''' 
 
def Remove_from_Cart():
    username = input("Enter the username for which the cart has to be modified.")
    attempts = 0
    var = 'True'
    while var == 'True':
        password = input("Enter the password associated to the entered username")
        S = "SELECT * FROM BIDDERS WHERE USERNAME = '"+username+"'"
        MyCur.execute(S)
        P = MyCur.fetchone()
        if P[4]==password:
            print("The password entered is correct. Welcome, Mr/Ms "+P[1]+"!")
            SQL = "SELECT * FROM "+username+" WHERE BILL_PAID  = 'NO'"
            MyCur.execute(SQL)
            R = MyCur.fetchall()
            for i in R: 
                print(i)
            item_id = int(input("Please enter the ID of the item that you need to remove."))
            SQL = "SELECT * FROM "+username+" WHERE ID ="+item_id
            MyCur.execute(SQL)
            A = MyCur.fetchone()
            purchase_price = A[3]
            SQL = "DELETE FROM "+username+" WHERE ID ="+item_id
            MyCur.execute(SQL)
            SQL = "UPDATE ITEMS SET BID_AMOUNT = '', STATUS = 'Open', DOP = '', Buyer = '' WHERE ID = "+item_id
            MyCur.execute(SQL)
            SQL = "UPDATE BIDDERS SET QTY=QTY-1, TOTAL_AMOUNT = TOTAL_AMOUNT -"+purchase_price+" WHERE USERNAME = '"+username+"'"  
            db.commit()
            S = "SELECT * FROM BIDDERS WHERE USERNAME = '"+username+"'"
            MyCur.execute(S)
            R = MyCur.fetchone()
            print("The quantity of items in your cart now are: "+R[5])
            print("The total amount that you now need to pay is Rs."+R[6])
            var = 'False'
    else:
        print("The password entered is wrong!")
        attempts+=1
        if attempts==3:
            print("The number of wrong password attempts has been exhausted. Please try again after some time!")
            var = 'False'


    
'''''''''''''''''''''''''''''''''''''''''
Main Program (User-driven)
'''''''''''''''''''''''''''''''''''''''''
    
print("Welcome to Auction Bidding System 1.0!")

#try:
 #F = open("C:/Krish/Rules for Bidding.txt","r")
    #Intro = F.readlines()
    #print(Intro)
    #F.close()
#except:
   #print("Not working")
print("Don't forget that the minimum age to participate in the bidding process is 18 years! Enjoy your bidding!")
while True:
   Option = input("1:Add a Bidder   2:Upload Item   3:Search    4:View items   5:Bidding   6:Generate your Bill  7:Remove from Cart  8:Exit")
   if Option=="1":
      Add_Bidder()
   elif Option=="2":
      Upload_Item()
   elif Option=="3":
      SearchItem()
   elif Option=="4":
      opt = input("Do you want to view items open or closed for bidding?(Open/Closed)")
      View(opt)
   elif Option=="5":    
      Bidding()
   elif Option=="6":
      Generate_Bill()
   elif Option=="7":
      Remove_from_Cart()
   elif Option=="8":
      print("Thank you for visiting!")
      break
   else:
      print("Please enter a valid option!")  
   db.close()
