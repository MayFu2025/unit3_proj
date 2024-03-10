from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.navigationrail import MDNavigationRail
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton, MDRectangleFlatIconButton, MDIconButton
from kivymd.uix.dialog import MDDialog
import datetime
from library import DatabaseWorker, make_hash, check_hash_match, show_popup, check_admin, get_letter_score


class App(MDApp):
    db = DatabaseWorker('database.db')
    current_user = []

    def build(self):
        Window.size = 1200, 1000
        return

    def on_stop(self):
        App.db.close()


class StartupScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.dialog = None

    def on_enter(self):
        self.ids.firstname.text = ""
        self.ids.lastname.text = ""
        self.ids.pword.text = ""

    def try_login(self):
        errors = []
        firstname = self.ids.firstname.text
        lastname = self.ids.lastname.text
        pword = self.ids.pword.text

        # Check if employee exists
        result = App.db.search(
            f"SELECT password, is_admin FROM users WHERE first_name = '{firstname}' and last_name='{lastname}'")
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
    def logout(self):
        App.current_user = []
        self.parent.parent.parent.current = "Startup"


class BackButton(MDRectangleFlatIconButton):
    pass


class HomeScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_pre_enter(self):
        month = str(datetime.date.today()).replace('-', '')[:6]
        self.ids.month_total_orders.text = f"""{App.db.search(query=f"select count(*) from orders where date like '{month}%'")[0]}"""
        self.ids.month_total_profit.text = f"""{App.db.search(query=f"select sum(amount) from ledger where date like '{month}%' and amount>0")[0]}"""
        self.ids.month_total_loss.text = f"""{App.db.search(query=f"select sum(amount) from ledger where date like '{month}%' and amount<=0")[0]}"""
        if App.db.search(query=f"select count(*) from orders where date like '{month}%'")[0] != 0:
            self.ids.month_avg_score.text = f"""{get_letter_score(App.db.search(f"select avg(score) from orders where date like '{month}%'")[0])}"""

        self.ids.alltime_orders.text = f"""{App.db.search(query=f"select count(*) from orders")[0]}"""
        self.ids.alltime_completed.text = f"""{App.db.search(query=f"select count(*) from orders where completion=TRUE")[0]}"""
        self.ids.alltime_incomplete.text = f"""{App.db.search(query=f"select count(*) from orders where completion=FALSE")[0]}"""


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
    def on_pre_enter(self):
        columns_names = [('id', 50), ('First Name', 85), ('Last Name', 85), ('Admin Status', 50)]
        self.employee_table = MDDataTable(
            size_hint=(0.6, 0.8),
            pos_hint={'center_x': 0.41, 'center_y': 0.45},
            use_pagination=True,
            rows_num=10,
            check=True,
            column_data=columns_names
        )
        self.employee_table.bind(on_check_press=self.checkbox_pressed)
        self.add_widget(self.employee_table)
        self.update()

    def update(self, sort=None):
        query = 'Select id, first_name, last_name, is_admin from users'
        if sort is not None:
            query += f' order by {sort.strip("")}'
        data = App.db.search(query=query, multiple=True)
        self.employee_table.update_row_data(None, data)

    def on_leave(self):
        # Including this prevents tables from being created on top of each other, which can cause shadows
        self.remove_widget(self.employee_table)

    def checkbox_pressed(self, table, current_row):
        if current_row[0] not in self.selected_rows:
            self.selected_rows.append(current_row[0])
        else:
            self.selected_rows.remove(current_row[0])

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

    def purchase_popup(self, material):
        InventoryManager.current_material = material
        self.dialog = MDDialog(
            title=f"Purchase {material}?",
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
        errors = []
        if not check_admin(App.current_user):
            errors.append("You do not have these permissions.")
        else:
            current_total = App.db.search(query="SELECT total FROM ledger WHERE id=(SELECT max(id) FROM ledger)")[0]
            if current_total < PurchaseDialog.cost:  # if not sufficient money
                errors.append("Not enough money!")
            else:
                query = f"""insert into ledger (date, amount, total)
                            values ({str(datetime.date.today()).replace('-', '')}, {-PurchaseDialog.cost}, {current_total - PurchaseDialog.cost})"""
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
        self.material_owned = \
            App.db.search(query=f"select amount from resources where name='{InventoryManager.current_material}'")[0]
        self.money_available = App.db.search(query="SELECT total FROM ledger WHERE id=(SELECT max(id) FROM ledger)")[0]
        self.ids.cost_amount.text = f"Currently Own: {self.material_owned}\nCost per unit: ${self.material_cost}\nMoney Available: ${self.money_available}"

    def update_amount_text(self):
        self.ids.total_cost.text = f"Total cost: ${int(self.ids.amount.text) * self.material_cost}"
        PurchaseDialog.cost = int(self.ids.amount.text) * self.material_cost
        PurchaseDialog.amount = int(self.ids.amount.text)


class OrderManager(MDScreen):
    viewed_order = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orders_data = None

    def on_enter(self):
        self.update()

    def on_leave(self):
        self.ids.orders_container.clear_widgets()

    def update(self, condition=None):
        self.ids.orders_container.clear_widgets()

        if condition is not None:
            query = "select * from orders " + condition
            self.orders_data = App.db.search(query=query, multiple=True)
        else:
            self.orders_data = App.db.search(query="select * from orders where completion=0", multiple=True)

        for order in self.orders_data:
            self.ids.orders_container.add_widget(
                MDRectangleFlatIconButton(
                    text=f"Order #{order[0]}",
                    icon=f"{self.choose_icon(order_id=str(order[0]))}",
                    icon_size=50,
                    size_hint=(1, 0.5),
                    on_press=lambda x, order_id=order[0]: self.view_details(order_id=order_id)
                )
            )

    def choose_icon(self, order_id):
        if App.db.search(query=f"select completion from orders where id={order_id}")[0] == 0:
            return "package-variant"
        else:
            return "package-variant-closed-check"

    def view_details(self, order_id: int):
        OrderManager.viewed_order = order_id
        print(OrderManager.viewed_order)
        self.parent.current = "OrderDetails"


class OrderDetails(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self):
        # Gain order information
        query = f"select * from orders where id={OrderManager.viewed_order}"
        self.order_details = App.db.search(query=query, multiple=False)
        self.ids.order_id.text = f"Order ID: #{self.order_details[0]}"
        self.ids.order_date.text = f"Order Date: {self.order_details[1]}"
        self.ids.customer_name.text = f"Customer Name: {' '.join(list(App.db.search(query=f'select first_name, last_name from customers where id={self.order_details[2]}')))}"
        self.ids.customer_address.text = f"Customer Address: {App.db.search(query=f'select address from customers where id={self.order_details[2]}')[0]}"
        self.ids.order_description.text = f"Order Description: {self.order_details[6]}"
        self.ids.order_price.text = f"Price: ${self.order_details[3]}"
        self.ids.order_score.text = f"Sustainability Score: {get_letter_score(self.order_details[4])}"

        # Gain materials count and make list
        query = f"""select resources.name, OrdersResources.amount from OrdersResources
        inner join resources on resources.id = OrdersResources.resource_id
        where OrdersResources.order_id = {OrderManager.viewed_order}
        """
        self.needed_materials = App.db.search(query=query, multiple=True)
        for material in self.needed_materials:
            self.ids.materials_needed.add_widget(TwoLineListItem(
                text=f"{material[0]}",
                secondary_text=f"Amount: {material[1]}"
            )
            )

    def cancel_order(self):
        # Delete from orders table, and delete resources for order_id from OrdersResources table
        App.db.run_query(query=f"delete from orders where id={OrderManager.viewed_order}")
        App.db.run_query(query=f"delete from OrdersResources where order_id={OrderManager.viewed_order}")
        show_popup(self, messages=["Order cancelled."], text="OK")

    def complete_order(self):
        # Check if sufficient materials
        errors = []
        for material in self.needed_materials:
            if material[1] > App.db.search(query=f"select amount from resources where name='{material[0]}'")[0]:
                errors.append(f"Not enough {material[0]}")

        # If sufficient materials, complete order
        if len(errors) == 0:
            # Take away materials
            for material in self.needed_materials:
                App.db.run_query(
                    query=f"update resources set amount=(select amount from resources where name='{material[0]}')-{material[1]} where name='{material[0]}'")
            # Add money
            App.db.run_query(
                query=f"insert into ledger(date, amount, total) values({str(datetime.date.today()).replace('-', '')}, {self.order_details[3]}, (select total from ledger where id=(select max(id) from ledger))+{self.order_details[3]})")
            # Mark order as complete
            App.db.run_query(query=f"update orders set completion=1 where id={OrderManager.viewed_order}")
            errors.append("Order completed successfully.")

        show_popup(self, messages=errors, text="OK")


class NewOrder(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speakers = {
            "standard": {"aluminium": 1, "copper": 2, "zinc": 1, "lithium": 1},  # Standard
            "gaming": {"aluminium": 1, "copper": 2, "zinc": 1, "lithium": 3},  # Longer battery life
            "bassboosted": {"aluminium": 2, "copper": 3, "zinc": 2, "lithium": 1},  # Larger speakers + coil power
            "audiophile": {"aluminium": 2, "copper": 2, "zinc": 2, "lithium": 2}  # All-around
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
        self.update()

    def clear_order(self):
        self.order = []
        self.options = ["base", "padding", "speaker"]
        self.score = 0
        self.price = 0
        self.update()

    def update(self):
        # disable buttons
        check = {"base": ["aluminium", "carbon", "wood"], "padding": ["silicone", "foam", "leather"],
                 "speaker": ["standard", "gaming", "bassboosted", "audiophile"]}
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
        self.score = 0
        for material in self.order:
            self.score += App.db.search(query=f"select score from resources where name='{material}'")[0]

        # calculate price
        self.price = 0
        for material in self.order:
            self.price += App.db.search(query=f"select sell_price from resources where name='{material}'")[0]
        for options in self.options[3:]:
            self.price += 30

        # update the text
        self.ids.specifications.text = f"""Base: {self.options[0]}\nPadding: {self.options[1]}\nSpeakers: {self.options[2]}\nOptions: {', '.join(self.options[3:])}\nSustainability Score: {get_letter_score(self.score)}"""
        self.ids.price.text = f"Total Price: ${self.price}"

    def place_order(self):
        errors = []
        # Check for required information
        if len(self.order) < 10:  # 10 units of material is the minimum an order can have
            errors.append("One or more selections are missing.")

        if self.ids.customer_firstname.text == "" or self.ids.customer_lastname.text == "":
            errors.append("Customer name is missing.")
        else:  # Customer names are present
            # Check if existing customer or not (whether address is required)
            existing_address = App.db.search(
                query=f"select address from customers where first_name='{self.ids.customer_firstname.text}' and last_name='{self.ids.customer_lastname.text}'")
            if existing_address is None and self.ids.customer_address.text == "":
                errors.append("New customer detected. Customer address is required.")

        if len(errors) == 0:
            # Add customer if new
            if existing_address is None:
                App.db.run_query(
                    query=f"insert into customers(first_name, last_name, address) values('{self.ids.customer_firstname.text}', '{self.ids.customer_lastname.text}', '{self.ids.customer_address.text}')")

            # Place new order
            order_description = f"A {self.options[0]} base with {self.options[1]} padding and {self.options[2]} speakers."
            if self.options[3:]:
                order_description += f" Added options for {', '.join(self.options[3:])}."

            query = f"""insert into orders(date, customer_id, cost, score, completion, description)
                        values({str(datetime.date.today()).replace('-', '')},
                                (select id from customers where first_name='{self.ids.customer_firstname.text}' and last_name='{self.ids.customer_lastname.text}'),
                                {self.price},
                                {self.score},
                                false,
                                '{order_description}')"""
            App.db.run_query(query=query)

            # Add materials to order
            order_id = App.db.search(query="select max(id) from orders")[0]
            materials = {x: self.order.count(x) for x in
                         self.order}  # Make dictionary of materials in the order and their amounts
            for material, amount in materials.items():
                App.db.run_query(
                    query=f"insert into OrdersResources(order_id, resource_id, amount) values({order_id}, (select id from resources where name='{material}'), {amount})")

            errors.append("Order created successfully.")
        show_popup(self, messages=errors, text="OK")


class FinanceManager(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ledger_table = None
        self.dialog = None

    def on_pre_enter(self):
        if App.db.search(query="select count(*) from ledger")[0] != 0:
            self.ids.current_total.text = f"Current Balance: ${App.db.search(query='select total from ledger where id=(select max(id) from ledger)')[0]}"
        if App.db.search(query="select count(*) from ledger where amount>0")[0] != 0:
            self.ids.total_profit.text = f"Total profit: ${App.db.search(query='select sum(amount) from ledger where amount>0')[0]}"
        if App.db.search(query="select count(*) from ledger where amount<=0")[0] != 0:
            self.ids.total_loss.text = f"Total loss: ${App.db.search(query='select sum(amount) from ledger where amount<=0')[0]}"

        # Making a Table
        columns_names = [('id', 50), ('Date', 125), ('Amount', 125)]
        self.ledger_table = MDDataTable(
            size_hint=(0.58, 0.8),
            pos_hint={'center_x': 0.42, 'center_y': 0.45},
            use_pagination=True,
            rows_num=10,
            check=False,
            column_data=columns_names
        )
        self.add_widget(self.ledger_table)
        self.update()

    def on_enter(self):
        self.update()

    def on_leave(self):
        # Including this prevents tables from being created on top of each other, which can cause shadows
        self.remove_widget(self.ledger_table)

    def update(self, sort=None):
        query = 'Select id, date, amount from ledger'
        if sort is not None:
            query += f' order by {sort.strip("")}'

        data = App.db.search(query=query, multiple=True)
        self.ledger_table.update_row_data(None, data)

    def filter(self, filter=None):
        query = 'Select id, date, amount from ledger' # Default
        if filter is not None:
            if filter == "month":
                query += f""" where date like '{str(datetime.date.today()).replace("-", "")[:6]}%'""" # Obtain YYYYMM
            elif filter == "year":
                query += f" where date like '{datetime.date.today().year}%'"
            else:
                query += f' where {filter.strip("")}'
        data = App.db.search(query=query, multiple=True)
        self.ledger_table.update_row_data(None, data)


a = App()
a.run()
