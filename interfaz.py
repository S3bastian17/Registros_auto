import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import re
from database import crear_tabla, insertar_datos, listar_autos, eliminar_auto

class RegistroAutosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Autos")
        self.root.geometry("500x400")
        
        # Tema y Estilo
        style = ttk.Style()
        style.theme_use('clam')
        self.root.option_add('*Font', 'Arial 12')
        
        # Crear la tabla en la base de datos
        crear_tabla()

        # Labels y entradas para registrar un auto
        tk.Label(root, text="Placa:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.placa_entry = tk.Entry(root)
        self.placa_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Color:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.color_entry = tk.Entry(root)
        self.color_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Modelo:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.modelo_entry = tk.Entry(root)
        self.modelo_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Empresa:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.empresa_entry = tk.Entry(root)
        self.empresa_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Nombre del Dueño:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.nombre_entry = tk.Entry(root)
        self.nombre_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(root, text="Apellido del Dueño:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.apellido_entry = tk.Entry(root)
        self.apellido_entry.grid(row=5, column=1, padx=10, pady=5)

        # Botón para registrar el auto
        tk.Button(root, text="Registrar Auto", command=self.registrar_auto).grid(row=6, column=0, columnspan=2, pady=10)

        # Botón para listar autos
        tk.Button(root, text="Listar Autos", command=self.abrir_planilla_autos).grid(row=7, column=0, columnspan=2, pady=10)
        
        # Botón de exportación a CSV
        tk.Button(root, text="Exportar a CSV", command=self.exportar_csv).grid(row=9, column=0, columnspan=2, pady=10)

        
    def validar_placa(self, placa):
        return re.match(r'^[0-9]{4} [A-Z]{3}$', placa)
        
    def registrar_auto(self):
        placa = self.placa_entry.get().upper()
        color = self.color_entry.get()
        modelo = self.modelo_entry.get()
        empresa = self.empresa_entry.get()
        nombre_dueño = self.nombre_entry.get()
        apellido_dueño = self.apellido_entry.get()
        
        #validacion 
        if not placa or not color or not modelo or not empresa or not nombre_dueño or not apellido_dueño:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return
        
        if not self.validar_placa(placa):
            messagebox.showerror("Error", "Formato de placa inválido. Use 4 numeros seguidas de 3 letras (ej: 1234 ABC).")
            return
        
        # Si todo está correcto, insertar los datos
        insertar_datos(placa, color, modelo, empresa, nombre_dueño, apellido_dueño)
        messagebox.showinfo("Éxito", "Auto registrado con éxito.")
        
        # Limpiar los campos después de registrar
        self.limpiar_campos()

        # Actualizar la tabla de autos en la ventana de lista (si está abierta)
        self.mostrar_autos()

    def limpiar_campos(self):
        # Limpiamos los campos de entrada
        self.placa_entry.delete(0, tk.END)
        self.color_entry.delete(0, tk.END)
        self.modelo_entry.delete(0, tk.END)
        self.empresa_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        
        #ventana de autos registrados    
    def abrir_planilla_autos(self):
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.title("Lista de Autos")
        nueva_ventana.geometry("900x500")

        # Campo de búsqueda de placas
        tk.Label(nueva_ventana, text="Buscar por Placa:").pack(pady=5)
        self.search_entry = tk.Entry(nueva_ventana)
        self.search_entry.pack(pady=5)
        self.search_entry.bind('<KeyRelease>', self.filtrar_autos)

        # Uso de Treeview para crear la tabla
        self.tree = ttk.Treeview(nueva_ventana, columns=("Placa", "Color", "Modelo", "Empresa", "Nombre", "Apellido"), show='headings')

        # Definir los encabezados
        self.tree.heading("Placa", text="Placa")
        self.tree.heading("Color", text="Color")
        self.tree.heading("Modelo", text="Modelo")
        self.tree.heading("Empresa", text="Empresa")
        self.tree.heading("Nombre", text="Nombre del Dueño")
        self.tree.heading("Apellido", text="Apellido del Dueño")

        # Ajustar el tamaño de las columnas
        self.tree.column("Placa", width=100)
        self.tree.column("Color", width=80)
        self.tree.column("Modelo", width=100)
        self.tree.column("Empresa", width=100)
        self.tree.column("Nombre", width=120)
        self.tree.column("Apellido", width=120)

        # Posicionar el Treeview
        self.tree.pack(expand=True, fill='both')

        # Botón para eliminar autos
        tk.Button(nueva_ventana, text="Eliminar Auto", command=self.eliminar_auto).pack(pady=10)

        # Mostrar todos los autos al abrir la ventana
        self.mostrar_autos()

    def mostrar_autos(self, filtro_placa=""):
        # Limpiar la tabla antes de mostrar los datos
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Recuperar todos los autos
        autos = listar_autos()

        # Filtrar autos si hay texto en el buscador
        if filtro_placa:
            autos = [auto for auto in autos if filtro_placa.upper() in auto[1].upper()]

        # Insertar autos filtrados en el Treeview
        for auto in autos:
            self.tree.insert('', tk.END, values=(auto[1], auto[2], auto[3], auto[4], auto[5], auto[6]))

    def filtrar_autos(self, event):
        # Obtener el valor del campo de búsqueda y actualizar la lista de autos
        filtro_placa = self.search_entry.get()
        self.mostrar_autos(filtro_placa)
        
    def eliminar_auto(self):
        # Obtener el auto seleccionado
        selected_item = self.tree.selection()
        if selected_item:
            valores = self.tree.item(selected_item)['values']
            placa = valores[0]

            # Confirmar eliminación
            confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de que desea eliminar el auto con placa {placa}?")
            if confirm:
                eliminar_auto(placa)
                self.mostrar_autos()
                messagebox.showinfo("Éxito", "Auto eliminado exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un auto para eliminar.")
            
    def exportar_csv(self):
        #Ubicacion de archivo
        archivo_csv = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        
        if archivo_csv:
            try:
                #Recuperar la lista de autos desde la base de datos
                autos = listar_autos()
                
                #Escribir los datos del archivo csv
                with open (archivo_csv, mode='w', newline='', encoding='utf-8') as archivos:
                    escritor_csv = csv.writer(archivos)
                    escritor_csv.writerow(["Placa", "Color", "Modelo", "Empresa", "Nombre", "Apellido"])
                    for auto in autos:
                        escritor_csv.writerow([auto[1], auto[2], auto[3], auto[4], auto[5], auto[6]])
                        
                messagebox.showinfo("Éxito", f"Datos exportados a {archivo_csv} exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistroAutosApp(root)
    root.mainloop()
