from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from customer import VipClient
from customer import Client
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce
import shutil
from tabulate import tabulate     #pedirle a chat gpt que me haga los cuadros con tabulate en Ventas consultar
from components import Valida

# Función para dibujar un marco especial en la consola
def draw_custom_frame():
    borrarPantalla()
    print(purple_color + "╔" + "═" * 95 + "╗")
    for _ in range(35):
        print("║" + " " * 95 + "║")
    print("╚" + "═" * 95 + "╝" + reset_color)
    
def determine_client_type(valor):
    if valor > 0:
        return "VIP"
    else:
        return "Regular"

  #cantidad de cliente con la de max, mi
path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion           #falta validar que se ingrese solo 10 numeros 
class CrudClients(ICrud):
    @Valida.validate_10_digits
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(43, 3); print(purple_color+"𝓡𝓮𝓰𝓲𝓼𝓽𝓻𝓪𝓻 𝓬𝓵𝓲𝓮𝓷𝓽𝓮")
        gotoxy(8, 4); print("____________________________________________________________________________________")

        json_file = JsonFile(os.path.join(path, 'archivos', 'clients.json'))
        clients_data = json_file.read()
        client_to_update = None

        while True:
            gotoxy(8, 6); print(reset_color+"Ingrese los datos del nuevo cliente:")
            gotoxy(8, 8); print(purple_color+"Cedula:")
            gotoxy(16, 8); dni = validar.cedula(red_color+"")
            
            # Verificar si la cédula ya existe en los datos existentes
            cedula_existente = False
            for client_data in clients_data:
                if client_data["dni"] == dni:
                    cedula_existente = True
                    break

            if cedula_existente:
                gotoxy(8, 9)
                print(red_color+"La cédula ingresada ya está registrada. Intente nuevamente.")
                time.sleep(2)
                gotoxy(8, 9)
                print(" "*90)
            else:
                break

        gotoxy(8, 10); print(purple_color+"Nombre:")
        gotoxy(18, 10); nombre = validar.solo_letras(reset_color+"Ingrese el nombre del nuevo cliente: ", red_color+"Solo letras.")
        if len(nombre) < 2 or len(nombre) > 20:  # Establece el rango de longitud del nombre
            while True:
                gotoxy(8, 12); print(red_color+"El nombre debe tener entre 2 y 30 caracteres.")
                nombre = validar.solo_letras(reset_color+"Ingrese el nombre del nuevo cliente: ", red_color+"Solo letras.")
                if 2 <= len(nombre) <= 30:
                    break
                gotoxy(8, 12); print(" " * 75)
        gotoxy(8, 14); print(purple_color+"Apellido:")
        gotoxy(18, 14); apellido = validar.solo_letras(reset_color+"Ingrese el apellido del nuevo cliente: ", red_color+"Solo letras.")
        if len(apellido) < 2 or len(apellido) > 20:  # Establece el rango de longitud del apellido
            while True:
                gotoxy(8, 17); print(red_color+"El apellido debe tener entre 2 y 30 caracteres.")
                apellido = validar.solo_letras(cyan_color+"Ingrese el apellido del nuevo cliente: ", red_color+"Solo letras.")
                if 2 <= len(apellido) <= 20:
                    break
                gotoxy(8, 17); print(" " * 75)
        gotoxy(8,19);is_vip = input(purple_color+"¿El cliente es VIP? (s/n): ").lower() == "s"

        gotoxy(8,21);confirmar = input(purple_color+"¿Está seguro de que desea registrar este cliente? (s/n): ")
        if confirmar.lower() != "s":
            gotoxy(28,22);print(red_color+"Registro cancelado.")
            return  # Salir del método si la confirmación es negativa

    # Crear instancia de cliente según la respuesta
        if is_vip:
            cliente = VipClient(nombre, apellido, dni)
        else:
            cliente = RegularClient(nombre, apellido, dni)

        # Leer los datos existentes del archivo JSON
        json_file = JsonFile(path + '/archivos/clients.json')
        clients_data = json_file.read()

        # Guardar los datos del nuevo cliente en la lista clients_data
        clients_data.append(cliente.getJson())    

        # Guardar los datos en el archivo JSON
        json_file.save(clients_data)

        gotoxy(24, 23); print(reset_color+" 😊 Cliente registrado correctamente. 😊")
        time.sleep(7)
    
