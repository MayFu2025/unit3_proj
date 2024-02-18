## Developer Profile

### Hired! Developing for Jenda's Headphone Business

Hi, thank you for taking interest in my profile. I'm May, a Computer Science Student learning Python, ready to help you make your life easier with my programs.

Although I could pitch myself right here, what not a better way to show you what I can do, than for you to experience it yourself?

For those interested in hiring me, the below code shows an example of how I program a class.
(From file `developer_profile.py`)
```.python
class Developer:
    def __init__(self, name: str, language: str, strengths: list, weaknesses: list):
        self.name = name
        self.language = language
        self.strengths = strengths
        self.weaknesses = weaknesses
        self.job = False

    def add_strengths(self, skill:str):
        self.strengths.append(skill)
        return self.strengths

    def add_weaknesses(self, weak:str):
        self.weaknesses.append(weak)
        return self.weaknesses

    def introduction(self):
        return f'''\nHi, my name is {self.name}! I'm a {self.language} developer, looking to help your business tackle both small and large problems.\nMy strengths are: {', '.join(self.strengths)}\nMy weaknesses are: {', '.join(self.weaknesses)}\n'''

    def hire_me_please(self):
        qm = 1
        while not self.job:
            a = input(f"Would you like to hire me for your company{'?'*qm} (Y/N): ")
            if a in "Yy":
                self.job = True
            else:
                qm += 1
        return "Thank you for hiring me! :D"
```

To see why you should hire me, run the following code after defining the class like I did above.
```.python
May = Developer("May", "Python", ["Resilient", "Quick to learn new things", "Follows instructions", "Enjoys coding"], ["Still a beginner", "Works late at night"])

print(May.introduction())
print(May.hire_me_please())
```

For other examples, please see my Github Profile at MayFu2025. For past projects, please see the repositories "unit_1 project" and "unit2_project".