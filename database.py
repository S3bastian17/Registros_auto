import sqlite3

def conectar():
    conn = sqlite3.connect('registros_autos.db')
    return conn

def crear_tabla():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL,
            color TEXT NOT NULL,
            modelo TEXT NOT NULL,
            empresa TEXT NOT NULL,
            nombre_dueño TEXT NOT NULL,
            apellido_dueño TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def insertar_datos(placa, color, modelo, empresa, nombre_dueño, apellido_dueño):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO autos (placa, color, modelo, empresa, nombre_dueño, apellido_dueño)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (placa, color, modelo, empresa, nombre_dueño, apellido_dueño))
    conn.commit()
    conn.close()

def buscar_auto(placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM autos WHERE placa = ?', (placa,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def listar_autos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM autos')
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def eliminar_auto(placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM autos WHERE placa = ?', (placa,))
    conn.commit()
    conn.close()

def menu():
    while True:
        print("Sistema de Registro de Autos")
        print("1. Registrar auto")
        print("2. Buscar auto por placa")
        print("3. Listar todos los autos")
        print("4. Eliminar auto por placa")
        print("5. Salir")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            placa = input("Placa: ")
            color = input("Color: ")
            modelo = input("Modelo: ")
            empresa = input("Empresa: ")
            nombre_dueño = input("Nombre del dueño: ")
            apellido_dueño = input("Apellido del dueño: ")
            insertar_datos(placa, color, modelo, empresa, nombre_dueño, apellido_dueño)
            print("Auto registrado con éxito.\n")
        elif opcion == '2':
            placa = input("Ingresa la placa del auto: ")
            auto = buscar_auto(placa)
            if auto:
                print(f"Auto encontrado: {auto}\n")
            else:
                print("Auto no encontrado.\n")
        elif opcion == '3':
            autos = listar_autos()
            for auto in autos:
                print(auto)
            print()
        elif opcion == '4':
            placa = input("Ingresa la placa del auto a eliminar: ")
            eliminar_auto(placa)
            print(f"Auto con placa {placa} eliminado.\n")
        elif opcion == '5':
            print("Saliendo...")
            break
        else:
            print("Opción no válida.\n")

if __name__ == "__main__":
    crear_tabla()
    menu()