#---------------------------------------------------------------------------------        
#ya esta hecha, valdada solo falta el marco un poco más abajo
    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(40, 2); print(yellow_color+"𝓜𝓸𝓭𝓲𝓯𝓲𝓬𝓪𝓻 𝓒𝓵𝓲𝓮𝓷𝓽𝓮")
        gotoxy(8, 3); print("____________________________________________________________________________________")

        json_file = JsonFile(path + '/archivos/clients.json')
        clients_data = json_file.read()
        client_to_update = None

        while True:
            gotoxy(8, 5); print(yellow_color+"Cedula:")
            gotoxy(22, 5); dni = validar.solo_numeros(red_color+"Solo números.", 20, 5)

            for client_data in clients_data:
                if client_data["dni"] == dni:
                    client_to_update = client_data
                    break

            if client_to_update:
                break  # Salir del bucle si se encuentra un cliente con la cédula proporcionada
            else:
                gotoxy(8, 7); print(red_color+"Cliente no encontrado. Intente nuevamente.")
                time.sleep(2)
                gotoxy(8, 7); print(" " * 75)


        gotoxy(8, 8); print(yellow_color+"Datos del cliente a actualizar:")
        gotoxy(8, 10); print(reset_color+f"  DNI: {client_to_update['dni']}")
        gotoxy(8, 11); print(reset_color+f"  Nombre: {client_to_update['nombre']}")
        gotoxy(8, 12); print(reset_color+f"  Apellido: {client_to_update['apellido']}")

        gotoxy(8, 14); print(yellow_color+"Ingrese los nuevos datos:")
        gotoxy(8, 15);nombre = validar.solo_letras(blue_color+"Ingrese nuevo nombre (deje vacío para conservar): ", red_color+"Solo letras.")
        if nombre is None:
            nombre = client_to_update['nombre']   # Conservar el nombre actual si el usuario no lo actualiza
        gotoxy(8, 18);apellido = validar.solo_letras(blue_color+"Ingrese nuevo apellido (deje vacío para conservar):", red_color+"Solo letras.")
        if apellido is None:
            apellido = client_to_update['apellido']
        gotoxy(9, 21);print(blue_color+"------> | Nueva Cedula: (deje vacío para conservar):")
        gotoxy(30, 21); nueva_dni = validar.solo_numeros(red_color+"Solo números.", 62, 21)
        while True:
            gotoxy(9, 21);print(blue_color+"------> | Nueva Cedula: (deje vacío para conservar):")
            gotoxy(30, 21); nueva_dni = validar.solo_numeros(red_color+"Solo números.", 62, 21)
            if nueva_dni is None:
                nueva_dni = client_to_update['dni']
                break  # Salir del bucle si el usuario deja el campo vacío (para conservar la cédula actual)
            # Verificar si la nueva cédula es válida

            if len(nueva_dni) == 10 and nueva_dni.startswith("09"):
                # Verificar si la nueva cédula ya está en uso
                if any(client_data["dni"] == nueva_dni for client_data in clients_data):
                    gotoxy(8, 23); print(red_color+"La nueva cédula ya está en uso. Intente nuevamente.")   #primero ponero uno que manual y de ahi uno de clients.json xd
                    time.sleep(2)
                else:
                    client_to_update['dni'] = nueva_dni
                    break  # Salir del bucle si la cédula es válida y no está en uso
            else:
                gotoxy(8, 23); print(red_color+"La nueva cédula debe tener 10 dígitos y comenzar con '09'. Intente nuevamente.")
                time.sleep(2)

        client_to_update['nombre'] = nombre
        client_to_update['apellido'] = apellido
        client_to_update['dni'] = dni
        # Confirmación y actualización del producto
        gotoxy(8, 23);confirmar = input(yellow_color+"¿Está seguro de que desea actualizar este producto? (s/n): ")
        if confirmar.lower() == "s":
            # Actualizar los datos del producto en la lista de clientes
            json_file.save(clients_data)
            gotoxy(12, 25);print(yellow_color+"_____________________________________________________________________")
            gotoxy(28, 26); print("😊 Cliente actualizado correctamente 😊")
            time.sleep(3)
        elif confirmar.lower() == "n":
            gotoxy(8, 25)
            print("Actualización cancelada.")
            print("")
            time.sleep(2)

        
