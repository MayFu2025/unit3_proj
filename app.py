from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDLabel
from kivymd.uix.list import TwoLineRightIconListItem, TwoLineIconListItem, IconRightWidget, TwoLineListItem
from kivymd.uix.navigationrail import MDNavigationRail
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.icon_definitions import md_icons
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
import datetime

import library
from library import DatabaseWorker, make_hash, check_hash_match, show_popup, check_admin


class App(MDApp):
    db = DatabaseWorker('database.db')
    current_user = []
    money = 0
    materials = {"wood": 10, "carbon": 5, "aluminium": 10, "silicone": 10, "foam": 5, "leather": 25, "cobalt": 20,
                 "copper": 15, "lithium": 20}

    def build(self):
        Window.size = 1200, 1000
        return


class StartupScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.dialog = None

    def on_enter(self):
        self.ids.firstname.text = ""
        self.ids.lastname.text = ""
        self.ids.pword.text = ""

    def try_login(self):
        print(make_hash("test"))
        errors = []
        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        pword = self.ids.pword.text

        # Check if employee exists
        result = App.db.search(
            f"SELECT password, is_admin FROM users WHERE first_name = '{firstname}' and last_name='{lastname}'")
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
    def try_change(self, destination: str):
        print(self.parent.ids)

    def logout(self):
        App.current_user = []
        self.parent.parent.parent.current = "Startup"


class BackButton(MDRectangleFlatIconButton):
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

    def on_enter(self):
        self.ids.new_firstname.text = ""
        self.ids.new_lastname.text = ""
        self.ids.new_password.text = ""

    # Making a Table
    def on_pre_enter(self, *args):  # '*args' means it doesn't know what the arguments will be
        columns_names = [('id', 50), ('First Name', 85), ('Last Name', 85), ('Admin Status', 50)]
        self.employee_table = MDDataTable(
            size_hint=(0.6, 0.8),
            pos_hint={'center_x': 0.41, 'center_y': 0.45},
            use_pagination=False,
            check=True,
            column_data=columns_names
        )
        self.employee_table.bind(on_check_press=self.checkbox_pressed)  # bind a function to function
        self.add_widget(self.employee_table)
        self.update()

    def update(self, sort=None):
        query = 'Select id, first_name, last_name, is_admin from users'
        if sort is not None:
            query += f' order by {sort.strip("")}'
        print(query)
        data = App.db.search(query=query, multiple=True)
        self.employee_table.update_row_data(None, data)

    def checkbox_pressed(self, table, current_row):
        print(f"Record checked: {current_row}")
        if current_row[0] not in self.selected_rows:
            self.selected_rows.append(current_row[0])
        else:
            self.selected_rows.remove(current_row[0])
        print(self.selected_rows)

    def admin_status_checkbox(self, checkbox, value):
        self.new_admin = False
        if value:
            self.new_admin = True

    def try_create(self):
        errors = []
        if not check_admin(App.current_user):
            errors.append("You do not have these permissions.")
        else:
            firstname = self.ids.new_firstname.text
            lastname = self.ids.new_lastname.text
            password = self.ids.new_password.text
            admin = self.new_admin

            # Check if user exists
            result = App.db.search(
                query=f"SELECT * from users where first_name='{firstname}' and last_name='{lastname}'")
            if result is not None:
                errors.append("User with same name already exists.")
            else:
                print(firstname, lastname, password, admin)
                App.db.run_query(
                    query=f'insert into users(first_name, last_name, password, is_admin) values("{firstname}", "{lastname}", "{make_hash(password)}", {admin})')
                errors.append("User created successfully.")

        show_popup(screen=self, messages=errors, text="OK")
        self.update()

    def delete_user(self):
        errors = []
        if not check_admin(App.current_user):
            errors.append("You do not have these permissions.")
        elif len(self.selected_rows) == 0:
            errors.append("No users selected.")
        else:
            for ids in self.selected_rows:
                App.db.run_query(query=f"delete from users where id={ids}")
            errors.append("User(s) deleted successfully.")
        show_popup(screen=self, messages=errors, text="OK")
        self.update()

    def edit_admin(self):
        errors = []
        if not check_admin(App.current_user):
            errors.append("You do not have these permissions.")
        elif len(self.selected_rows) == 0:
            errors.append("No users selected.")
        else:
            for ids in self.selected_rows:
                query = f"update users set is_admin= not(select is_admin where id = {ids}) where id={ids}"
                App.db.run_query(query=query)
            errors.append("Permissions changed successfully.")

        show_popup(screen=self, messages=errors, text="OK")
        self.update()


