from iCrud import ICrud
import json

# Clase concreta para manejar clientes
class CustomerManager(ICrud):
    def __init__(self, filename):
        self.filename = filename

    def create(self):
        # Código para crear un nuevo cliente
        pass

    def update(self):
        # Código para actualizar un cliente existente
        pass

    def delete(self):
        # Código para eliminar un cliente existente
        pass

    def consult(self):
        # Código para consultar clientes
        pass

    def consult_general(self):
        # Código para la consulta general de clientes
        with open(self.filename) as f:
            clients_data = json.load(f)
        
        self.print_clients(clients_data)

    def consult_vip(self):
        # Código para la consulta de clientes VIP
        with open(self.filename) as f:
            clients_data = json.load(f)
        
        vip_clients = [client for client in clients_data if client.get('valor') == 'VIP']
        self.print_clients(vip_clients)

    def consult_regular(self):
        # Código para la consulta de clientes regulares
        with open(self.filename) as f:
            clients_data = json.load(f)
        
        regular_clients = [client for client in clients_data if client.get('valor') == 'Regular']
        self.print_clients(regular_clients)

    def consult_todos(self):
        # Código para la consulta de todos los clientes
        with open(self.filename) as f:
            clients_data = json.load(f)
        
        self.print_clients(clients_data)

    def print_client(self, client):
        # Función para imprimir los detalles de un solo cliente
        print(f"DNI: {client['dni']}")
        print(f"Nombre: {client['nombre']} {client['apellido']}")
        if 'valor' in client:
            print(f"Valor: {client['valor']}")
        print()

    def print_clients(self, clients):
        # Función para imprimir los detalles de varios clientes
        for client in clients:
            self.print_client(client)

# Ejemplo de uso
if __name__ == "__main__":
    customer_manager = CustomerManager('clients.json')
    customer_manager.consult_general()