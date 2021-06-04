import cisco_ios_dev as cid

cisco_3745 = [{
    'device_type': 'cisco_ios',
    'host': '192.168.87.136',
    'username':'cisco',
    'password':'cisco',
    'port':22,
    'secret':'cisco'
},
{
    'device_type': 'cisco_ios',
    'host': '192.168.87.200', #Dirección que acutalmente no existe
    'username':'cisco',
    'password':'cisco',
    'port':22,
    'secret':'cisco'
},
{
    'device_type': 'cisco_ios',
    'host': '192.168.87.137',
    'username':'cisco',
    'password':'cisco',
    'port':22,
    'secret':'cisco'
},
]

connection = cid.RoutersMGMT(cisco_3745)
connection.startConnection()

def actionsMenu(connection):
    menu = """

SELECCIONE UNA OPCIÓN:
1) Mostrar Usuarios (startup)
2) Mostrar Usuarios (running)
3) Agregar Usuarios
4) Eliminar Usuarios
5) Guardar Cambios
6) Respaldar configuración
7) Salir

>: """

    while True:
        opcion = input(menu)
        if opcion == "1":
            connection.getUsers(running=False)

        elif opcion == "2":
            connection.getUsers(running=True)

        elif opcion == "3":
            agregarUsuario(connection)

        elif opcion == "4":
            eliminarUsuario(connection)

        elif opcion == "5":
            connection.saveConfig()

        elif opcion == "6":
            connection.backup()

        elif opcion == "7":
            
            break
        else:
            print("OPCIÓN INCORRECTA: Intente de nuevo")
            continue

def agregarUsuario(connection):
    while True:
        user = input("Ingrese el nombre de usuario (presione '0' para salir): ")
        if user == '0':
            print("Acción cancelada por el usuario")
            break
        else:
            secret = input("Ingrese la contraseña: ")
            connection.addUser(user,secret)

def eliminarUsuario(connection):
    
    while True:
        user = input("Ingrese el nombre de usuario a eliminar (presione '0' para salir): ")
        if user == '0':
            break
        else:
            opc = input("Presione 's' para confirmar: ")
            if opc.lower() == 's':
                connection.deleteUser(user)
            else:
                print("Acción cancelada")
                continue  


if __name__ == '__main__':
    actionsMenu(connection)