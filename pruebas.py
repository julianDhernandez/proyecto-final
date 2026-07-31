import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog


registros = []


costos = {
    "examen de sangre (12000)": 12000,
    "examen de orina (8000)": 8000,
    "citologias (9000)": 9000,
}

ventana = tk.Tk()
ventana.geometry("900x700")
ventana.title("Laboratorio Clinico BioSalud")
ventana.config(bg="#142849")


def pacientes():
    nombre = name.get()

    if not nombre.replace(" ", "").isalpha():
        messagebox.showerror("ERROR", "EL NOMBRE DEBE DE CONTENER LETRAS")
        return

    try:
        cedula = int(documen.get())
    except ValueError:
        messagebox.showerror("ERROR", "LA CEDULA DEBE DE CONTENER VALORES NUMERICOS")
        return

    examen = examenes.get()
    if examen not in costos:
        messagebox.showerror("ERROR", "SELECCIONE UN TIPO DE EXAMEN VALIDO")
        return

    costo = costos[examen]

    valor_atencion = atencion.get()
    if valor_atencion == 1:
        aten = "SI"
        es_prioritaria = True
    elif valor_atencion == 2:
        aten = "SI"
        es_prioritaria = True
    elif valor_atencion == 3:
        aten = "NO"
        es_prioritaria = False
    else:
        messagebox.showerror("ERROR", "SELECCIONE EL TIPO DE ATENCION")
        return

    paciente = {
        "nombre": nombre,
        "cedula": cedula,
        "examen": examen,
        "costo": costo,
        "atencion": aten,
        "es_prioritaria": es_prioritaria
    }
    registros.append(paciente)

    name.delete(0, END)
    documen.delete(0, END)
    examenes.set("")
    tabla.insert("", tk.END, values=(nombre, cedula, examen, aten, costo))


def facturacion_total_recursiva(lista_ordenes):
   
    if len(lista_ordenes) == 0:
        return 0.0
    primer_paciente = lista_ordenes[0]
    costo_actual = primer_paciente["costo"]
    resto_de_lista = lista_ordenes[1:]
    return costo_actual + facturacion_total_recursiva(resto_de_lista)


def contar_ordenes_prioritarias(lista_ordenes):
    
    if len(lista_ordenes) == 0:
        return 0
    primer_paciente = lista_ordenes[0]
    resto_de_lista = lista_ordenes[1:]
    if primer_paciente["es_prioritaria"] == True:
        conteo_actual = 1
    else:
        conteo_actual = 0
    return conteo_actual + contar_ordenes_prioritarias(resto_de_lista)


def buscar_examenes_paciente(lista_ordenes, cedula_paciente):
    
    if len(lista_ordenes) == 0:
        return 0
    primer_paciente = lista_ordenes[0]
    resto_de_lista = lista_ordenes[1:]
    if primer_paciente["cedula"] == cedula_paciente:
        coincidencia = 1
    else:
        coincidencia = 0
    return coincidencia + buscar_examenes_paciente(resto_de_lista, cedula_paciente)


def listar_tipos_examenes_paciente(lista_ordenes, cedula_paciente):
    
    if len(lista_ordenes) == 0:
        return []
    primer_paciente = lista_ordenes[0]
    resto_de_lista = lista_ordenes[1:]
    resultado_resto = listar_tipos_examenes_paciente(resto_de_lista, cedula_paciente)
    if primer_paciente["cedula"] == cedula_paciente:
        return [primer_paciente["examen"]] + resultado_resto
    else:
        return resultado_resto


def construir_texto_examenes(lista_examenes):
    
    if len(lista_examenes) == 0:
        return ""
    primer_examen = lista_examenes[0]
    resto = lista_examenes[1:]
    return primer_examen + construir_texto_examenes(resto)


def genere_cierre_ca(lista_ordenes):
    
    total_ordenes = len(lista_ordenes)
    total_facturado = facturacion_total_recursiva(lista_ordenes)
    total_prioritarias = contar_ordenes_prioritarias(lista_ordenes)
    return total_ordenes, total_facturado, total_prioritarias


