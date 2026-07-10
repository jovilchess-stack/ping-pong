"""
Evaluación Final Transversal - FPY1101
Sistema de administración de planes de membresía - Gimnasio FitPass
"""


# ============================================================
# FUNCIONES DE VALIDACIÓN INDIVIDUAL (Opción 4 - Agregar plan)
# ============================================================

def validar_codigo(codigo, planes, inscripciones):
    if codigo.strip() == "":
        return False
    if codigo.upper() in planes or codigo.upper() in inscripciones:
        return False
    return True


def validar_nombre(nombre):
    return nombre.strip() != ""


def validar_tipo(tipo):
    return tipo.lower() in ("mensual", "trimestral", "anual")


def validar_duracion(duracion):
    try:
        return int(duracion) > 0
    except ValueError:
        return False


def validar_acceso_piscina(valor):
    return valor.lower() in ("s", "n")


def validar_incluye_clases(valor):
    return valor.lower() in ("s", "n")


def validar_horario(horario):
    return horario.strip() != ""


def validar_precio(precio):
    try:
        return int(precio) > 0
    except ValueError:
        return False


def validar_cupos(cupos):
    try:
        return int(cupos) >= 0
    except ValueError:
        return False


# ============================================================
# LECTURA DE OPCIÓN DE MENÚ
# ============================================================

def leer_opcion():
    while True:
        try:
            opcion = int(input("Ingrese opción: "))
            if 1 <= opcion <= 6:
                return opcion
            else:
                print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


# ============================================================
# OPCIÓN 1 - CUPOS POR TIPO DE PLAN
# ============================================================

def cupos_tipo(tipo, planes, inscripciones):
    total = 0
    for codigo, datos in planes.items():
        if datos[1].lower() == tipo.lower():
            total += inscripciones[codigo][1]
    print(f"El total de cupos disponibles es: {total}")


# ============================================================
# OPCIÓN 2 - BÚSQUEDA DE PLANES POR RANGO DE PRECIO
# ============================================================

def busqueda_precio(p_min, p_max, planes, inscripciones):
    resultados = []
    for codigo, datos in inscripciones.items():
        precio = datos[0]
        cupos = datos[1]
        if p_min <= precio <= p_max and cupos != 0:
            nombre_plan = planes[codigo][0]
            resultados.append(f"{nombre_plan}-{codigo}")

    if resultados:
        resultados.sort()
        print(f"Los planes encontrados son: {resultados}")
    else:
        print("No hay planes en ese rango de precios.")


# ============================================================
# OPCIÓN 3 - ACTUALIZAR PRECIO DE PLAN
# ============================================================

def buscar_codigo(codigo, planes):
    return codigo.upper() in planes


def actualizar_precio(codigo, nuevo_precio, planes, inscripciones):
    codigo = codigo.upper()
    if buscar_codigo(codigo, planes):
        inscripciones[codigo][0] = nuevo_precio
        return True
    return False


# ============================================================
# OPCIÓN 4 - AGREGAR PLAN
# ============================================================

def agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina,
                  incluye_clases, horario, precio, cupos,
                  planes, inscripciones):
    codigo = codigo.upper()
    if codigo in planes or codigo in inscripciones:
        return False

    planes[codigo] = [nombre, tipo.lower(), duracion, acceso_piscina,
                       incluye_clases, horario]
    inscripciones[codigo] = [precio, cupos]
    return True


# ============================================================
# OPCIÓN 5 - ELIMINAR PLAN
# ============================================================

def eliminar_plan(codigo, planes, inscripciones):
    codigo = codigo.upper()
    if buscar_codigo(codigo, planes):
        del planes[codigo]
        del inscripciones[codigo]
        return True
    return False


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def mostrar_menu():
    print("\n========== MENÚ PRINCIPAL ==========")
    print("1. Cupos por tipo de plan")
    print("2. Búsqueda de planes por rango de precio")
    print("3. Actualizar precio de plan")
    print("4. Agregar plan")
    print("5. Eliminar plan")
    print("6. Salir")
    print("=====================================")


