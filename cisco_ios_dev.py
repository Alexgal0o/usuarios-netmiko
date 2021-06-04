from jinja2 import Template,utils
from netmiko import ConnectHandler
from tabulate import tabulate
from termcolor import colored
from prettytable import PrettyTable
import os

class Router():
    
    def __init__(self,credential):
        self.credential = credential
    
    def connect(self):
        
        print("Conectando a:",self.getIP(),'...')
        self.conn = ConnectHandler(**self.credential)
        self.conn.enable()
        #print(self.getHostname())
        #print('Fin')
        print(colored(f"{self.getIP()} ({self.getHostname()}) conectado",'green'))

    def getHostname(self):
        
        hostname = self.conn.send_command(Commands.showHostname)
        hostname = hostname.split()
        return hostname[1]

    def getIP(self):
        return self.credential['host']

    def getUsers(self, running = True):
        #show run | include username
        output = self.conn.send_command(Commands.showUsers(running))
        users = []
        
        for credentials in output.splitlines():
            if credentials == "":
                continue
            user = credentials.split()[1]
            users.append(user)
        
        return users
    
    def getPasswords(self, running = True):
        #show run | include username
        output = self.conn.send_command(Commands.showUsers(running))
        users = []
        for credentials in output.splitlines():
            if credentials == "":
                continue
            userCredentials = credentials.split()
            user = userCredentials[1]
            password = userCredentials[4]
            users.append([user,password])
        return users
    
    def addUser(self,user,secret):
       
        output = self.conn.send_config_set(Commands.addUser(user,secret))
        
        print(Commands.okmsg,f" {self.getHostname}: Se ha agregado el usuario")

            

    def userExists(self,user):
        
        users = self.getUsers()
        if user in users:
            return True
        else:
            return False

    def deleteUser(self, user):
        command = "no username "+user
        output = self.conn.send_config_set(command)
        print(Commands.okmsg,f" {self.getHostname()}: Se ha eliminado el usuario")
      

    def saveConfig(self):
        output = self.conn.send_command(Commands.save)
        print(Commands.okmsg,f" {self.getHostname()}: Configuración guardada con éxito")
        return output   

    def getCfg(self):
        output = self.conn.send_command(Commands.showStart)
        return output
    
    def backup(self, path="backup/"):

        script_path = os.path.abspath(__file__) # i.e. /path/to/dir/foobar.py
        script_dir = os.path.split(script_path)[0] #i.e. /path/to/dir/
        rel_path = path+self.getHostname()+".cfg"
        abs_file_path = os.path.join(script_dir, rel_path)

        dest = path+self.getHostname()+".cfg"
        file = open(abs_file_path,'w+')
        file.write(self.getCfg())
        file.close()
        print(Commands.okmsg,f' {self.getHostname()}: Confuguración respaldada')


    

class Commands():

    runShowUsers = "show run | include username"
    startShowUsers = "show start | include username"
    save = "write"
    showHostname = "show run | include hostname"
    showRunning = "show run"
    showStart = "show start"
    
    okmsg = "["+colored("OK","green")+"]"
    attentionmsg = "["+colored("!","yellow")+"]"


    def addUser(user,secret):
        template = "user {{user}} secret {{secret}}" 
        t = Template(template)
        return t.render(user = user, secret = secret)
    
    def showUsers(running = True):

        if running:
            return Commands.runShowUsers
        else:
            return Commands.startShowUsers
    


class RoutersMGMT():
    
    def __init__(self,routersCredentials):
       self.routerCredential =  routersCredentials
       self.connectedDevice = []    

    def startConnection(self):
        print("Conectando a dispositivos...")
        devicesNumber = len(self.routerCredential)
        
        for iteration, credential in enumerate(self.routerCredential):
            
            print(f'[Dispositivo {iteration+1}/{devicesNumber}]')

            try:
                router = Router(credential)
                router.connect()
                self.connectedDevice.append(router)
                continue
            except:
                print(colored("ERROR: no se pudo conectar al dispositivo",'red'))
                continue
    
    def getUsers(self,running = True):
        if running:
            titulo = 'MOSTRANDO USUARIOS DE RUNNING-CONFIG'
        else:
            titulo = 'MOSTRANDO USUARIOS DE STARTUP-CONFIG'
        
        print(titulo)
        for router in self.connectedDevice:
            title = router.getHostname() + " ("+router.getIP()+")"
            header = ['USUARIOS']
            data = [router.getUsers(running)]
            print(colored(8*"="+" "+title+" "+8*"=",'yellow'))
            print(tabulate(data,headers=header))
    
    def getPasswords(self,running = True):
        if running:
            titulo = 'MOSTRANDO USUARIOS DE RUNNING-CONFIG'
        else:
            titulo = 'MOSTRANDO USUARIOS DE STARTUP-CONFIG'
        
        print(titulo)
        for router in self.connectedDevice:
            title = router.getHostname() + " ("+router.getIP()+")"
            header = ['USUARIO','PASSWORD']
            data = router.getPasswords(running=False)
            print(colored(8*"="+" "+title+" "+8*"=",'yellow'))
            print(tabulate(data,headers=header))
    
    def addUser(self,user,password):

        for router in self.connectedDevice:
            if not router.userExists(user):
                router.addUser(user,password)
            else:
                print(Commands.attentionmsg,f" {router.getHostname}: Usuario ya existe actualmente")
    
    def deleteUser(self,user):

        for router in self.connectedDevice:
            if router.userExists(user):
                router.deleteUser(user)
            else:
                print(Commands.attentionmsg,f" {router.getHostname}: Usuario no existe")

    def saveConfig(self):
        for router in self.connectedDevice:
            router.saveConfig()
            
    def backup(self,path="backup/"):

        for router in self.connectedDevice:
            router.backup()