def buscar_historial():
    cedula_texto = simpledialog.askstring(
        "Buscar historial", "Ingrese la cedula del paciente a buscar:"
    )
    if not cedula_texto:
        return
    try:
        cedula_buscada = int(cedula_texto)
    except ValueError:
        messagebox.showerror("ERROR", "LA CEDULA DEBE SER NUMERICA")
        return

    cantidad = buscar_examenes_paciente(registros, cedula_buscada)
    tipos_examen = listar_tipos_examenes_paciente(registros, cedula_buscada)

    if cantidad == 0:
        messagebox.showinfo(
            "Historial del paciente",
            "La cedula", cedula_buscada, "no tiene examenes registrados.",
        )
        return

    lista_como_texto = construir_texto_examenes(tipos_examen)
    messagebox.showinfo(
        "Historial del paciente",
        "La cedula ",cedula_buscada, "tiene" ,cantidad, "examen registrado:",
        lista_como_texto
    )


def generar_cierre():
    if len(registros) == 0:
        messagebox.showinfo("Cierre de caja", "No hay ordenes registradas todavia.")
        return

    total_ordenes, total_facturado, total_prioritarias = genere_cierre_ca(registros)

    confirmar = messagebox.askyesno(
        "Cierre de caja",
        "Total de ordenes:", total_ordenes,
        "Total facturado:",total_facturado,
        "Ordenes prioritarias:",total_prioritarias,
        "Deseas cerrar caja y borrar los registros para empezar de nuevo?",
    )

    if confirmar:
        registros.clear()
        tabla.delete(*tabla.get_children())
        messagebox.showinfo("Cierre de caja", "Registros borrados. Listo para un nuevo turno.")


registro = tk.LabelFrame(ventana, text="Ingreso de pacientes", padx=10, pady=10, bg="#142849", fg="WHITE")
registro.pack(fill="x", padx=15, pady=10)

tk.Label(registro, text="Nombre del paciente : ").grid(row=0, column=0, padx=20, pady=20, sticky="w")
name = tk.Entry(registro, width=40)
name.grid(row=0, column=1)

tk.Label(registro, text="Cedula o documento de la persona: ").grid(row=1, column=0, padx=20, pady=20, sticky="w")
documen = tk.Entry(registro, width=40)
documen.grid(row=1, column=1)

tipo = ["examen de sangre (12000)", "examen de orina (8000)", "citologias (9000)"]
tk.Label(registro, text="Tipo de examen medico : ").grid(row=2, column=0, padx=20, pady=20, sticky="w")
examenes = ttk.Combobox(registro, values=tipo, width=40)
examenes.grid(row=2, column=1)

atencion = tk.IntVar()
tk.Label(registro, text="Atencion prioritaria: ").grid(row=3, column=0, pady=20, padx=20, sticky="w")
tk.Radiobutton(registro, text="Tercera edad", variable=atencion, value=1).grid(row=3, column=1)
tk.Radiobutton(registro, text="Embarazada", variable=atencion, value=2).grid(row=3, column=2)
tk.Radiobutton(registro, text="Ingreso normal", variable=atencion, value=3).grid(row=3, column=4)

tk.Button(registro, text="Ingresar orden", command=pacientes, bg="#123940", fg="WHITE").grid(row=4, column=1)
tk.Button(registro, text="Buscar historial", command=buscar_historial, bg="#123940", fg="WHITE").grid(row=4, column=0)
tk.Button(registro, text="Generar cierre de caja", command=generar_cierre, bg="#123940", fg="WHITE").grid(row=4, column=3)

registro2 = tk.LabelFrame(ventana, text="Pacientes Ingresados", padx=10, pady=10, bg="#142849", fg="WHITE")
registro2.pack(fill="both", expand=True, padx=10, pady=10)

tabla = ttk.Treeview(registro2, columns=("Nombre", "Cedula", "tipo de examen", "prioridad", "Total"), show="headings")

tabla.heading("Nombre", text="Nombre")
tabla.heading("Cedula", text="Cedula")
tabla.heading("tipo de examen", text="tipo de examen")
tabla.heading("prioridad", text="prioridad")
tabla.heading("Total", text="Total Pagar")

tabla.column("Nombre", width=180)
tabla.column("Cedula", width=120)
tabla.column("tipo de examen", width=130)
tabla.column("prioridad", width=120)
tabla.column("Total", width=120)

tabla.pack(fill="both", expand=True)

ventana.mainloop()