class InventoryManager(MDScreen):
    current_material = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

    def purchase_popup(self, material): #text still doesn't show up which is kinda sad but it's okay
        InventoryManager.current_material = material
        print(self)
        self.dialog = MDDialog(
            title=f"Purchase {material}?",
            text=f"""Cost per unit: ${App.db.search("select cost from resources where name='{material}'")}
                    Currently have: ${App.money}""",
            type="custom",
            content_cls=PurchaseDialog(),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_press=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="Purchase",
                    on_press=lambda x: self.purchase()  # purchase function comes here
                )
            ]
        )
        self.dialog.open()

    def purchase(self):
        # Purchase (take away money and add materials)
        print("test")
        errors = []
        current_total = App.db.search(query="SELECT total FROM ledger WHERE id=(SELECT max(id) FROM ledger)")[0]
        print(current_total)
        if current_total < PurchaseDialog.cost:  # if not sufficient money
            errors.append("Not enough money!")
        else:
            query = f"""insert into ledger (buy, sell, amount, total)
                        values (1, 0, {PurchaseDialog.cost}, {current_total - PurchaseDialog.cost})"""
            App.db.run_query(query=query)
            query = f"""update resources set amount=((select amount from resources where resources.name='{InventoryManager.current_material}')+{PurchaseDialog.amount})
                        where name='{InventoryManager.current_material}'"""
            App.db.run_query(query=query)
            errors.append("Purchase successful!")
        self.dialog.dismiss()
        show_popup(self, messages=errors, text="OK")


class PurchaseDialog(MDBoxLayout):
    cost = 0
    amount = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.material_cost = \
        App.db.search(query=f"select cost from resources where name='{InventoryManager.current_material}'")[0]

    def update_amount_text(self):
        self.ids.total_cost.text = f"Total cost: ${int(self.ids.amount.text) * self.material_cost}"  # * App.materials[InventoryManager.current_material]
        PurchaseDialog.cost = int(self.ids.amount.text) * self.material_cost
        PurchaseDialog.amount = int(self.ids.amount.text)


