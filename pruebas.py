import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


lista = []


COSTOS = {
    "examen de sangre (12000)": 12000,
    "examen de orina (8000)": 8000,
    "citologias (9000)": 9000
}

ventana = tk.Tk()
ventana.geometry("900x700")
ventana.title("Laboratorio Clinico BioSalud")
ventana.config(bg="#142849")



def pacientes():
    nombre = name.get().strip()

    if not nombre.replace(" ", "").isalpha():
        messagebox.showerror("ERROR", "EL NOMBRE DEBE CONTENER SOLO LETRAS")
        return
    
    try:
        cedula = int(documen.get())
    except ValueError:
        messagebox.showerror("ERROR", "LA CÉDULA DEBE CONTENER VALORES NUMÉRICOS")
        return
    
    examen = examenes.get()
    if examen not in COSTOS:
        messagebox.showerror("ERROR", "SELECCIONE UN EXAMEN VÁLIDO")
        return
        
    costo = COSTOS[examen]

    
    if atencion.get() in (1, 2):
        aten_texto = "SI"
        es_prioritaria = True
    elif atencion.get() == 3:
        aten_texto = "NO"
        es_prioritaria = False
    else:
        messagebox.showerror("ERROR", "SELECCIONE EL TIPO DE ATENCIÓN")
        return 

    
    orden = {
        "nombre": nombre,
        "cedula": cedula,
        "examen": examen,
        "costo": costo,
        "prioridad_texto": aten_texto,
        "es_prioritaria": es_prioritaria
    }
    
    lista.append(orden)

    
    name.delete(0, tk.END)
    documen.delete(0, tk.END)
    examenes.set("")
    atencion.set(0)
    tabla.insert("", tk.END, values=(nombre, cedula, examen, aten_texto, f"${costo:,}"))


def obtener_total(lista_ordenes):
    
    if len(lista_ordenes) == 0:
        return 0.0
    primer_paciente = lista_ordenes[0]
    costo_actual = primer_paciente["costo"]
    resto_de_lista = lista_ordenes[1:]
    return costo_actual + obtener_total(resto_de_lista)


def contar_prioridades(lista_ordenes):
    
    if len(lista_ordenes) == 0:
        return 0
    primer_paciente = lista_ordenes[0]
    conteo_actual = 1 if primer_paciente["es_prioritaria"] else 0
    resto_de_lista = lista_ordenes[1:]
    return conteo_actual + contar_prioridades(resto_de_lista)


def contar_exa(lista_ordenes, cedula_paciente):
    
    if len(lista_ordenes) == 0:
        return 0
    primer_paciente = lista_ordenes[0]
    coincidencia = 1 if primer_paciente["cedula"] == cedula_paciente else 0
    resto_de_lista = lista_ordenes[1:]
    return coincidencia + contar_exa(resto_de_lista, cedula_paciente)


def cierre_caja():
    if not lista:
        messagebox.showinfo("CIERRE DE CAJA", "No hay órdenes registradas aún.")
        return
        
    total_ordenes = len(lista)
    total_facturado = obtener_total(lista)
    total_prioritarias = contar_prioridades(lista)
    
    resumen = (
        f"--- RESUMEN CIERRE DE CAJA ---\n\n"
        f"Total órdenes registradas: {total_ordenes}\n"
        f"Órdenes prioritarias: {total_prioritarias}\n"
        f"Total recaudado: ${total_facturado:,.2f}"
    )
    messagebox.showinfo("Cierre de Caja", resumen)
    lista.clear()
    tabla.delete(*tabla.get_children())


def buscar_historial():
    try:
        cedula_buscar = int(documen.get())
    except ValueError:
        messagebox.showerror("ERROR", "Ingrese un número de cédula en el campo para buscar.")
        return

    cantidad = contar_exa(lista, cedula_buscar)
    messagebox.showinfo("HISTORIAL DE PACIENTE", f"El paciente con cédula {cedula_buscar} tiene {cantidad} examen(es) registrado(s).")



registro = tk.LabelFrame(ventana, text="Ingreso de pacientes", padx=10, pady=10, bg="#142849", fg="WHITE")
registro.pack(fill="x", padx=15, pady=10)

tk.Label(registro, text="Nombre del paciente: ", bg="#142849", fg="WHITE").grid(row=0, column=0, padx=20, pady=10, sticky="w")
name = tk.Entry(registro, width=40)
name.grid(row=0, column=1)

tk.Label(registro, text="Cédula o documento de la persona: ", bg="#142849", fg="WHITE").grid(row=1, column=0, padx=20, pady=10, sticky="w")
documen = tk.Entry(registro, width=40)
documen.grid(row=1, column=1)

tipo = list(COSTOS.keys())
tk.Label(registro, text="Tipo de examen médico: ", bg="#142849", fg="WHITE").grid(row=2, column=0, padx=20, pady=10, sticky="w")
examenes = ttk.Combobox(registro, values=tipo, width=37)
examenes.grid(row=2, column=1)

atencion = tk.IntVar()
tk.Label(registro, text="Atención prioritaria: ", bg="#142849", fg="WHITE").grid(row=3, column=0, pady=10, padx=20, sticky="w")

tk.Button(registro, text="Buscar historial", command=buscar_historial, bg="#123940", fg="WHITE", width=18).grid(row=4, column=0, pady=15)
tk.Button(registro, text="Ingresar orden", command=pacientes, bg="#123940", fg="WHITE", width=18).grid(row=4, column=1, pady=15)
tk.Button(registro, text="Generar cierre de caja", command=cierre_caja, bg="#123940", fg="WHITE", width=18).grid(row=4, column=2, pady=15)


registro2 = tk.LabelFrame(ventana, text="Pacientes Ingresados", padx=10, pady=10, bg="#142849", fg="WHITE")
registro2.pack(fill="both", expand=True, padx=15, pady=10)

tabla = ttk.Treeview(registro2, columns=("Nombre", "Cedula", "tipo de examen", "prioridad", "Total"), show="headings")

tabla.heading("Nombre", text="Nombre")
tabla.heading("Cedula", text="Cédula")
tabla.heading("tipo de examen", text="Tipo de Examen")
tabla.heading("prioridad", text="Prioridad")
tabla.heading("Total", text="Total Pagar")

tabla.column("Nombre", width=180)
tabla.column("Cedula", width=120)
tabla.column("tipo de examen", width=200)
tabla.column("prioridad", width=100)
tabla.column("Total", width=100)

tabla.pack(fill="both", expand=True)


tk.Radiobutton(registro, text="Tercera edad", variable=atencion, value=1, 
               bg="#142849", fg="WHITE", selectcolor="#123940", activebackground="#142849", activeforeground="WHITE").grid(row=3, column=1, sticky="w")

tk.Radiobutton(registro, text="Embarazada", variable=atencion, value=2, 
               bg="#142849", fg="WHITE", selectcolor="#123940", activebackground="#142849", activeforeground="WHITE").grid(row=3, column=2, sticky="w")

tk.Radiobutton(registro, text="Ingreso normal", variable=atencion, value=3, 
              bg="#142849", fg="WHITE", selectcolor="#123940", activebackground="#142849", activeforeground="WHITE").grid(row=3, column=3, sticky="w")




ventana.mainloop()