def main():
    planes = {
        'F001': ['Plan Básico', 'mensual', 1, False, False, 'libre'],
        'F002': ['Plan Full', 'mensual', 1, True, True, 'libre'],
        'F003': ['Plan Estudiante', 'trimestral', 3, False, True, 'tarde'],
        'F004': ['Plan Senior', 'trimestral', 3, True, False, 'mañana'],
        'F005': ['Plan Anual Pro', 'anual', 12, True, True, 'libre'],
        'F006': ['Plan Nocturno', 'mensual', 1, False, True, 'noche'],
    }

    inscripciones = {
        'F001': [14990, 30],
        'F002': [22990, 10],
        'F003': [39990, 0],
        'F004': [35990, 6],
        'F005': [159990, 2],
        'F006': [18990, 15],
    }

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion == 1:
            tipo = input("Ingrese tipo de plan a consultar: ")
            cupos_tipo(tipo, planes, inscripciones)

        elif opcion == 2:
            while True:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    if p_min >= 0 and p_max >= 0 and p_min <= p_max:
                        break
                    else:
                        print("Debe ingresar valores enteros")
                except ValueError:
                    print("Debe ingresar valores enteros")
            busqueda_precio(p_min, p_max, planes, inscripciones)

        elif opcion == 3:
            repetir = "s"
            while repetir == "s":
                codigo = input("Ingrese código del plan: ")
                try:
                    nuevo_precio = int(input("Ingrese nuevo precio: "))
                    if actualizar_precio(codigo, nuevo_precio, planes, inscripciones):
                        print("Precio actualizado")
                    else:
                        print("El código no existe")
                except ValueError:
                    print("Debe ingresar un valor entero")
                repetir = input("¿Desea actualizar otro precio (s/n)?: ").lower()

        elif opcion == 4:
            codigo = input("Ingrese código del plan: ")
            nombre = input("Ingrese nombre del plan: ")
            tipo = input("Ingrese tipo (mensual/trimestral/anual): ")
            duracion = input("Ingrese duración (meses): ")
            acceso_piscina = input("¿Incluye acceso a piscina? (s/n): ")
            incluye_clases = input("¿Incluye clases grupales? (s/n): ")
            horario = input("Ingrese horario: ")
            precio = input("Ingrese precio: ")
            cupos = input("Ingrese cupos: ")

            if not validar_codigo(codigo, planes, inscripciones):
                print("Código inválido o ya existente")
            elif not validar_nombre(nombre):
                print("Nombre inválido")
            elif not validar_tipo(tipo):
                print("Tipo inválido")
            elif not validar_duracion(duracion):
                print("Duración inválida")
            elif not validar_acceso_piscina(acceso_piscina):
                print("Valor de acceso a piscina inválido")
            elif not validar_incluye_clases(incluye_clases):
                print("Valor de clases grupales inválido")
            elif not validar_horario(horario):
                print("Horario inválido")
            elif not validar_precio(precio):
                print("Precio inválido")
            elif not validar_cupos(cupos):
                print("Cupos inválidos")
            else:
                acceso_piscina_bool = acceso_piscina.lower() == "s"
                incluye_clases_bool = incluye_clases.lower() == "s"
                if agregar_plan(codigo, nombre, tipo, int(duracion),
                                 acceso_piscina_bool, incluye_clases_bool,
                                 horario, int(precio), int(cupos),
                                 planes, inscripciones):
                    print("Plan agregado")
                else:
                    print("El código ya existe")

        elif opcion == 5:
            codigo = input("Ingrese código del plan a eliminar: ")
            if eliminar_plan(codigo, planes, inscripciones):
                print("Plan eliminado")
            else:
                print("El código no existe")

        elif opcion == 6:
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()