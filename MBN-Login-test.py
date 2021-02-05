import cmd
import getpass
import pyfiglet
import time
import re
from os import system
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.firefox.options import Options

#----------------------------------------------------------------------------------------------------

class Color:
    COLORS = {
        "cyan": "\033[0;36m",
        "magenta": "\033[0;35m",
        "green": "\033[0;32m",
        "red": "\033[0;31m",
        "white": "\033[0;37m",
        "yellow": "\033[0;33m",
    }

    def __init__(self, color):
        try:
            self.prefix = self.COLORS[color.lower()]
        except AttributeError:
            raise ValueError("color must be a str")
        except KeyError:
            raise ValueError(f"unknow color, availables colors are {', '.join(self.COLORS)}")

    def __call__(self, text):
        return f"{self.prefix}{text} \033[0m"

#----------------------------------------------------------------------------------------------------

def print_separator(): print(Color("red")("--------------------"))
def print_figlet(color, text): print(Color(color)(pyfiglet.figlet_format(text)))
def start_text(): print_figlet("red", "MBN-Login")
def clear(): system('clear')

def stop(): 
    clear()
    exit()

#----------------------------------------------------------------------------------------------------

class MonBureauNumeriqueLogin:


        def __init__(self):
            options = Options()
            #options.add_argument('--headless')
            self.driver = webdriver.Firefox(options = options)
            self.driver.set_window_position(1000, 0)
            self.XPATHs = {
                "acceuil": "/html/body/div[1]/nav/ul[2]/li[1]",
                "Messagerie": "/html/body/div[1]/nav/ul[2]/li[2]",
                "Cahier": "/html/body/div[1]/nav/ul[2]/li[3]",
                "Classeur": "/html/body/div[1]/nav/ul[2]/li[4]",
                "Absences": "/html/body/div[1]/nav/ul[2]/li[5]",
                "Evaluations": "/html/body/div[1]/nav/ul[2]/li[6]",
            }


        def stop_engine(self):
            self.driver.quit()
            stop()


        def wait_for_loading(self):
            try:
                myElem = WebDriverWait(self.driver, 4).until(EC.presence_of_element_located((By.ID, 'html')))
            except TimeoutException:
                print(Color("cyan")("[!] -"))

#----------------------------------------------------------------------------------------------------

        def login(self, username, password):
            try:
                self.driver.get("https://www.monbureaunumerique.fr/")
                self.driver.maximize_window()
                print(Color("yellow")("[*] lance la page"))
                print(Color('cyan')("[!] -"))
                self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/a[2]").click()
                self.driver.find_element_by_xpath("/html/body/main/div/div/div[1]/div/div/form/div[1]/div/label").click()
                print(Color("green")("[*] Choix de connection"))
                self.driver.find_element_by_xpath("/html/body/main/div/div/div[1]/div/div/form/div[3]/input[2]").click()
                self.wait_for_loading()
                print(Color("magenta")("[*] Connection en cours"))
                self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/form/div[1]/input").send_keys(username)
                self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/form/div[2]/input").send_keys(password)
                self.driver.find_element_by_xpath("/html/body/div[2]/div[1]/form/div[3]/button").click()
                self.wait_for_loading()
                self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/button").click()
                self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/ul/li[1]/a").click()                
                print(Color("red")("[*] Connecté"))
                return True
            except KeyboardInterrupt:
                self.stop_engine()
                return False

#----------------------------------------------------------------------------------------------------

        def menu(self, arg):

            xpath = self.XPATHs.get(arg)

            try:
                self.driver.find_element_by_xpath(xpath).click()
            except KeyboardInterrupt:
                self.stop_engine()
                return False

#----------------------------------------------------------------------------------------------------     

        def moodle(self):

            regex = r"https:\/\/lyc-([a-zA-Z1-9]+)\.monbureaunumerique\.fr.*"

            test_str = self.driver.current_url

            matches = re.finditer(regex, test_str, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
    
                for groupNum in range(0, len(match.groups())):
                    groupNum = groupNum + 1
        
            self.driver.get("https://lyc-" + "{group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)) + ".monbureaunumerique.fr/sg.do?PROC=MOODLE")

#----------------------------------------------------------------------------------------------------

engine = MonBureauNumeriqueLogin()

#----------------------------------------------------------------------------------------------------

class PromptShell(cmd.Cmd):

    prompt = Color("red")(">>>>>")

    def __init__(self):
        super(PromptShell, self).__init__()
        print_separator()


    def do_Close(self, arg):
        "Commande pour éteindre le programme et fermer la page mbn"
        engine.stop_engine()


    def do_Clear(self, arg):
        "Commande pour clear le terminal"
        clear()


    def do_Accueil(self, arg):
        "Commande pour aller a l'accueil"
        engine.menu("accueil")


    def do_Messagerie(self, arg):
        "Commande pour aller a la messagerie"
        engine.menu("Messagerie")


    def do_Cahier(self,arg):
        "Commande pour aller au cahier de texte"
        engine.menu("Cahier")


    def do_Classeur(self,arg):
        "Commande pour aller au classeur pedagogique"
        engine.menu("Classeur")


    def do_Absences(self,arg):
        "Commande pour aller au absences"
        engine.menu("Absences")


    def do_Evaluations(self,arg):
        "Commande pour aller voir ses notes O_o"
        engine.menu("Evaluations")


    def do_Moodle(self,arg):
        "Commande pour aller a moodle"
        engine.moodle()

#----------------------------------------------------------------------------------------------------

def main():
    clear()
    start_text()
    try:
        while True:
            username = input("Username: ")
            password = getpass.getpass()
            if len(password) < 0:
                print_separator()
                continue
            print_separator()

            if engine.login(username, password) == False: 
                print_separator()
                continue
            else:
                shell = PromptShell()
                shell.cmdloop()
            break
    except KeyboardInterrupt:
        stop()

if __name__ == "__main__":
    main()

#----------------------------------------------------------------------------------------------------