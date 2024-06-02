from utilities import borrarPantalla, gotoxy
import time
import datetime
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color


class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil) 
            valor = input()
            if valor =="":
                return None
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(2)
                gotoxy(col,fil);print(" "*50)
        return valor
    
    def solo_letras(self,mensaje,mensajeError): 
        while True:
            valor = str(input(" ----> | {} ".format(mensaje)))
            if valor == "":
                return None
            if valor.replace(" ","").isalpha(): # Revisa si solo contiene letras después de eliminar espacios en blanco
                break
            else:
                print(" ---->< | {} ".format(mensajeError))
        return valor
    
    def solo_decimales(self,mensaje,mensajeError):
        while True:
            valor = str(input(" ----> | {} ".format(mensaje)))
            if valor == "":
                return None
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                print("---->< | {} ".format(mensajeError))
        return valor
    
    def fecha(self, mensaje):
        while True:
            fecha_input = input(mensaje)
            if not fecha_input:
                # Si el usuario deja el campo vacío, retornamos None
                return None

            # Dividir la entrada en día, mes y año
            partes_fecha = fecha_input.split('/')
            if len(partes_fecha) != 3:
                print("Formato de fecha incorrecto. Debe ser dd/mm/yyyy.")
                time.sleep(2) 


            # Intentar convertir cada parte a entero
            try:
                dia = int(partes_fecha[0])
                mes = int(partes_fecha[1])
                año = int(partes_fecha[2])
            except ValueError:
                print("Formato de fecha incorrecto. Debe ser dd/mm/yyyy.")
                time.sleep(2) 
                continue

            # Verificar si la fecha es válida
            if dia < 1 or mes < 1 or mes > 12 or año < 1:
                print("Fecha inválida. Revise los valores ingresados.")
                time.sleep(2) 
                continue

            # Verificar si el día es válido para el mes
            dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            if mes == 2 and año % 4 == 0 and (año % 100 != 0 or año % 400 == 0):
                dias_por_mes[1] = 29  # Año bisiesto
            if dia > dias_por_mes[mes - 1]:
                print("Fecha inválida. El día no corresponde al mes.")
                time.sleep(2) 
                continue

            # Si llegamos aquí, la fecha es válida
            return fecha_input
    
    def cedula(self, mensaje):
        while True:
            cedula_input = input(mensaje)
            if not cedula_input:
                # Si el usuario deja el campo vacío, retornamos None
                return None

            # Verificar si la cédula tiene la longitud adecuada
            if len(cedula_input) != 10:
                gotoxy(8,9);print(red_color+"La cédula debe tener 10 dígitos.")
                time.sleep(2)
                gotoxy(8, 9); print(" " * 75)
                gotoxy(16, 8)
                continue

            # Verificar si todos los caracteres son dígitos
            if not cedula_input.isdigit():
                gotoxy(8,9);print(red_color+"La cédula debe contener solo dígitos.")
                time.sleep(2)
                gotoxy(8, 9); print(" " * 75)
                gotoxy(16, 8)
                continue

            # Verificar si la cédula comienza con "09"
            if not cedula_input.startswith("09"):
                gotoxy(8,9);print(red_color+"La cédula debe comenzar con '09'.")
                time.sleep(2)
                gotoxy(8, 9); print(" " * 75)
                gotoxy(16, 8)
                
                continue

            # Si llegamos aquí, la cédula es válida
            return cedula_input
        
    # Define el decorador para validar que tenga exactamente 10 dígitos
    def validate_10_digits(func):
        def wrapper(value):
            if isinstance(value, str) and value.isdigit() and len(value) == 10:
                return func(value)
            else:
                print("El valor debe ser una cadena de 10 dígitos.")
        return wrapper
    # Define el decorador para validar que sean solo dígitos
    def validate_digits_only(func):
        def wrapper(value):
            if isinstance(value, str) and value.isdigit():
                return func(value)
            else:
                print("El valor debe contener solo dígitos.")
        return wrapper
        
class otra:
    pass 

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)