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
from library import DatabaseWorker, check_hash_match, show_popup

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
        db = DatabaseWorker("database.db")
        result = db.search(f"SELECT password FROM users WHERE first_name = '{firstname}' and last_name='{lastname}'")
        print(result)
        db.close()
        if result is None:
            errors.append("Employee does not exist.")
        else:
            if not check_hash_match(hashed=result[0], text=pword):
                errors.append("Password is incorrect.")

        if len(errors) > 0:
            show_popup(self, errors)
        else:
            self.parent.current = "Home"


class Navigation(MDNavigationRail):
    def try_change(self, destination:str):
        print(self.parent.ids)

class BackButton(MDFlatButton):
    pass


class HomeScreen(MDScreen):
    pass


class EmployeeManager(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employee_table = None
        self.selected_rows = []  # List to keep track which rows were selected

    # Making a Table
    def on_pre_enter(self, *args): #'*args' means it doesn't know what the arguments will be
        columns_names = [('First Name', 50), ('Last Name', 50), ('Admin Status', 50)]
        self.employee_table = MDDataTable(
            size_hint = (0.8, 0.5),
            pos_hint = {'center_x':0.5, 'center_y':0.5},
            use_pagination = False,
            check = True,
            column_data = columns_names
        )
        self.data_tables.bind(on_row_press=self.row_pressed)  # bind a function to function
        self.data_tables.bind(on_check_press=self.checkbox_pressed)
        self.add_widget(self.data_tables)
        self.update()


class InventoryManager(MDScreen):
    pass


class OrderManager(MDScreen):
    pass


class FinanceManager(MDScreen):
    pass


class app(MDApp):
    def build(self):
        Window.size = 1200, 1000
        return


a = app()
a.run()
