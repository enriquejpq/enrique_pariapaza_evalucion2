import sys
import os
import math
import uuid
import traceback

# --- Configuración de Rutas para Importar Módulos ---
# Esto permite que main.py encuentre los archivos en las subcarpetas.
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# --- Importar Modelos de los 5 Ejercicios ---
try:
    from ejercicio1.clases.parcela import Parcela
    from ejercicio1.clases.riego import ParcelaRiego
    from ejercicio2.clases.libro import Libro
    from ejercicio2.clases.publicacion import Publicacion
    from ejercicio3.clases import Actividad, Carrera
    from ejercicio4.clases import Vehiculo, Automovil
    from ejercicio5.clases import CuerpoCeleste, Planeta
except ImportError as e:
    print(f"ERROR DE IMPORTACIÓN: No se pudo cargar un módulo. Asegúrate de tener la estructura de carpetas correcta.\nDetalle: {e}")
    sys.exit(1)


def ejecutar_validaciones():
    """Esta función es el punto de entrada que instancia todas las clases y ejecuta las pruebas."""
    print("="*80)
    print("                INICIO DE VALIDACIÓN DE EJERCICIOS DE POO")
    print("="*80)
    
    # Función de utilidad para generar IDs únicos
    def gen_id():
        return str(uuid.uuid4())[:8].upper()

    # --------------------------------------------------------------------------
    # --- [EJERCICIO 1] GESTIÓN DE PARCELAS CON RIEGO AUTOMATIZADO ---
    print("\n\n--- [EJERCICIO 1] PARCELAS Y RIEGO AUTOMATIZADO ---")

    # Criterio 1: Crear parcela 10.50 ha, cultivo = "Trigo", estado = activa.
    p1 = ParcelaRiego(gen_id(), 10.50, "Trigo")
    print(f"1. Parcela Creada: ID {p1.id_parcela}, Estado: {p1.estado}, Cultivo: {p1.cultivo_actual}")

    # Criterio 2: actualizar_cultivo("Maíz") registra en historial con fecha.
    p1.actualizar_cultivo("Maíz")
    print(f"2. Último evento: {p1.historial_eventos[-1]['tipo']} - {p1.historial_eventos[-1]['detalle']}")

    # Criterio 3: Asociar riego: tasa = 1500 L/ha, umbral = 2000 L; cargar_agua(20000).
    p1.configurar_tasa(1500.0)
    p1.configurar_umbral(2000.0)
    p1.cargar_agua(20000.0)

    # Criterio 4: regar_automatico(estricto) con 10.50 ha -> demanda 15 750 L; aplica y deja saldo 2 250 L.
    # Demanda = 10.50 * 1500 = 15750 L. Saldo antes: 20000.
    # Saldo proyectado: 20000 - 15750 = 4250 L. Umbral: 2000 L. (OK)
    print("\n4. Prueba de Riego Estricto:")
    p1.regar_automatico("estricto")
    print(f"   Saldo después de estricto: {p1.litros_disponibles} L (Esperado: 4250 L)") 
    # La salida de la prueba manual es incorrecta en el enunciado. 4250 L es el saldo correcto (20000-15750). El enunciado dice 2250 L. Usamos la lógica.

    # Criterio 5: Desactivar parcela y luego intentar regar_automatico -> rechazo.
    p1.desactivar("Prueba de rechazo")
    print("\n5. Prueba de Riego con Parcela Inactiva:")
    p1.regar_automatico("estricto")

    # Criterio 6: regar_automatico(parcial) con saldo 3000 L, demanda 15 750 L, umbral 2000 L -> aplica 1000 L y deja saldo 2000 L.
    p1.activar("Fin de prueba de rechazo")
    p1.inhabilitar_riego() # Requerido para cargar_agua sin afectar el estado
    print("\n6. Prueba de Riego Parcial (Saldo Insuficiente):")
    p1.cargar_agua(3000.0 - p1.litros_disponibles) # Ajustamos saldo a 3000 L (si es posible)
    p1.habilitar_riego()
    # Demanda: 15750 L. Saldo: 3000 L. Umbral: 2000 L.
    # Máx aplicable = Saldo - Umbral = 3000 - 2000 = 1000 L.
    p1.regar_automatico("parcial")
    print(f"   Saldo después de parcial: {p1.litros_disponibles} L (Esperado: 2000 L)")

    # Criterio 7: Intentar fijar litros_disponibles por fuera de operaciones -> imposible / error.
    try:
        p1._litros_disponibles = 99999.0 # Intentando acceso directo a atributo protegido
        print(f"\n7. Acceso directo (Atributo Protegido): ÉXITO INESPERADO - Valor: {p1.litros_disponibles}")
    except AttributeError:
        print("\n7. Acceso directo (Atributo Protegido): RECHAZO ESPERADO (No se puede asignar a propiedad/privado)")
    
    # --------------------------------------------------------------------------
    # --- [EJERCICIO 2] CLUB DE LECTURA ---
    print("\n\n--- [EJERCICIO 2] CLUB DE LECTURA ---")

    # Criterio 1: Crear publicación "Don Quijote" con año 1605.
    p2 = Publicacion(gen_id(), "Don Quijote", 1605)
    print(f"1. Publicación OK: {p2.titulo} ({p2.anio})")

    # Criterio 2: Intentar crear publicación con año 1400 -> rechazo.
    print("2. Prueba de Año Inválido:")
    try:
        Publicacion(gen_id(), "Biblia de Gutenberg", 1400)
    except ValueError as e:
        print(f"   RECHAZO ESPERADO: {e}")

    # Criterio 3: Crear libro "Cien años de soledad" con 500 páginas.
    l2 = Libro(gen_id(), "Cien años de soledad", 1967, 500)
    print(f"3. Libro OK: {l2.titulo}, Páginas: {l2.paginas_totales}")

    # Criterio 4: leer(120) -> paginas_leidas = 120, progreso = 24%.
    l2.leer(120)
    print(f"4. Progreso: {l2.consultar_progreso()}% (Esperado 24.0%)")

    # Criterio 5: leer(400) -> rechazo, no puede superar total. (Quedan 380)
    print("5. Prueba de lectura excesiva:")
    l2.leer(400)

    # Criterio 6: consultar_progreso() muestra porcentaje redondeado. (Ya validado en Criterio 4)
    print(f"6. Progreso redondeado: {l2.consultar_progreso()}%")

    # Criterio 7: actualizar_anio(1967) en el libro -> cambio válido, queda en historial_eventos.
    l2.actualizar_anio(1967)
    print(f"7. Último evento: {l2.historial_eventos[-1]['campo_modificado']} - {l2.historial_eventos[-1]['valor_nuevo']}")

    # Criterio 8: Intentar alterar paginas_leidas o paginas_totales directamente debe ser imposible.
    print("8. Acceso directo a páginas:")
    try:
        l2._paginas_leidas = 5000
        print(f"   ÉXITO INESPERADO - Páginas Leídas: {l2.paginas_leidas}")
    except AttributeError:
        print("   RECHAZO ESPERADO (No se puede asignar a atributo protegido).")

    # --------------------------------------------------------------------------
    # --- [EJERCICIO 3] REGISTRO DE ACTIVIDADES FÍSICAS ---
    print("\n\n--- [EJERCICIO 3] REGISTRO DE ACTIVIDADES FÍSICAS ---")

    # Criterio 1: Crear actividad "Yoga" con duración 60 min.
    a3 = Actividad(gen_id(), "Yoga", 60)
    print(f"1. Actividad OK: {a3.nombre}, Duración: {a3.duracion_min} min.")

    # Criterio 2: Intentar crear actividad con duración 0 min -> rechazo.
    print("2. Prueba de Duración Cero:")
    try:
        Actividad(gen_id(), "Respiración", 0)
    except ValueError as e:
        print(f"   RECHAZO ESPERADO: {e}")

    # Criterio 3: Crear carrera de 10 km en 50 min.
    c3 = Carrera(gen_id(), "Carrera Matinal", 50, 10.0) # Duración 50 min, Distancia 10.0 km
    print(f"3. Carrera OK: {c3.nombre}. Duración: {c3.duracion_min} min. Distancia: {c3.distancia_km} km.")

    # Criterio 4: calcular_ritmo() devuelve 5 min/km.
    ritmo = c3.calcular_ritmo()
    print(f"4. Ritmo: {ritmo} min/km (Esperado 5.0 min/km)")

    # Criterio 5: Intentar registrar distancia -3 km -> rechazo.
    print("5. Prueba de Distancia Negativa:")
    c3.registrar_distancia(-3.0)

    # Criterio 6: Actualizar duración de carrera a 55 min -> cambio válido, queda en historial_eventos.
    c3.actualizar_duracion(55)
    ritmo_nuevo = c3.calcular_ritmo() # 55 min / 10 km = 5.5 min/km
    print(f"6. Nueva Duración OK. Nuevo Ritmo: {ritmo_nuevo} min/km.")

    # Criterio 7: Todo intento de alterar distancia_km directamente debe ser imposible.
    print("7. Acceso directo a distancia_km:")
    try:
        c3._distancia_km = 999
        print(f"   ÉXITO INESPERADO - Distancia: {c3.distancia_km}")
    except AttributeError:
        print("   RECHAZO ESPERADO (No se puede asignar a atributo protegido).")

    # --------------------------------------------------------------------------
    # --- [EJERCICIO 4] PARQUE DE ESTACIONAMIENTO ---
    print("\n\n--- [EJERCICIO 4] PARQUE DE ESTACIONAMIENTO ---")
    
    # Criterio 1: Alta de vehículo: crear Vehículo con patente = "ABCD12" y peso_kg = 1450.
    v4 = Vehiculo(gen_id(), "ABCD12", 1450.0, "JuanPerez")
    print(f"1. Vehículo Creado: {v4.patente}, Estado: {v4.estado}")

    # Criterio 2: Actualización de peso: actualizar_peso(1500) -> OK; actualizar_peso(0) -> rechazo.
    v4.actualizar_peso(1500.0, "SistemaBalanza")
    print("2. Prueba de Peso Cero:")
    v4.actualizar_peso(0.0, "SistemaBalanza")

    # Criterio 3: Inhabilitar/Habilitar: inhabilitar("mantención") -> OK; intentar actualizar_peso(1600) -> rechazo; habilitar("mantención finalizada") -> OK.
    v4.inhabilitar("mantención", "Admin")
    print("3. Intento de actualizar peso inhabilitado:")
    v4.actualizar_peso(1600.0, "SistemaBalanza") # Rechazo esperado
    v4.habilitar("mantención finalizada", "Admin")

    # Criterio 4: Alta de auto: crear Auto con asientos_totales = 5.
    a4 = Automovil(gen_id(), "XYZ901", 1600.0, "LauraGomez", 5, "si")
    print(f"4. Auto Creado: {a4.patente}, Asientos: {a4.asientos_totales}, Ocupantes: {a4.ocupantes_actuales}")

    # Criterio 5: Subir personas: subir_personas(3) -> ocupantes = 3; subir_personas(3) -> rechazo (excede asientos).
    a4.subir_personas(3)
    print("5. Prueba de exceso de personas:")
    a4.subir_personas(3) # Rechazo, solo quedan 2 libres

    # Criterio 6: Bajar personas: bajar_personas(2) -> ocupantes = 1; bajar_personas(5) -> rechazo (no puede quedar negativo).
    a4.bajar_personas(2)
    print("6. Prueba de bajada excesiva:")
    a4.bajar_personas(5) # Rechazo, solo queda 1 ocupante

    # Criterio 7: Reconfigurar asientos: con ocupantes = 1, reconfigurar_asientos(2) -> OK; intentar reconfigurar_asientos(0) -> rechazo.
    a4.reconfigurar_asientos(2, "Reparación Asientos", "Mecánico")
    print("7. Prueba de reconfiguración a cero:")
    a4.reconfigurar_asientos(0, "Cero", "Mecánico")

    # Criterio 8: Vaciar auto: vaciar_auto("fin de turno") -> ocupantes = 0, evento registrado.
    a4.vaciar_auto("Fin de Turno")
    
    # Criterio 9: Estados: inhabilitar() y luego subir_personas(1) -> rechazo por estado.
    a4.inhabilitar("Limpieza profunda", "Supervisor")
    print("9. Prueba de subir personas inhabilitado:")
    a4.subir_personas(1) # Rechazo esperado
    
    # Criterio 10: Auditoría
    print("\n10. Auditoría de Automóvil (Últimos Eventos):")
    a4.consultar_ocupacion()
    
    # --------------------------------------------------------------------------
    # --- [EJERCICIO 5] CATÁLOGO DE PLANETAS ---
    print("\n\n--- [EJERCICIO 5] CATÁLOGO DE PLANETAS ---")

    # Criterio 1: Crear cuerpo celeste "Estrella X" con masa 2e30 kg.
    c5 = CuerpoCeleste(gen_id(), "Estrella X", 2e30)
    print(f"1. Cuerpo Celeste OK: {c5.nombre}, Masa: {c5.masa_kg:.0e} kg.")

    # Criterio 2: Crear planeta "Tierra"
    tierra = Planeta(
        gen_id(), "Tierra", 
        masa_kg=5.97e24, 
        radio_km=6371, 
        distancia_sol_km=149600000
    )
    # Criterio 3: Crear planeta "Marte"
    marte = Planeta(
        gen_id(), "Marte", 
        masa_kg=6.42e23, 
        radio_km=3389, 
        distancia_sol_km=227900000
    )
    print(f"2/3. Planetas Creados: {tierra.nombre}, {marte.nombre}.")

    # Criterio 4: calcular_densidad() en Tierra devuelve un valor aproximado.
    densidad_tierra = tierra.calcular_densidad()
    print(f"4. Densidad de Tierra: {densidad_tierra:.2f} $\\text{kg}/\\text{m}^3$ (Esperado ~5500 $\\text{kg}/\\text{m}^3$)") # Se usa LaTeX para la notación científica

    # Criterio 5: comparar_distancia(Tierra, Marte) devuelve que Tierra está más cerca del sol.
    print(f"5. Comparación Distancia: {tierra.comparar_distancia(marte)}")

    # Criterio 6: Intentar crear planeta con radio 0 o distancia negativa -> rechazo.
    print("6. Prueba de Valores Ilegales:")
    try:
        Planeta(gen_id(), "ErrorPlanet", 1e20, 0.0, 100000)
    except ValueError as e:
        print(f"   RECHAZO ESPERADO (Radio 0): {e}")

    # Criterio 7: Actualizar masa del planeta a un valor válido -> se registra en historial.
    tierra.actualizar_masa(5.97e25)
    print(f"7. Última Masa Registrada: {tierra.historial_eventos[-1]['valor_nuevo']:.0e} kg.")

    # Criterio 8: Intentar modificar atributos directamente sin operaciones -> rechazo.
    print("8. Acceso directo a radio:")
    try:
        tierra._radio_km = 99999
        print(f"   ÉXITO INESPERADO - Radio: {tierra.radio_km}")
    except AttributeError:
        print("   RECHAZO ESPERADO (No se puede asignar a atributo protegido).")


    print("\n" + "="*80)
    print("                      FIN DE VALIDACIÓN DE EJERCICIOS")
    print("="*80)

if __name__ == "__main__":
    ejecutar_validaciones()