from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.navigationrail import MDNavigationRail
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.icon_definitions import md_icons

import library
from library import DatabaseWorker, check_hash_match, show_popup, check_admin

class StartupScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.dialog = None

    def on_enter(self):
        self.ids.firstname.text = ""
        self.ids.lastname.text = ""
        self.ids.pword.text = ""

    def try_login(self):
        print("try_login called")
        errors = []
        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        pword = self.ids.pword.text

        # Check if employee exists
        result = App.db.search(f"SELECT password, is_admin FROM users WHERE first_name = '{firstname}' and last_name='{lastname}'")
        print(result)
        if result is None:
            errors.append("Employee does not exist.")
        else:
            if not check_hash_match(hashed=result[0], text=pword):
                errors.append("Password is incorrect.")

        if len(errors) > 0:
            show_popup(self, errors, "OK")
        else:
            App.current_user = [firstname, lastname, result[1]]
            self.parent.current = "Home"


class Navigation(MDNavigationRail):
    def try_change(self, destination:str):
        print(self.parent.ids)

    def logout(self):
        App.current_user = []
        self.parent.parent.parent.current = "Startup"

class BackButton(MDFlatButton):
    pass


class HomeScreen(MDScreen):
    pass


class EmployeeManager(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_table = None
        self.selected_rows = []  # List to keep track which rows were selected
        self.dialog = None
        self.new_admin = False

    # Making a Table
    def on_pre_enter(self, *args): #'*args' means it doesn't know what the arguments will be
        columns_names = [('First Name', 110), ('Last Name', 110), ('Admin Status', 50)]
        self.employee_table = MDDataTable(
            size_hint = (0.6, 0.8),
            pos_hint = {'center_x':0.41, 'center_y':0.43},
            use_pagination = False,
            check = True,
            column_data = columns_names
        )
        self.employee_table.bind(on_row_press=self.row_pressed)  # bind a function to function
        self.employee_table.bind(on_check_press=self.checkbox_pressed)
        self.add_widget(self.employee_table)
        self.update()

    def update(self):
        data = App.db.search(query='Select first_name, last_name, is_admin from users', multiple=True)
        self.employee_table.update_row_data(None, data)

    def row_pressed(self, table, cell): # Don't think we need this
        print(f"Value clicked: {cell.text}")

    def checkbox_pressed(self, table, current_row):
        print(f"Record checked: {current_row}")
        # Here you could delete or update the record

    def check_admin_status(self, checkbox, value):
        self.new_admin = False
        if value:
            self.new_admin = True

    def try_create(self):
        errors = []
        if not check_admin(App.current_user):
            errors += "You do not have these permissions."
        else:
            firstname = self.ids.new_firstname.text
            lastname = self.ids.new_lastname.text
            password = self.ids.new_password.text
            admin = self.new_admin

            # Check if user exists
            result = App.db.search(query=f"SELECT * from users where first_name='{firstname}' and last_name='{lastname}'")
            if result is not None:
                errors.append("User with same name already exists.")
            else:
                print(firstname, lastname, password, admin)
                errors.append("User creation successful.")

        show_popup(screen=self, messages=errors, text="OK")




class InventoryManager(MDScreen):
    pass


class OrderManager(MDScreen):
    pass


class FinanceManager(MDScreen):
    pass


class App(MDApp):
    db = DatabaseWorker('database.db')
    current_user = []

    def build(self):
        Window.size = 1200, 1000
        return


a = App()
a.run()