class OrderManager(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orders_data = App.db.search(query="select * from orders where completion=FALSE", multiple=True)

    def on_pre_enter(self):
        print(self.orders_data)
        print(self.ids.orders_container)
        for order in self.orders_data:
            self.ids.orders_container.add_widget(
                TwoLineListItem(
                    text=f"Order #{order[0]}",
                    secondary_text=f"Date ordered: {str(order[1])[:4]}/{str(order[1])[4:6]}/{str(order[1])[6:8]}"
                )
            )

    def on_leave(self, *args):
        self.ids.orders_container.clear_widgets()

    def view_details(self, order_id: int):
        self.parent.parent.parent.current = "OrderDetails"

    def update(self):
        # searched = self.ids.searchbar.text
        # query = f'''select * from orders
        #             where (id like '%{searched}%') or (date like '%{searched}%') or
        #             (customers.first_name like '%{searched}%') or (customers.last_name like '%{searched}%')
        #             inner join customers on orders.customer_id=customers.id)'''
        result = App.db.search(query=query, multiple=True)
        pass


class OrderDetails(MDScreen):
    pass


class NewOrder(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speakers = {
            "standard" : {"aluminium":1, "copper":2, "zinc":1, "lithium":1}, # Standard
            "gaming" : {"aluminium":1, "copper":2, "zinc":1, "lithium":3}, # Longer battery life
            "bassboosted" : {"aluminium":2, "copper":3, "zinc":2, "lithium":1}, # Larger speakers + coil power
            "audiophile" : {"aluminium":2, "copper":2, "zinc":2, "lithium":2} # All-around
        }
        self.order = []
        self.options = ["base", "padding", "speaker"]
        self.score = 0
        self.price = 0
        self.dialog = None

    def add_material(self, part, material):
        if part == "base":
            self.options[0] = material
            for n in range(3):  # 3 units of base
                self.order.append(material)
        elif part == "padding":  # 2 units of padding
            self.options[1] = material
            for n in range(2):
                self.order.append(material)
        elif part == "speaker":
            self.options[2] = material
            for k, v in self.speakers[material].items():
                for unit in range(v):
                    self.order.append(k)
        else:
            self.options.append(material)  # Optional was selected
        print(self.order)
        print(self.options)
        self.update()


    def clear_order(self):
        self.order = []
        self.options = ["base", "padding", "speaker"]
        self.score = 0
        self.price = 0
        self.update()

    def update(self):
        # disable buttons TODO: can probably use a loop lol
        check = {"base": ["aluminium", "carbon", "wood"], "padding": ["silicone", "foam", "leather"], "speaker": ["standard", "gaming", "bassboosted", "audiophile"]}
        for n in range(3):
            if self.options[n] != list(check)[n]:
                for material in list(check.values())[n]:
                    self.ids[material].disabled = True
            else:
                for material in list(check.values())[n]:
                    self.ids[material].disabled = False
        if self.options[3:]:
            for option in self.options[3:]:
                self.ids[option].disabled = True
        else:
            self.ids.coating.disabled = False
            self.ids.waterproof.disabled = False
            self.ids.bluetooth.disabled = False

        # calculate sustainability score
        score = 0
        for material in self.order:
            score += App.db.search(query=f"select score from resources where name='{material}'")[0]
        self.score = score

        # calculate price
        price = 0
        for material in self.order:
            price += App.db.search(query=f"select sell_price from resources where name='{material}'")[0]
        for options in self.options[3:]:
            price += 30
        self.price = price

        # update the text
        # TODO: when adding more than one option, somehow the '' is not removed
        self.ids.specifications.text = f"""Base: {self.options[0]}\nPadding: {self.options[1]}\nSpeakers: {self.options[2]}\nOptions: {', '.join(self.options[3:])}\nSustainability Score: {self.score}"""
        self.ids.price.text = f"Total Price: ${self.price}"
    def place_order(self):
        errors = []
        # Check for required information
        if len(self.order) < 10:  # 10 units of material is the minimum an order can have
            errors.append("One or more selections are missing.")

        if self.ids.customer_firstname.text == "" or self.ids.customer_lastname.text == "":
            errors.append("Customer name is missing.")
        else: # Customer names are present
            # Check if existing customer or not (whether address is required)
            existing_address = App.db.search(query=f"select address from customers where first_name='{self.ids.customer_firstname.text}' and last_name='{self.ids.customer_lastname.text}'")
            if existing_address is None and self.ids.customer_address.text == "":
                errors.append("New customer detected. Customer address is required.")

        if len(errors) == 0:
            # Add customer if new
            if existing_address is None:
                App.db.run_query(query=f"insert into customers(first_name, last_name, address) values('{self.ids.customer_firstname.text}', '{self.ids.customer_lastname.text}', '{self.ids.customer_address.text}')")
            # Place new order
            query = f"""insert into orders(date, customer_id, cost, score, completion)
                        values({str(datetime.date.today()).replace("-", "")},
                                (select id from customers where first_name='{self.ids.customer_firstname.text}' and last_name='{self.ids.customer_lastname.text}'),
                                {self.price},
                                {self.score},
                                false)"""
            App.db.run_query(query=query)
            # Add materials to order
            order_id = App.db.search(query="select max(id) from orders")[0]
            materials = {x:self.order.count(x) for x in self.order}  # Make dictionary of materials in the order and their amounts
            for material, amount in materials.items():
                App.db.run_query(query=f"insert into OrdersResources(order_id, resource_id, amount) values({order_id}, (select id from resources where name='{material}'), {amount})")

            errors.append("Order created successfully.")
        show_popup(self, messages=errors, text="OK")


class FinanceManager(MDScreen):
    pass


a = App()
a.run()
