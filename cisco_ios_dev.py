from jinja2 import Template,utils

class Router():
    
    def __init__(self,connection):
        self.conn = connection
        pass

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
            

    def userExists(self,user):
        
        users = self.getUsers()
        if user in users:
            return True
        else:
            return False
    def deleteUser(self, user):
        command = "no username "+user
        output = self.conn.send_config_set(command)
      

    def saveConfig(self):
        output = self.conn.send_command(Commands.save)
        return output   

    

class Commands():

    runShowUsers = "show run | include username"
    startShowUsers = "show start | include username"
    save = "write"

    def addUser(user,secret):
        template = "user {{user}} secret {{secret}}" 
        t = Template(template)
        return t.render(user = user, secret = secret)
    
    def showUsers(running = True):

        if running:
            return Commands.runShowUsers
        else:
            return Commands.startShowUsers
        