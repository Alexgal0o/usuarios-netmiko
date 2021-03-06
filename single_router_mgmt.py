import cisco_ios_dev as cid


cisco_3745 = {
    'device_type': 'cisco_ios',
    'host': '192.168.87.136',
    'username':'cisco',
    'password':'cisco',
    'port':22,
    'secret':'cisco'
}


router = cid.Router(cisco_3745)
router.connect()

def main():
    menu = """

SELECCIONE UNA OPCIÓN:
1) Mostrar Usuarios (startup)
2) Mostrar Usuarios (running)
3) Agregar Usuarios
4) Eliminar Usuarios
5) Guardar Cambios
6) Salir

Selección: """

    while True:
        opcion = input(menu)
        if opcion == "1":
            print("USUARIOS STARTUP:",*router.getUsers(running=False),sep="\n-",end="")

        elif opcion == "2":
            print("USUARIOS RUNNING: ",*router.getUsers(running=True),sep="\n-",end="")

        elif opcion == "3":
            agregarUsuario()

        elif opcion == "4":
            eliminarUsuario()

        elif opcion == "5":
            router.saveConfig()

        elif opcion == "6":
            print("Finalizando sesión...")
            break
        else:
            print("OPCIÓN INCORRECTA: Intente de nuevo")
            continue

def agregarUsuario():
    while True:
        user = input("Ingrese el nombre de usuario (presione '0' para salir): ")
        if user == '0':
            break
        if router.userExists(user):
            print("El usuario ya existe")
            continue
        else:
            secret = input("Ingrese la contraseña: ")
            router.addUser(user,secret)
            print("Usuario agregado con éxito!")

def eliminarUsuario():
    while True:
        user = input("Ingrese el nombre de usuario a eliminar (presione '0' para salir): ")
        if user == '0':
            break
        if not router.userExists(user):
            print("El usuario no existe")
            continue
        else:
            opc = input("Presione 's' para confirmar: ")
            if opc.lower() == 's':
                router.deleteUser(user)
            else:
                print("Acción cancelada")
                continue   


if __name__ == '__main__':
    main()