#-----------------------------------------------------------------------------------
    #validar veuleve al menu principal 1
    def delete(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(36, 3);print(purple_color+"𝓔𝓵𝓲𝓶𝓲𝓷𝓪𝓻 𝓒𝓵𝓲𝓮𝓷𝓽𝓮")
        gotoxy(8, 4);print("____________________________________________________________________________________")
        while True:
            gotoxy(8, 6)
            print("Cedula:")
            gotoxy(22, 6)
            dni = validar.solo_numeros(red_color+"Solo números.", 20, 6)

            json_file = JsonFile(path + '/archivos/clients.json')
            clients_data = json_file.read()
            client_to_delete = None

            for client_data in clients_data:
                if client_data["dni"] == dni:
                    client_to_delete = client_data
                    break  # Salir del bucle cuando se encuentre el cliente

            if client_to_delete:
                gotoxy(8, 9)
                print(purple_color+"Datos del cliente a eliminar:")
                gotoxy(8, 11)
                print(reset_color +f"DNI: {client_to_delete['dni']}")
                gotoxy(8, 12)
                print(reset_color +f"Nombre: {client_to_delete['nombre']}")
                gotoxy(8,13)
                print(reset_color +f"Apellido: {client_to_delete['apellido']}")

                gotoxy(8,15)
                confirmacion = input(purple_color+"¿Estás seguro de que deseas eliminar este cliente? (s/n): ")
                if confirmacion.lower() == "s":
                    clients_data.remove(client_to_delete)
                    json_file.save(clients_data)

                    gotoxy(8,16);print("------------------------------------------------------------")
                    gotoxy(24, 17)
                    print(reset_color+"😊 Cliente eliminado correctamente. 😊")
                else:
                    gotoxy(28, 17)
                    print(red_color+"Eliminación cancelada.")
                    time.sleep(2)
                    gotoxy(12, 17); print(" " * 75)
            else:
                gotoxy(26, 8)
                print(red_color+"Cliente no encontrado.")
                time.sleep(2)
                gotoxy(12, 8); print(" " * 75)

            gotoxy(8, 19);opcion = input(purple_color+"¿Desea eliminar otro cliente? (s/n): ")
            if opcion.lower() != "s":
                break
            time.sleep(3)
            gotoxy(8,19); print(" "*75)  # Salir del bucle si el usuario no desea eliminar otro cliente

#----------------------------------------------------    consulta generaal o consulta especifica
    # total valor de los clientes, cliente con mayor valor, cliente con menor valor
    def consult(self):
        borrarPantalla()
        print('\033c', end='')  # Limpiar la pantalla
        draw_custom_frame()
        gotoxy(2, 1)
        gotoxy(42, 3);print(blue_color+"𝓒𝓸𝓷𝓼𝓾𝓵𝓽𝓪𝓻 𝓒𝓵𝓲𝓮𝓷𝓽𝓮")
        gotoxy(8, 4);print("____________________________________________________________________________________")

        
        # Leer el JSON de los clientes
        json_file = JsonFile(path + '/archivos/clients.json')
        clients = json_file.read()

        while True:
            gotoxy(8, 6)
            print("\033[36m1. Consultar cliente por DNI")
            gotoxy(8, 7)
            print("\033[36m2. Mostrar toda la lista de clientes")
            gotoxy(8, 8)
            option = input("\033[34mSeleccione una opción (1/2): ")

            if option == "1":
                gotoxy(8, 10)
                while True:
                    gotoxy(10, 10)
                    dni = input("\033[36mIngrese el DNI del cliente que desea consultar: ")
                    if dni.isdigit():
                        dni = int(dni)
                        break
                    else:
                        gotoxy(10, 11)
                        print("\033[31mSolo números")

                # Buscar el cliente por su DNI y mostrar sus detalles
                client_found = False
                for client in clients:
                    if client.get("dni") is not None and int(client["dni"]) == dni:
                        client_found = True
                        gotoxy(12, 13)
                        print("\033[31mDetalles del cliente:")
                        gotoxy(12, 14)
                        print("\033[34mDNI:", client["dni"])
                        gotoxy(12, 15)
                        print("\033[34mNombre:", client["nombre"])
                        gotoxy(12, 16)
                        print("\033[34mApellido:", client["apellido"])
                        if "valor" in client:
                            gotoxy(12, 17)
                            print("\033[34mValor:", client["valor"])
                        break

                if not client_found:
                    gotoxy(8, 18)
                    print("\033[31mNo se encontró ningún cliente con el DNI especificado.")

                gotoxy(8,19);input("\033[36mPresione una tecla para continuar...")
                break

            elif option == "2":
                # Mostrar toda la lista de clientes
                start_row = 12  # Definir la fila donde empieza a imprimirse la lista de clientes
                gotoxy(8, start_row)
                print("\033[34mLista de Clientes:")
                header_row = start_row + 1
                gotoxy(8, header_row)
                print(cyan_color + "┌───────────┬────────────┬──────────────┬──────────┬────────┐")
                gotoxy(8, header_row + 1)
                print(cyan_color + "│    DNI    │   Nombre   │  Apellido    │   Valor  │  Tipo  │")
                gotoxy(8, header_row + 2)
                print(cyan_color + "├───────────┼────────────┼──────────────┼──────────┼────────┤")

                row = header_row + 3  # Iniciar desde la siguiente fila después del encabezado
                total_valor_clientes = 0  # Inicializar el total de valor de clientes
                valores_clientes = []  # Lista para almacenar los valores de los clientes

                for client in clients:
                    dni = client.get('dni', '')
                    nombre = client.get('nombre', '')
                    apellido = client.get('apellido', '')
                    valor = client.get('valor', '')

                    # Calcular el total de valor de clientes
                    if valor is not None and isinstance(valor, (int, float)):
                        total_valor_clientes += valor

                    # Agregar el valor del cliente a la lista
                    if valor is not None:
                        valores_clientes.append(valor)

                    client_type = determine_client_type(valor)  # Determinar el tipo de cliente (VIP o Regular)

                    if dni is None:
                        dni = ''
                    if nombre is None:
                        nombre = ''
                    if apellido is None:
                        apellido = ''
                    if valor is None:
                        valor = ''

                    gotoxy(8, row)
                    print(cyan_color + f"│{dni:^11}│{nombre:^12}│{apellido:^14}│{valor:^10}│{client_type:^8}│")
                    row += 1  # Incrementar la posición vertical para el siguiente cliente

                # Imprimir el total de valor de clientes
                gotoxy(8, row)
                print(cyan_color + "└───────────┴────────────┴──────────────┴──────────┴────────┘")
                row += 1  # Incrementar una fila más para el mensaje del total
                gotoxy(8, row)
                print(f"\033[34mTotal Valor de Clientes: {total_valor_clientes}")

                # Imprimir el cliente con el mayor valor
                if valores_clientes:
                    max_valor_cliente = max(valores_clientes)
                    gotoxy(8, row + 1)
                    print(f"\033[34mCliente con Mayor Valor: {max_valor_cliente}")

                # Imprimir el cliente con el menor valor
                if valores_clientes:
                    min_valor_cliente = min(valores_clientes)
                    gotoxy(8, row + 2)
                    print(f"\033[34mCliente con Menor Valor: {min_valor_cliente}")

                input("\033[34mPresione una tecla para continuar...")

           
#-------------------------------------------------------------------------------------------        
class CrudProducts(ICrud):
    def create(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(41, 3)
        print(green_color+"𝓡𝓮𝓰𝓲𝓼𝓽𝓻𝓪𝓻 𝓟𝓻𝓸𝓭𝓾𝓬𝓽𝓸")

        # Cargar los datos de productos desde el archivo JSON
        json_file = JsonFile(path + '/archivos/products.json')
        productos_data = json_file.read()

        # Solicitar datos del nuevo producto
        gotoxy(8, 6)
        print("Ingrese los datos del nuevo producto:")

        # ID
        gotoxy(8, 8)
        print("ID:")
        while True:
            gotoxy(22, 8)
            id_producto = validar.solo_numeros("Solo números.", 20, 8)

            # Convertir el ID ingresado a entero
            id_producto = int(id_producto)

            # Verificar si el ID existe en la lista de productos
            producto_encontrado = False
            for producto in productos_data:
                if producto["id"] == id_producto:
                    producto_encontrado = True
                    break
                    
            # Verificar si el ID ya existe en la lista de productos
            if producto_encontrado:
                gotoxy(8, 9)
                print(red_color+"Error: El ID ingresado ya está en uso. Por favor, ingrese un ID diferente ")
                gotoxy(8,10);input(green_color+"Presione una tecla para continuar...")
                time.sleep(2)
                gotoxy(8, 9);print(" " * 90)  # Limpiar el campo de entrada del ID
                gotoxy(8,10);print(" " * 90)  # Limpiar el campo de entrada del ID
            else:
                break

        # Descripción
        gotoxy(8, 12);print("Descripción:")
        while True:
            gotoxy(25, 12);descripcion_producto = validar.solo_letras(reset_color+"Ingrese la descripción del nuevo producto: ", red_color+"Solo letras.")
    
    # Cargar los datos de productos desde el archivo JSON
            json_file = JsonFile(path + '/archivos/products.json')
            productos_data = json_file.read()

    # Verificar si la descripción ya existe en la lista de productos
            descripcion_existente = any(producto["descripcion"].lower() == descripcion_producto.lower() for producto in productos_data)
            if descripcion_existente:
                gotoxy(8, 15);print(red_color+"La descripción ingresada ya está en uso. Por favor, ingrese una descripción diferente.")
                time.sleep(2)
                gotoxy(8, 15)
                print(" " * 90)  # Limpiar el mensaje de error
                gotoxy(20, 12)
                print(" " * len(descripcion_producto))  # Limpiar la entrada de descripción
            else:
                break  # Salir del bucle si la descripción es válida        

    # Precio
        gotoxy(8, 17);print("Precio:")
        gotoxy(15, 17);precio_producto = validar.solo_decimales(reset_color+"Ingrese el precio del nuevo producto: ", red_color+"Solo números decimales.")

    # Stock
        gotoxy(8, 20)
        print("Stock:")
        gotoxy(18, 22)
        stock_producto = validar.solo_numeros("Solo números.", 20, 20)

    # Confirmación y guardado del producto
        gotoxy(8, 24)
        confirmar = input(green_color+"¿Está seguro de que desea registrar este producto? (s/n): ")
        if confirmar.lower() != "s":
            print("Registro cancelado.")
        else:

    # Guardar el nuevo producto en el archivo JSON
            nuevo_producto = {"id": id_producto, "precio": precio_producto, "descripcion": descripcion_producto, "stock": stock_producto}
            productos_data.append(nuevo_producto)
            json_file.save(productos_data)

    # Mensaje de confirmación
            gotoxy(12,28);print("***************************************************")
            gotoxy(20, 29);print(green_color+" 😊 Producto registrado correctamente. 😊")
            time.sleep(7)
#---------------------------------------------------------------------------------------
    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(3, 3)
        print("𝓐𝓬𝓽𝓾𝓪𝓵𝓲𝔃𝓪𝓻 𝓟𝓻𝓸𝓭𝓾𝓬𝓽𝓸")
        gotoxy(8, 4);print("____________________________________________________________________________________")

        json_file = JsonFile(path + '/archivos/products.json')
        productos_data = json_file.read()
    
        while True:
                # Solicitar el ID del producto a actualizar
                gotoxy(8, 6)
                id_producto = input("Ingrese el ID del producto a actualizar: ")
                if not id_producto.isdigit():
                    gotoxy(8, 7)
                    print(red_color+"Error: Ingrese solo números.")
                    input(blue_color+"Presione una tecla para continuar...")
                    continue
                
                id_producto = int(id_producto)    
                # Verificar si el ID existe en la lista de productos
                producto_encontrado = False
                for producto in productos_data:
                    if producto["id"] == id_producto:
                        producto_encontrado = True
                        break
                    
                # Mostrar mensaje de error si el ID no se encuentra
                if not producto_encontrado:
                    gotoxy(8, 8)
                    print(red_color+"Error: El producto con el ID ingresado no fue encontrado.")
                    gotoxy(8,9);input(blue_color+"Presione una tecla para continuar...")
                    continue
                
                # Mostrar los detalles del producto antes de actualizar
                gotoxy(8, 11)
                print(cyan_color+"Detalles del producto a actualizar:")
                for producto in productos_data:
                    if producto["id"] == id_producto:
                        gotoxy(10, 12)
                        print(f"ID: {producto['id']}")
                        gotoxy(10, 13)
                        print(f"Descripción: {producto['descripcion']}")
                        gotoxy(10, 14)
                        print(f"Precio: {producto['precio']}")
                        gotoxy(10, 15)
                        print(f"Stock: {producto['stock']}")
                        break   
                    
                # Solicitar la información actualizada del producto

                gotoxy(8, 17);print(blue_color + "Ingrese la información actualizada del producto:")

                # Descripción
                gotoxy(8, 18) # gotoxy(15, 10); nombre = validar.solo_letras("Ingrese el nombre del nuevo cliente: ", "Solo letras.")
                print(cyan_color+"Nueva Descripción (deje vacío si no desea actualizar): ")
                gotoxy(64, 18); nueva_descripcion = validar.solo_letras(" ",red_color+"Solo letras.")
                if nueva_descripcion is None:
                    nueva_descripcion = producto['descripcion']

                # Nuevo Precio
                gotoxy(8, 21);print(cyan_color+"Nuevo Precio (deje vacío si no desea actualizar): ")
                gotoxy(60, 21)
                nuevo_precio = validar.solo_decimales(red_color+" ", "Solo decimales.")
                if nuevo_precio is None:
                    nuevo_precio = producto['precio']

                # Nuevo Stock
                gotoxy(8, 25)
                print(cyan_color+"Nuevo Stock (deje vacío si no desea actualizar): ")
                gotoxy(60, 25)
                nuevo_stock = validar.solo_numeros("Ingrese un número válido: ", 60, 25)

                if nuevo_stock is None:
                    nuevo_stock = producto['stock']   

                # Confirmación y actualización del producto
                gotoxy(8,27);confirmar = input("¿Está seguro de que desea actualizar este producto? (s/n): ")

                if confirmar.lower() == "s":
                    # Actualizar los datos del producto en la lista de productos
                    producto['descripcion'] = nueva_descripcion
                    producto['precio'] = float(nuevo_precio)
                    producto['stock'] = int(nuevo_stock)

                    # Guardar los cambios en el archivo JSON
                    json_file.save(productos_data)
                    # Mostrar mensaje de confirmación
                    gotoxy(8, 28)
                    print("Producto actualizado correctamente.")
                    time.sleep(3)
                else:
                    gotoxy(8, 29)
                    print("Actualización cancelada.")
                    print("")
                break  # Salir del bucle después de procesar el producto

 #--------------  --------------------------------------------------------------   
    def delete(self):
        borrarPantalla()
        validar = Valida()
        print('\033c', end='')  # Limpiar la pantalla
        draw_custom_frame()
        gotoxy(42, 3);print(red_color+"𝓔𝓵𝓲𝓶𝓲𝓷𝓪𝓻 𝓟𝓻𝓸𝓭𝓾𝓬𝓽𝓸")
        gotoxy(8, 4);print("____________________________________________________________________________________")


        # Leer el JSON de los productos
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.read()
                
        # Buscar el producto por su ID y mostrar su descripción
        product_to_delete = None
        while product_to_delete is None:
            # Solicitar al usuario que ingrese el ID del producto a eliminar
            gotoxy(8,6);print(green_color+"ID:")
            product_id = int(validar.solo_numeros("Ingrese el ID del producto que desea eliminar: ",12,6))

            # Buscar el producto por su ID y mostrar su descripción
            for product in products:
                if int(product["id"]) == product_id:
                    product_to_delete = product
                    gotoxy(8, 10)
                    print(red_color+"Detalles del producto a eliminar:")
                    gotoxy(10, 1)
                    print(green_color+f"ID: {product['id']}")
                    gotoxy(10, 12)
                    print(f"Descripción: {product['descripcion']}")
                    gotoxy(10, 13)
                    print(f"Precio: {product['precio']}")
                    gotoxy(10, 14)
                    print(f"Stock: {product['stock']}")
                    break

            if product_to_delete is None:
                gotoxy(10, 18);print("No se encontró ningún producto con el ID especificado.")
                gotoxy(10, 19);input("Presione una tecla para continuar...")

        # Confirmar la eliminación con el usuario
        gotoxy(9,16);confirmacion = input(red_color+"¿Estás seguro de que quieres eliminar este producto? (s/n): ").lower()
        if confirmacion == 's':
            products.remove(product_to_delete)
            json_file.save(products)
            gotoxy(10,18);print(green_color+"¡Producto eliminado exitosamente!")
            gotoxy(10, 19);input(green_color+"Presione una tecla para salir...")
        else:
            gotoxy(10, 18);print("Eliminación cancelada.")
            gotoxy(10, 19);input("Presione una tecla para salir...")
 #--------------  -------------------------------------------------------------- 
    def consult(self):
        borrarPantalla()
        print('\033c', end='')  # Limpiar la pantalla
        draw_custom_frame()
        gotoxy(3, 3)
        print("𝓒𝓸𝓷𝓼𝓾𝓵𝓽𝓪𝓻 𝓟𝓻𝓸𝓭𝓾𝓬𝓽𝓸")
        gotoxy(3,4);print("____________________________________________________________________________________")

        # Leer el JSON de los productos
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        while True:
            gotoxy(8, 6)
            print(cyan_color +"1. Consultar producto por ID")
            gotoxy(8, 7);print(cyan_color +"2. Mostrar toda la lista de productos")
            gotoxy(8, 8);option = input(blue_color+"Seleccione una opción (1/2): ")

            if option == "1":
                gotoxy(8, 12)
                while True:
                    gotoxy(10,12);product_id = input(cyan_color +"Ingrese el ID del producto que desea consultar: ")
                    if product_id.isdigit():
                        product_id = int(product_id)
                        break
                    else:
                        gotoxy(10, 13)
                        print(red_color+"Solo números")

                # Buscar el producto por su ID y mostrar sus detalles
                product_found = False
                for product in products:
                    if int(product["id"]) == product_id:
                        product_found = True
                        gotoxy(12, 14)
                        print(red_color + "Detalles del producto:")
                        gotoxy(12, 15)
                        print(blue_color + f"ID: {product['id']}")
                        gotoxy(12, 16)
                        print(blue_color +f"Descripción: {product['descripcion']}")
                        gotoxy(12, 17)
                        print(blue_color +f"Precio: {product['precio']}")
                        gotoxy(12, 18)
                        print(blue_color +f"Stock: {product['stock']}")
                        break

                if not product_found:
                    gotoxy(10, 18)
                    print("No se encontró ningún producto con el ID especificado.")

                gotoxy(8,20);input(cyan_color+"Presione una tecla para continuar...")
                break

            elif option == "2":
            
                current_y = 16  # Empieza en una línea debajo del encabezado
                gotoxy(8, 12)
                print(blue_color + "Lista de Productos:")
                gotoxy(8, 13)
                print(cyan_color + "┌──────────┬─────────────────────┬────────┬────────┐")
                gotoxy(8, 14)
                print(cyan_color + "│    ID    │      Descripción    │ Precio │ Stock  │")
                gotoxy(8, 15)
                print(cyan_color + "├──────────┼─────────────────────┼────────┼────────┤")
                total_stock = 0  # Inicializar la suma total de stock
                precios = []
                for product in products:
                    gotoxy(8, current_y)
                    print(cyan_color + f"│{product['id']:8}  │ {product['descripcion'][:18]:18}  │ {product['precio']:6} │ {product['stock']:6} │")
                    total_stock += int(product['stock'])  # Sumar el stock de este producto al total
                    precios.append(float(product['precio']))  # Agregar el precio a la lista de precios
                    current_y += 1  # Incrementa la posición vertical para el próximo producto
                gotoxy(8, current_y)
                print(cyan_color + "└──────────┴─────────────────────┴────────┴────────┘")
                current_y += 1  # Asegura que el mensaje de presionar una tecla esté en la siguiente línea
                gotoxy(8, current_y)
                print(f"Precio Máximo: {max(precios)}")  # Imprimir el precio máximo
                current_y += 1
                gotoxy(8, current_y)
                print(f"Precio Mínimo: {min(precios)}")  # Imprimir el precio mínimo
                current_y += 1
                gotoxy(8, current_y)
                print(f"Suma de Precios: {sum(precios)}")  # Imprimir la suma de los precios
                current_y += 1
                gotoxy(8, current_y)
                print(f"Total de Stock: {total_stock}")  # Imprimir el total de stock al final
                input(blue_color + "Presione una tecla para continuar...")
    #--------------  --------------------------------------------------------------   

class CrudSales(ICrud):
    def __init__(self):
        self.sales_list = []
    
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(2,1);print(green_color+"*"*90+reset_color)   #gotoxy es para mover el cursor a la posicion especifica en la pantalla
        gotoxy(40,2);print(blue_color+"𝓡𝓮𝓰𝓲𝓼𝓽𝓻𝓪𝓻 𝓿𝓮𝓷𝓽𝓪")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
#aqui termina registro venta
#--------------------------------------------------------- MODIFICAR --------------------------------------------------------

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        draw_custom_frame()
        gotoxy(36, 3)
        print("𝓐𝓬𝓽𝓾𝓪𝓵𝓲𝔃𝓪𝓻 𝓥𝓮𝓷𝓽𝓪")
        gotoxy(8, 4);print("____________________________________________________________________________________")
        
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices_data = json_file.read()
        
        while True:
            # Solicitar el número de factura a actualizar
            gotoxy(8, 6)
            numero_factura = input(green_color+"Ingrese el número de factura a actualizar: ")
            
            if not numero_factura.isdigit():
                gotoxy(8, 7)
                print(red_color + "Error: Ingrese solo números.")
                input(green_color + "Presione una tecla para continuar...")
                continue
            
            numero_factura = int(numero_factura)
            
            # Verificar si el número de factura existe en la lista de facturas
            factura_encontrada = None
            for factura in invoices_data:
                if factura["factura"] == numero_factura:
                    factura_encontrada = factura
                    break
                        
            # Mostrar mensaje de error si la factura no se encuentra
            if not factura_encontrada:
                gotoxy(8, 8)
                print(red_color + "Error: La factura con el número ingresado no fue encontrada.")
                time.sleep(2)
                gotoxy(8, 8)
                print(" " * 90)
                gotoxy(8,9);input(green_color + "Presione una tecla para continuar...")
                time.sleep(2)
                gotoxy(8, 9)
                print(" " * 90)
                continue
            
            # Mostrar los detalles de la factura antes de actualizar
            gotoxy(8, 9);print(cyan_color + "Detalles de la factura a actualizar:")
            gotoxy(10, 10);print(f"Factura#: {factura_encontrada['factura']}")
            gotoxy(10, 11);print(f"Fecha: {factura_encontrada['Fecha']}")
            gotoxy(10, 12);print(f"Cliente: {factura_encontrada['cliente']}")
            gotoxy(10, 13);print(f"Subtotal: {factura_encontrada['subtotal']}")
            gotoxy(10, 14);print(f"Descuento: {factura_encontrada['descuento']}")
            gotoxy(10, 15);print(f"IVA: {factura_encontrada['iva']}")
            gotoxy(10, 16);print(f"Total: {factura_encontrada['total']}")
            
            
            # Solicitar la información actualizada de la factura
            gotoxy(8, 18)
            print(blue_color + "Ingrese la información actualizada de la factura:")
            
            # Nueva fecha
            gotoxy(8, 19);nueva_fecha = validar.fecha(reset_color+"Nueva Fecha (deje vacío si no desea actualizar): ")
            if nueva_fecha is None:
                nueva_fecha = factura_encontrada['Fecha']

            # Nuevo subtotal
            gotoxy(8, 22);nuevo_subtotal = validar.solo_decimales(reset_color+"Nuevo Subtotal (deje vacío si no desea actualizar): ", red_color+"Solo decimales.")
            if nuevo_subtotal is None:
                nuevo_subtotal = factura_encontrada['subtotal']

            # Nuevo descuento
            gotoxy(8, 25);nuevo_descuento = validar.solo_decimales(reset_color+"Nuevo Descuento (deje vacío si no desea actualizar): ", red_color+"Solo decimales.")
            if nuevo_descuento is None:
                nuevo_descuento = factura_encontrada['descuento']

            # Nuevo IVA
            gotoxy(8, 28);nuevo_iva = validar.solo_decimales(reset_color+"Nuevo IVA (deje vacío si no desea actualizar): ", red_color+"Solo decimales.")
            if nuevo_iva is None:
                nuevo_iva = factura_encontrada['iva']

            # Nuevo total
            gotoxy(8, 31);nuevo_total = validar.solo_decimales(reset_color+"Nuevo Total (deje vacío si no desea actualizar): ", red_color+"Solo decimales.")
            if nuevo_total is None:
                nuevo_total = factura_encontrada['total']

            # Confirmación y actualización de la factura
            gotoxy(8, 33)
            confirmar = input(green_color+"¿Está seguro de que desea actualizar esta factura? (s/n): ")

            if confirmar.lower() == "s":
                # Actualizar los datos de la factura
                factura_encontrada['Fecha'] = nueva_fecha
                factura_encontrada['subtotal'] = float(nuevo_subtotal)
                factura_encontrada['descuento'] = float(nuevo_descuento)
                factura_encontrada['iva'] = float(nuevo_iva)
                factura_encontrada['total'] = float(nuevo_total)

                # Guardar los cambios en el archivo JSON
                json_file.save(invoices_data)
                # Mostrar mensaje de confirmación
                gotoxy(8, 34)
                print(green_color+"Factura actualizada correctamente.")
            else:
                gotoxy(8, 34)
                print(red_color+"Actualización cancelada.")
                print("")
            break  # Salir del bucle después de procesar la factura

# Luego puedes llamar al método update en la instancia de Sale

#----------------------------- BORRAR --------------------------------------------   
    def delete(self):
        validar = Valida()
        while True:
            borrarPantalla()
            print('\033c', end='')  # Limpiar la pantalla
            draw_custom_frame()
            gotoxy(40, 3)
            print("𝓔𝓵𝓲𝓶𝓲𝓷𝓪𝓻 𝓥𝓮𝓷𝓽𝓪")
            gotoxy(8, 4);print("____________________________________________________________________________________")

            # Solicitar al usuario que ingrese el número de factura a eliminar
            gotoxy(8, 6)
            while True:
                factura_numero = input(yellow_color + "Número de factura que desea eliminar (deje en blanco para volver al menú principal): ")
                # Leer el JSON de las facturas
                json_file = JsonFile(path+'/archivos/invoices.json')
                invoices = json_file.read()

                if not factura_numero:
                    return  # Regresar al menú principal si se deja en blanco
                if factura_numero.isdigit():
                    factura_numero = int(factura_numero)
                    break
                else:
                    gotoxy(8, 7)
                    print("Ingrese solo números")
                    time.sleep(1)
                    gotoxy(8, 7)
                    print(" " * 76)

            # Buscar la factura por su número
            factura_a_eliminar = None
            for factura in invoices:
                if factura["factura"] == factura_numero:
                    factura_a_eliminar = factura
                    break

            if factura_a_eliminar is not None:
                # Mostrar los detalles de la factura que se va a eliminar
                gotoxy(8, 8)
                print("Detalles de la factura a eliminar:")
                gotoxy(8, 10);print(green_color+f"Factura #: {factura_a_eliminar['factura']}")
                gotoxy(8, 11);print(green_color+f"Fecha: {factura_a_eliminar['Fecha']}")
                gotoxy(8, 12);print(green_color+f"Cliente: {factura_a_eliminar['cliente']}")
                gotoxy(8, 13);print(green_color+f"Subtotal: {factura_a_eliminar['subtotal']}")
                gotoxy(8, 14);print(green_color+f"Descuento: {factura_a_eliminar['descuento']}")
                gotoxy(8, 15);print(green_color+f"IVA: {factura_a_eliminar['iva']}")
                gotoxy(8, 16);print(green_color+f"Total: {factura_a_eliminar['total']}")

                # Confirmar la eliminación con el usuario
                gotoxy(8, 18)
                confirmacion = input(yellow_color+"¿Estás seguro de que quieres eliminar esta factura? (s/n): ").lower()
                if confirmacion == 's':
                    invoices.remove(factura_a_eliminar)
                    json_file.save(invoices)
                    gotoxy(8, 19)
                    print("¡Factura eliminada exitosamente!")
                else:
                    gotoxy(8, 19)
                    print(red_color+"Eliminación cancelada.")
            else:
                gotoxy(8, 16)
                print(red_color+"No se encontró ninguna factura con el número especificado.")
                time.sleep(2)  # Esperar 2 segundos
                gotoxy(8, 18)
                print(" " * 76)


    #----------------------------- CONSULTAR --------------------------------------------   
#maximo codigo de cliente y minimo de cliente
    def consult(self):
        draw_custom_frame()
        gotoxy(36,3)
        print(blue_color + '𝓒𝓸𝓷𝓼𝓾𝓵𝓽𝓪𝓻 𝓥𝓮𝓷𝓽𝓪')
        gotoxy(3,4);print("____________________________________________________________________________________")
        gotoxy(15,5);invoice= input(blue_color + "Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            
            if invoices:
                factura = invoices[0]
                detalles_factura = {k: v for k, v in factura.items() if k != 'detalle'}
                detalle_venta = factura["detalle"]
                gotoxy(9,7)
                print(f"Impresion de la Factura # {invoice}")
                print(tabulate([detalles_factura], headers="keys", tablefmt="heavy_grid", numalign="center"))
                # Mostrar el detalle de la venta
                gotoxy(9,14)
                print("Detalle de la Venta:")
                headers = detalle_venta[0].keys() if detalle_venta else []
                data = [[detalle[key] for key in headers] for detalle in detalle_venta]

                if data:
                    print(tabulate(data, headers=headers, tablefmt="heavy_grid", stralign="center", numalign="center"))

                else:
                    gotoxy(15, 8)
                    print(red_color + "No hay detalles de venta para esta factura." + reset_color)
            else:
                    gotoxy(15, 8)
                    print(red_color + "No se encontraron detalles para esta factura." + reset_color)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))
            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        gotoxy(43,23)
        x =input(blue_color + "presione una tecla para continuar...") 

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    draw_custom_frame()
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()  
            draw_custom_frame()
            customer = CrudClients()  
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                customer.create()
            elif opc1 == "2":
                customer.update()
            elif opc1 == "3":
                customer.delete()
            elif opc1 == "4":
                customer.consult()
            gotoxy(8,24);print("Regresando al menu Clientes...")
            time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla() 
            draw_custom_frame()
            product = CrudProducts()   
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                product.create()
            elif opc2 == "2":
                product.update()
            elif opc2 == "3":
                product.delete()
            elif opc2 == "4":
                product.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            draw_custom_frame()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()  
            elif opc3 == "4":
                sales.delete()    
     
    gotoxy(8,24);print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

