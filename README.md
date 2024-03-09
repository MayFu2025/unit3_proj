# Unit 3: Comapany Manager Application

![](headerimage.png)  
<sub>"THE HEADER" by SOMEONE, *linkhere*</sub>

## Criteria A: Planning
### Problem Definition
Headphones for the New Era (in this document referred to as HNE) is a new gadget producer that creates headphones, with a special emphasis on their products’ sustainability. The founder of the company has expressed difficulties in keeping track of placed orders, financing revenue, and managing inventory with the amount of orders they are getting. As a result, HNE is planning on implementing a digital system accessible to employees to help with running the store.

At the moment, HNE receives orders in-store, and ships the product later to the customer. The employees write down notes-- physical or electronic-- of the order and customer's details, and passes it to the store manager at the end of the day. This manager is then responsible for inputting the information into a spreadsheet. This spreadsheet is then viewed by employees of the factory division, who create the order and ship it to the address provided. Additionally, as of now, the manager of the factory division is solely responsible for keeping track of the amount of resources they have left, and purchasing more from partnered suppliers should it be necessary.

As a result of this lengthy process made to ensure only trustable, higher-ranking individuals have the permissions to add and edit valuable information, HNE has found that it slow down the efficiency of the company. HNE hence wishes to change this portion of manual labor into a smoother digital system for all employees of HNE to increase their rate of production and revenue.

### Proposed Solution


### Design Statement
Using python and KivyMD I will create a GUI application for HNE in which a user can use to store and manipulate key information for the business on an SQLite Database. The application will take approximately a month to create, and will have the key components/features as listed below in my success criteria.

### Success Criteria
1. The application has a log-in system to distinguish users between an admin and an employer.
   - [issue solved: “There should be a login system.” (2024/02/01 meeting)]
2. The application allows for the user to record and create new orders, and update their shipping status.
   - [issue solved: “The person ordering is going to choose from a few specifications" "The supplier should be able to update (the order's shipping) status” (2024/02/01 meeting)]
3. The user can find details about each order, such as the date ordered, price, and materials used.
   - [issue solved: “If you’re the supplier you can view different orders you have and their content” (2024/02/01 meeting)]
4. The application allows the user to view the store's finances, such as the money raised and spent.
   - [issue solved: “The user should see some sort of summary on how much money he has invested into the materials he is ordering” (2024/02/01 meeting)]
5. The application allows the user to track the store's inventory, such as viewing the amount left and buying more resources.
   - [issue solved: "Since each order needs materials that should also be tracked" (2024/02/01 meeting)]
6. The application can calculate a score that indicates the sustainability of the product a customer orders, and calculate an average score for the month.
   - [issue solved: "A sustainability scale when people pick out their material would be very cool." (2024/02/01 meeting)]

#### Client Approval of Success Criteria
![](assets/success_criteria_proof1.png)
**Fig.1** *Email to client proposing success criteria*

![](assets/success_criteria_proof2.png)
**Fig.2** *Reply of approval from client*

## Criteria B: Design
### System Diagram
![](assets/unit3_system_diagram.png)
**Fig.3** *System diagram of proposed solution*

### Application Wireframe
<iframe style="border: 1px solid rgba(0, 0, 0, 0.1);" width="800" height="450" src="https://www.figma.com/embed?embed_host=share&url=https%3A%2F%2Fwww.figma.com%2Ffile%2Futc6ePhsfo0sHDL2E9SGdy%2FUnit-3-Wireframe%3Ftype%3Ddesign%26node-id%3D37%253A805%26mode%3Ddesign%26t%3DeRKIabr4ogkip19t-1" allowfullscreen></iframe>
**Fig.4** *Wireframe of the application design, created on Figma using components from Wireframes Kit [Free] by Nailul Izah (https://www.figma.com/community/file/1122167340874425914)*

### UML Diagram
![](assets/uml_diagram.png)
**Fig.5** *UML diagram of proposed solution*

### ER Diagram
![](assets/er_diagram.png)
**Fig.6** *ER diagram of database*

### Flow Diagrams
![](placeholder.png)
**Fig.7** *Flow diagram of*

![](placeholder.png)
**Fig.8** *Flow diagram of*

![](placeholder.png)
**Fig.9** *Flow diagram of*

### Record of Tasks
| Planned Action                                    | Planned Outcome                                                                                                                                     | Time estimate | Target completion date | Criteria |
|---------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|---------------|------------------------|----------|
| Write problem definition                          | Meet with client and finalize a description of the problem.                                                                                         | 30min         | Feb 1                  | A        |
| Suggest and finalize success criteria with client | Meet with client again and receive feedback on proposed success criteria for the solution.                                                          | 30min         | Feb 5                  | A        |
| Write proposed solution                           | Finalize the success criteria and form a proposed solution to justify the methods that will be used.                                                | 30min         | Feb 6                  | A        |
| Create wireframe for application                  | Plan the frontend structure of the application by creating a wireframe of the app.                                                                  | 2hr           | Feb 8                  | B        |
| Create diagrams                                   | Create UML and ER diagrams to plan the backend structure of the app.                                                                                | 2hr           | Feb 10                 | B        |
| Create test plan                                  | Create a test plan to use when checking if the application works, and is up to standards.                                                           | 15min         | Feb 11                 | B        |
| Create basic screens and link planned screens     | Create basic/blank screens for all planned screens in the application, compile them into a ScreenManager and make it possible to move between each. | 1hr           | Feb 12                 | C/D      |
| Create login screen                               | Create a login function that retrieves user data from a database, allowing users to log into the application.                                       | 1hr           | Feb 13                 | C/D      |
| Create employee manager screen                    | Create an employee manager screen that allows admin users to view and edit existing employees, as well as create new employee accounts.             | 1hr           | Feb 15                 | C/D      |
| Create inventory screen                           | Create an inventory screen that allows users to view the amount of resources in stock, and allows admin users to puchase more resources.            | 2hr           | Feb 20                 | C/D      |
| Create order creation screen                      | Create an order creation function that allows users to create a new order and save it to a table of all orders.                                     | 1hr 30min     | Feb 22                 | C/D      |
| Create order details screen                       | Create an order details screen that allows users to view the details of a given order in the table.                                                 | 1hr 30min     | Feb 24                 | C/D      |
| Create order list screen                          | Create an order list screen that lists all of the orders in the table, and links to the order details screen of each unique order.                  | 1hr 30min     | Feb 26                 | C/D      |
| Create finance manager screen                     | Create an finance manager screen that allows users to view all transactions made, filterable by date, type, and amounts.                            | 1hr           | Feb 28                 | C/D      |
| Run tests                                         | Run tests as specified in the Test Plan, and fix bugs acoordingly.                                                                                  | 2hr           | Mar 1                  | B/C/D    |
| Adjust and finalize UI                            | Adjust UI (e.g. size, layout) to promote user friendliness, stylize to promote company brand image.                                                 | 1hr 30min     | Mar 3                  | C/D      |
| Run tests again                                   | Run tests as specified in the Test Plan again to ensure that any changes made to UI didn't interfere with functionality.                            | 30min         | Mar 3                  | B        |
| Meet with client for evaluation                   | Meet with client for a final evaluation on the application as a solution to the problem.                                                            | 30min         | Mar 10                 | A/D      |

### Test Plan

## Criteria C: Development
### Techniques used
1. If/Else Statements
2. For/While Loops
3. Input Validation
4. Functions
5. Classes, encapsulation and decapsulation
6. Hashing
7. Databases

### Modules/Libraries used
1. hashlib