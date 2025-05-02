import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        user='root',
        password='Nahom2025',
        host='localhost',
        database='BankingProj', 
        autocommit=True) #saves changes as soon as made
    return connection
print('Connection successful!')
# connection.close()


def return_to_menu():
    choice = input('Go back to main menu? (Y/N): ')
    if choice in ['N', 'No']:
        print('Goodbye! ')
        exit()


def create_account():
    conn = get_connection()# creats a connection to MYSQL
    cursor = conn.cursor()

    while True: 
        name = input('Enter your customer name: ')
        if name.isalpha(): #make sure the input is alphabetic characters
            break
        else:
            print('Wrong, your name can only include alphabetic characters')

    while True:
        age = input("Enter your age: ")
        try:
            age = int(age)
            break
        except ValueError: 
            print('Wrong, your age must be in numbers and not in anything else.')

    email = input("Enter your email: ")

    while True:
        gender = input("Enter your gender: ")
        if gender.lower() in ['male', 'female']:
            break
        else:
            print("Gender must be 'Male' or 'Female'")

    password = input('Password: ')

    query = "INSERT INTO customer (customer_name, age, email, gender, password) VALUES (%s, %s, %s, %s, %s)"
    #using %s for valus helps protect against SQL injection and makes my code cleaner 
    values = (name, age, email, gender, password) # everything that the user inputs in the variabls its going to be insored withing this variable 
    cursor.execute(query, values) 
    print("Account created successfully!")

    #Fetching the new user bec im going to use it in the log in function
    validation = "SELECT * FROM customer WHERE customer_name = %s AND password = %s"
    cursor. execute(validation, (name, password))
    user = cursor.fetchone()
    cursor.close() 
    conn.close()

    return user #using in the login function & retruning full user tuple (id, name, age)
    #closes my conection 

# def insert_users(cusomer_name, age, email, gender, password):



def check_balance(current_user):
    conn = get_connection()
    cursor = conn.cursor()

    customer_id = current_user [0]
    query = "SELECT SUM(amount) FROM transactions WHERE customer_id = %s AND type = 'deposit' "
    cursor.execute(query, (customer_id,))#the comma makes it a real tuple 
    deposit = cursor.fetchone()[0] or 0 #if there's do deposit,return 0

    query = "SELECT SUM(amount) FROM transactions WHERE customer_id = %s AND type = 'Withdrawls Only' "
    cursor.execute(query, (customer_id,)) #acts like a channel for running SQl commands through my database connection 
    withdraw = cursor.fetchone()[0] or 0

    balance = deposit - withdraw
    print(f"Your current balance is: ${balance:.2f}")#means to show 2 deciamls places
     
    cursor.close()
    conn.close()
    print()

    return_to_menu() 

    





def deposit_funds(current_user):
    conn = get_connection()
    cursor = conn.cursor()


    customer_id = current_user [0]
     #this gets the ID from the row
    while True:
        try:
            amount = float(input("Amount to deposit: "))
            break
        except ValueError:
            print ('Invalid input. Please enter a valid number!')
    #using .format method to print upto 2 decimal point
    decimal_points = 2
    formatted_float = "{:.{}f}".format(amount, decimal_points)
    query = "INSERT INTO transactions (customer_id, amount, type, date) VALUES (%s, %s, 'deposit', NOW())"
    cursor.execute(query, (customer_id, amount))
    print("Deposit successful.")
    print(f'You deposited ${formatted_float}')

    cursor.close()
    conn.close()
    print()

    return_to_menu() 




def withdraw_funds(current_user):
    conn = get_connection()
    cursor = conn.cursor()


    customer_id = current_user [0]
    amount = float(input("Amount to withdraw: "))
    decimal_points = 2 
    formatted_float = "{:.{}f}".format(amount, decimal_points)#formats the amount into a string with exactly 2 decimal places 
    query = "INSERT INTO transactions (customer_id, amount, type, date) VALUES (%s, %s, 'withdraw', NOW())"
    cursor.execute(query, (customer_id, amount))
    print("Withdrawal successful.")
    print(f'You withdraw ${formatted_float}')


    cursor.close()
    conn.close()
    print()
    
    return_to_menu() 



def delete_account(current_user):
    conn = get_connection()
    cursor = conn.cursor()


    customer_id = current_user [0]
    cursor.execute("DELETE FROM transactions WHERE customer_id = %s", (customer_id, ))
    cursor.execute("DELETE FROM customer WHERE id = %s", (customer_id,))
    print("Account deleted.")

    cursor.close()
    conn.close()
    print()

    return login() 
    


def modify_account(current_user):
    conn = get_connection()
    cursor = conn.cursor()

  
    customer_id = current_user [0]
    new_email = input("Enter new email: ")

    cursor.execute("UPDATE customer SET email = %s WHERE id = %s", (new_email, customer_id))
    print("Email updated.")
        
    cursor.close()
    conn.close()
    print()
    return_to_menu() 




def login():
    conn = get_connection()# creats a connection to MYSQL
    cursor = conn.cursor()
    print('\nWelcome to Nahom Bank') 
    attempts = 0
    while attempts < 3:
        customer_name = input('Enter your customer name: ')
        if not customer_name.replace(" ", "").isalpha(): #by passing if the user inputs spaces 
            print("Name must contain only alphabetic characters.")
            attempts += 1
            continue

        password = input("Enter your password: ")

        validation = "SELECT * FROM customer WHERE customer_name = %s AND password = %s"
        cursor.execute(validation, (customer_name, password))
        user = cursor.fetchone()

        if user:
            return user  #Success — go to menu
        else:
            print("Invalid login.")
            attempts += 1

    # After 3 failed tries
    new_user = input("Too many attempts. Want to create an account? Y/N: ")
    if new_user in ['Y', 'Yes']:
        return create_account()
        return login() # go through login after account is created
    else:
        return None

            


current_user = login()

print()
def main_menu():
    print('1. Checking account balance')
    print('2. Depositing Funds')
    print('3. Withdrawing Funds')
    print('4. Deleting an account')
    print('5. Modifying account details')
    print('6. Exit')


    choice = input('Pick an option (1-6): ')
    return choice 


if current_user is not None: #if ther is a user 
    print(f'\nWelcome back, {current_user[1]}! ') #index 1 is the name
    while True: #loop forever until you stop it!
        choice = main_menu()
        
        if choice == '1':
            check_balance(current_user)
        elif choice == '2':
            deposit_funds(current_user)
        elif choice == '3':
            withdraw_funds(current_user)
        elif choice == '4':
            delete_account(current_user)
        elif choice == '5':
            modify_account(current_user)
        elif choice == '6': 
            print('Thank you!')
            break
        else:
            print('Please input a valid choice. Please try again! ')

# else: 
#     print('Good Bye! You didnt create an account! ')






