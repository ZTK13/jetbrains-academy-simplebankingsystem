# Write your code here
import random
import sqlite3


def calculate_luhn_checksum(num_string):
    num_list = [int(n) for n in num_string]
    num_list = [num_list[i] * 2 if i % 2 == 0 else num_list[i]
                for i in range(len(num_list))]
    num_list = [n - 9 if n > 9 else n for n in num_list]
    digit_sum = sum(num_list)
    checksum = (digit_sum * 9) % 10
    return checksum


class BankingSystem:
    def __init__(self):
        self.iin = '400000'
        self.current_menu = 1
        self.login_card = None
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.cur.execute("""
        create table if not exists card (
            id integer primary key autoincrement,
            number text unique,
            pin text,
            balance integer default 0
        )
        """)
        self.conn.commit()

    def create_account(self):
        if self.current_menu == 1:
            valid_card_number = False
            card_num = '0' * 10
            while not valid_card_number:
                card_num_suffix = random.randint(0, 999999999)
                card_num = self.iin + str(card_num_suffix).zfill(9)
                checksum = calculate_luhn_checksum(card_num)
                card_num += str(checksum)
                self.cur.execute(f"""
                select * from card 
                where number = {card_num}
                """)
                db_row = self.cur.fetchone()
                if not db_row:
                    valid_card_number = True
            # new_account = BankAccount(card_num)
            pin_num = random.randint(0, 9999)
            pin = str(pin_num).zfill(4)
            self.cur.execute(f"""
            insert into card (number, pin) 
            values ({card_num}, {pin})
            """)
            self.conn.commit()
            print("Your card has been created")
            print("Your card number:")
            print(card_num)
            print("Your card PIN:")
            print(pin)
            # self.accounts[card_num] = new_account

    def log_into_account(self):
        # account = None
        if self.current_menu == 1:
            print("Enter your card number:")
            card_num = input()
            print("Enter your PIN:")
            pin = input()
            self.cur.execute(f"""
            select pin from card 
            where number = {card_num}
            """)
            db_row = self.cur.fetchone()
            if db_row:
                db_pin = db_row[0]
                if pin == db_pin:
                    print("You have successfully logged in!")
                    self.current_menu = 2
                    self.login_card = card_num
                    return

            print("Wrong card number or PIN")
            # if card_num in self.accounts.keys():
            #     account = self.accounts[card_num]
            #     if pin != account.pin:
            #         account = None
            # if account is None:
            #     print("Wrong card number or PIN")
            # else:
            #     print("You have successfully logged in!")
            #     self.current_menu = 2
        # self.login_account = account

    def get_account_balance(self):
        if self.current_menu == 2:
            self.cur.execute(f"""
            select balance from card 
            where number = {self.login_card}
            """)
            db_row = self.cur.fetchone()
            return db_row[0]

    def add_income(self):
        if self.current_menu == 2:
            print("Enter income:")
            income = int(input())
            self.cur.execute(f"""
            select balance from card 
            where number = {self.login_card}
            """)
            db_row = self.cur.fetchone()
            balance = db_row[0] + income
            self.cur.execute(f"""
            update card
            set balance = {balance}
            where number = {self.login_card}
            """)
            self.conn.commit()
            print("Income was added!")

    def do_transfer(self):
        if self.current_menu == 2:
            print("Transfer")
            print("Enter card number:")
            transfer_card = input().strip()
            if transfer_card == self.login_card:
                print("You can't transfer money to the same account!")
            elif ((len(transfer_card) != 16) or
                  (int(transfer_card[-1]) !=
                   calculate_luhn_checksum(transfer_card[:-1]))):
                print("Probably you made a mistake in the card number. " +
                      "Please try again!")
            else:
                self.cur.execute(f"""
                select balance from card 
                where number = {self.login_card}
                """)
                login_account_balance = self.cur.fetchone()[0]
                self.cur.execute(f"""
                select balance from card 
                where number = {transfer_card}
                """)
                db_row = self.cur.fetchone()
                if db_row:
                    receiver_account_balance = db_row[0]
                    print("Enter how much money you want yo transfer:")
                    transfer_amount = int(input())
                    if transfer_amount > login_account_balance:
                        print("Not enough money!")
                    else:
                        self.cur.execute(f"""
                        update card
                        set balance = {login_account_balance - transfer_amount}
                        where number = {self.login_card}
                        """)
                        self.conn.commit()
                        self.cur.execute(f"""
                        update card
                        set balance = {receiver_account_balance + 
                                       transfer_amount}
                        where number = {transfer_card}
                        """)
                        self.conn.commit()
                        print("Success!")
                else:
                    print("Such a card does not exist.")

    def close_account(self):
        if self.current_menu == 2:
            self.cur.execute(f"""
            delete from card 
            where number = {self.login_card}
            """)
            self.conn.commit()
            self.login_card = None
            print("The account has been closed!")
            self.current_menu = 1

    def log_out(self):
        if self.current_menu == 2:
            self.login_card = None
            print("You have successfully logged out!")
            self.current_menu = 1

    def print_menu(self):
        if self.current_menu == 1:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")
        else:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")

    def call_correct_command(self):
        option = int(input())
        print()
        if option == 0:
            self.conn.close()
            print("Bye!")
            return False
        elif self.current_menu == 1:
            if option == 1:
                self.create_account()
            elif option == 2:
                self.log_into_account()
            else:
                print("Wrong option entered")
        elif self.current_menu == 2:
            if option == 1:
                print(f"Balance: {self.get_account_balance()}")
            elif option == 2:
                self.add_income()
            elif option == 3:
                self.do_transfer()
            elif option == 4:
                self.close_account()
            elif option == 5:
                self.log_out()
            else:
                print("Wrong option entered")
        print()
        return True


# class BankAccount:
#     def __init__(self, card_num):
#         self.card_num = card_num
#         pin_num = random.randint(0, 9999)
#         self.pin = str(pin_num).zfill(4)
#         self.balance = 0


bank_v1 = BankingSystem()
continue_loop = True
while continue_loop:
    bank_v1.print_menu()
    continue_loop = bank_v1.call_correct_command()
