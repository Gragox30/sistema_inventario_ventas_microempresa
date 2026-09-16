# ============================================================
# Sistema de Gestión de Inventario y Registro de Ventas para una Microempresa
# ============================================================
import os
from datetime import datetime

# ============================================================
# ESTRUCTURA PRINCIPAL
# ============================================================
products = {}
id_product = 1
# Definición de rutas
CARPETA = 'sistema'
ARCHIVO_INVENTARIO = os.path.join(CARPETA, 'sis_inventario_ventas.txt')
ARCHIVO_VENTAS = os.path.join(CARPETA, 'registro_ventas.txt')
# ============================================================
# VERIFICAR ARCHIVOS
# ============================================================
def verificar_archivo():
    """Crea la carpeta y archivos necesarios."""
    if not os.path.exists(CARPETA):
        os.makedirs(CARPETA)
        print(f"Carpeta '{CARPETA}' creada correctamente.")
    if not os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, 'w', encoding='utf-8') as archive:
            pass
        print('Archivo de Inventario creado correctamente.')
    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, 'w', encoding='utf-8') as archive:
            pass
        print('Archivo de Ventas creado correctamente.')
# ============================================================
# GUARDAR PRODUCTOS
# ============================================================
def guardar_productos():
    """Guarda todos los productos en el archivo."""
    try:
        with open(ARCHIVO_INVENTARIO, 'w', encoding='utf-8') as archive:
            for p_id, datos in products.items():
                archive.write(
                    f"{p_id},"
                    f"{datos['nombre']},"
                    f"{datos['precio']},"
                    f"{datos['stock']},"
                    f"{datos['activo']}\n"
                )
    except IOError as e:
        print(f"Error al guardar los productos: {e}")
# ============================================================
# CARGAR PRODUCTOS
# ============================================================
def cargar_productos():
    """Carga los productos desde el archivo."""
    global id_product
    if not os.path.exists(ARCHIVO_INVENTARIO):
        return
    try:
        with open(ARCHIVO_INVENTARIO, 'r', encoding='utf-8') as archive:
            max_id = 0
            for line in archive:
                line = line.strip()
                if line:
                    partes = line.split(',')
                    # Formato nuevo:
                    # ID,nombre,precio,stock,activo
                    if len(partes) == 5:
                        p_id = int(partes[0])
                        nombre = partes[1]
                        precio = float(partes[2])
                        stock = int(partes[3])
                        activo = partes[4].lower() == 'true'
                    # Compatibilidad con el archivo anterior
                    # ID,nombre,precio,stock
                    elif len(partes) == 4:
                        p_id = int(partes[0])
                        nombre = partes[1]
                        precio = float(partes[2])
                        stock = int(partes[3])
                        # Los productos antiguos
                        # se consideran activos
                        activo = True
                    else:
                        continue
                    products[p_id] = {
                        'nombre': nombre,
                        'precio': precio,
                        'stock': stock,
                        'activo': activo
                    }
                    if p_id > max_id:
                        max_id = p_id
            id_product = max_id + 1
    except (
        ValueError,
        FileNotFoundError
    ) as e:
        print(f"Error al cargar productos: {e}")
# ============================================================
# REGISTRAR PRODUCTO
# ============================================================
def registrar_producto():
    """Registra un nuevo producto."""
    global id_product
    print('\n=== Registrar Producto ===')
    product_name = input('Ingresa el nombre del producto: ').strip()
    if product_name == '':
        print('El nombre no puede estar vacío.')
        return
    # Verificar nombre existente
    for datos in products.values():
        if datos['nombre'].lower() == product_name.lower():
            print('El nombre del producto ya está registrado.')
            return
    try:
        product_price = float(input('Ingresa el precio: '))
        product_stock = int(input('Ingresa el stock inicial: '))
        if product_price < 0 or product_stock < 0:
            print(
                'Error: El precio y el stock '
                'deben ser valores positivos.'
            )
            return
        products[id_product] = {
            'nombre': product_name,
            'precio': product_price,
            'stock': product_stock,
            'activo': True
        }
        guardar_productos()
        print(f'Producto registrado correctamente.')
        print(f'ID asignado: {id_product}')
        id_product += 1
    except ValueError:
        print('Error: Ingrese valores numéricos válidos.')
# ============================================================
# MOSTRAR PRODUCTOS
# ============================================================
def mostrar_productos():
    """Muestra todos los productos."""
    if not products:
        print('\nNo hay productos registrados.')
        return
    print('\n=== Lista de Productos ===')
    for p_id, datos in products.items():
        estado = (
            'ACTIVO'
            if datos['activo']
            else 'DESACTIVADO'
        )
        print(f"ID: {p_id}")
        print(f"Nombre: {datos['nombre']}")
        print(f"Precio: S/ {datos['precio']:.2f}")
        print(f"Stock: {datos['stock']}")
        print(f"Estado: {estado}")
        print('---------------------------')
# ============================================================
# BUSCAR PRODUCTO
# ============================================================
def buscar_producto():
    """Busca un producto mediante su ID."""
    try:
        p_id = int(input('\nIngresa el ID del producto: '))
        if p_id not in products:
            print('El ID ingresado no existe.')
            return
        datos = products[p_id]
        estado = (
            'ACTIVO'
            if datos['activo']
            else 'DESACTIVADO'
        )
        print('\n=== Producto Encontrado ===')
        print(f"ID: {p_id}")
        print(f"Nombre: {datos['nombre']}")
        print(f"Precio: S/ {datos['precio']:.2f}")
        print(f"Stock: {datos['stock']}")
        print(f"Estado: {estado}")
    except ValueError:
        print('Error: Ingrese un ID entero.')
# ============================================================
# ACTUALIZAR STOCK
# ============================================================
def actualizar_stock():
    """Añade unidades al stock."""
    print('\n=== Actualizar Stock ===')
    try:
        p_id = int(input('Ingrese el ID del producto: '))
        if p_id not in products:
            print('El producto no existe.')
            return
        datos = products[p_id]
        if not datos['activo']:
            print('El producto está desactivado.')
            print('Debe reactivarlo antes de modificar ', 'su stock.')
            return
        add_stock = int(input('Ingrese la cantidad a agregar: '))
        if add_stock <= 0:
            print('La cantidad debe ser mayor a 0.')
            return
        products[p_id]['stock'] += add_stock
        guardar_productos()
        print('Stock actualizado correctamente.')
        print(
            f"Nuevo stock: "
            f"{products[p_id]['stock']}"
        )
    except ValueError:
        print('Error: Ingrese un número entero válido.')
# ============================================================
# EDITAR PRODUCTO
# ============================================================
def editar_producto():
    """
    Modifica nombre y precio.
    El ID y el stock se mantienen.
    """
    print('\n=== Editar Producto ===')
    try:
        p_id = int(input('Ingrese el ID del producto: '))
        if p_id not in products:
            print('El producto no existe.')
            return
        datos = products[p_id]
        print('\n=== Datos actuales ===')
        print(f"ID: {p_id}")
        print(f"Nombre: {datos['nombre']}")
        print(f"Precio: S/ {datos['precio']:.2f}")
        print(f"Stock: {datos['stock']}")
        nuevo_nombre = input('\nNuevo nombre: ').strip()
        if nuevo_nombre == '':
            print('El nombre no puede estar vacío.')
            return
        # Verificar que el nombre no pertenezca
        # a otro producto
        for otro_id, otro_datos in products.items():
            if otro_id != p_id:
                if (otro_datos['nombre'].lower() == nuevo_nombre.lower()):
                    print('Ese nombre ya pertenece ', 'a otro producto.')
                    return
        nuevo_precio = float(input('Nuevo precio: '))
        if nuevo_precio < 0:
            print('El precio no puede ser negativo.')
            return
        # Mantiene ID y stock
        products[p_id]['nombre'] = nuevo_nombre
        products[p_id]['precio'] = nuevo_precio
        guardar_productos()
        print('\nProducto actualizado correctamente.')
        print(f'ID conservado: {p_id}')
    except ValueError:
        print('Error: Ingrese un precio válido.')
# ============================================================
# DESACTIVAR/REACTIVAR PRODUCTO
# ============================================================
def eliminar_producto():
    """
    Desactiva o reactiva un producto.
    NO elimina físicamente el producto.
    El ID se conserva.
    """
    print('\n=== Desactivar / Reactivar Producto ===')
    try:
        p_id = int(input('Ingrese el ID del producto: '))
        if p_id not in products:
            print('El producto no existe.')
            return
        datos = products[p_id]
        print('\n=== Producto ===')
        print(f"ID: {p_id}")
        print(f"Nombre: {datos['nombre']}")
        print(f"Precio: S/ {datos['precio']:.2f}")
        print(f"Stock: {datos['stock']}")
        if datos['activo']:
            print('\nEstado actual: ACTIVO')
            confirmar = input('¿Desea DESACTIVAR este producto? (S/N): ').strip().lower()
            if confirmar == 's':
                products[p_id]['activo'] = False
                guardar_productos()
                print('\nProducto desactivado correctamente.')
                print(f'El ID {p_id} se ha conservado.')
                print('El historial de ventas también ', 'se mantiene.')
            else:
                print('Operación cancelada.')
        else:
            print('\nEstado actual: DESACTIVADO')
            confirmar = input('¿Desea REACTIVAR este producto? (S/N): ').strip().lower()
            if confirmar == 's':
                products[p_id]['activo'] = True
                guardar_productos()
                print('\nProducto reactivado correctamente.')
                print(f'El ID {p_id} sigue siendo: {p_id}')
            else:
                print('Operación cancelada.')
    except ValueError:
        print('Error: Ingrese un ID entero.')
# ============================================================
# REGISTRAR VENTA
# ============================================================
def ventas():
    '''
    Registra una venta con descuento,
    pago y cálculo de vuelto.
    '''
    print('\n=== Registrar Venta ===')
    try:
        p_id = int(input('Ingrese el ID del producto: '))
        if p_id not in products:
            print('El ID del producto no existe.')
            return
        datos = products[p_id]
        # No permitir ventas de productos desactivados
        if not datos['activo']:
            print('Este producto está DESACTIVADO.')
            print('No se puede realizar una venta con este producto.')
            return
        print('\n=== Producto ===')
        print(f"ID: {p_id}")
        print(f"Nombre: {datos['nombre']}")
        print(
            f"Precio unitario: "
            f"S/ {datos['precio']:.2f}"
        )
        print(
            f"Stock disponible: "
            f"{datos['stock']}"
        )
        cantidad = int(input('\nIngrese la cantidad a vender: '))
        if cantidad <= 0:
            print('La cantidad debe ser mayor a cero.')
            return
        if cantidad > datos['stock']:
            print(
                f"Stock insuficiente. "
                f"Solo quedan {datos['stock']}."
            )
            return
        # Subtotal
        subtotal = (cantidad * datos['precio'])
        print(f'\nSubtotal: S/ {subtotal:.2f}')
        # Descuento
        tiene_descuento = input('¿Tiene descuento? (S/N): ').strip().lower()
        descuento_porcentaje = 0
        if tiene_descuento == 's':
            descuento_porcentaje = float(
                input('Ingrese porcentaje de descuento: '))
            if (descuento_porcentaje < 0 or descuento_porcentaje > 100):
                print('El descuento debe estar entre 0 y 100%.')
                return
        # Calcular descuento
        monto_descuento = (subtotal * descuento_porcentaje / 100)
        total = (subtotal - monto_descuento)
        print(
            f'Descuento: '
            f'{descuento_porcentaje:.2f}%'
        )
        print(
            f'Monto descuento: '
            f'S/ {monto_descuento:.2f}'
        )
        print(
            f'TOTAL A PAGAR: '
            f'S/ {total:.2f}'
        )
        # Pago
        pago = float(input('\nIngrese el monto pagado: '))
        if pago < total:
            print(f'Pago insuficiente.')
            print(
                f'Faltan: '
                f'S/ {total - pago:.2f}'
            )
            return
        # Vuelto
        vuelto = pago - total
        # Actualizar stock
        products[p_id]['stock'] -= cantidad
        guardar_productos()
        # Fecha y hora
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Registrar venta
        with open(ARCHIVO_VENTAS, 'a', encoding='utf-8') as archivo_ventas:
            archivo_ventas.write(
                f"{fecha_actual},"
                f"{p_id},"
                f"{datos['nombre']},"
                f"{cantidad},"
                f"{datos['precio']:.2f},"
                f"{descuento_porcentaje:.2f},"
                f"{monto_descuento:.2f},"
                f"{total:.2f},"
                f"{pago:.2f},"
                f"{vuelto:.2f}\n"
            )
        # Comprobante
        print('\n')
        print('=' * 40)
        print('        VENTA REALIZADA')
        print('=' * 40)
        print(f'Producto: {datos["nombre"]}')
        print(f'Cantidad: {cantidad}')
        print(
            f'Precio unitario: '
            f'S/ {datos["precio"]:.2f}'
        )
        print(
            f'Subtotal: '
            f'S/ {subtotal:.2f}'
        )
        print(
            f'Descuento: '
            f'{descuento_porcentaje:.2f}%'
        )
        print(
            f'Total: '
            f'S/ {total:.2f}'
        )
        print(
            f'Pago recibido: '
            f'S/ {pago:.2f}'
        )
        print(
            f'Vuelto: '
            f'S/ {vuelto:.2f}'
        )
        print(
            f'Stock restante: '
            f'{products[p_id]["stock"]}'
        )
        print('=' * 40)
    except ValueError:
        print('Error: Ingrese valores numéricos válidos.')
# ============================================================
# REPORTE DE VENTAS
# ============================================================
def reporte_ventas():
    """
    Muestra todas las ventas realizadas,
    organizadas por día.
    """
    print('\n=== REPORTE DE VENTAS ===')
    if not os.path.exists(ARCHIVO_VENTAS):
        print('No existe el archivo de ventas.')
        return
    try:
        with open(ARCHIVO_VENTAS, 'r', encoding='utf-8') as archivo:
            ventas_registradas = []
            for line in archivo:
                line = line.strip()
                if not line:
                    continue
                partes = line.split(',')
                # El nuevo formato contiene 10 datos
                if len(partes) != 10:
                    continue
                (
                    fecha_hora,
                    p_id,
                    nombre,
                    cantidad,
                    precio,
                    descuento,
                    monto_descuento,
                    total,
                    pago,
                    vuelto
                ) = partes
                ventas_registradas.append({
                    'fecha_hora': fecha_hora,
                    'fecha': fecha_hora.split(' ')[0],
                    'hora': fecha_hora.split(' ')[1],
                    'id': p_id,
                    'nombre': nombre,
                    'cantidad': int(cantidad),
                    'precio': float(precio),
                    'descuento': float(descuento),
                    'monto_descuento':
                        float(monto_descuento),
                    'total': float(total),
                    'pago': float(pago),
                    'vuelto': float(vuelto)
                })
        if not ventas_registradas:
            print('\nNo existen ventas registradas.')
            return
        # Obtener días únicos
        dias = []
        for venta in ventas_registradas:
            if venta['fecha'] not in dias:
                dias.append(
                    venta['fecha']
                )
        # Ordenar días
        dias.sort()
        # Mostrar ventas por día
        for dia in dias:
            print('\n')
            print('=' * 60)
            print(f'FECHA: {dia}')
            print('=' * 60)
            ventas_del_dia = []
            for venta in ventas_registradas:
                if venta['fecha'] == dia:
                    ventas_del_dia.append(
                        venta
                    )
            total_dia = 0
            unidades_dia = 0
            for venta in ventas_del_dia:
                print(f'\nHora: {venta["hora"]}')
                print(f'ID Producto: {venta["id"]}')
                print(f'Producto: {venta["nombre"]}')
                print(f'Cantidad: {venta["cantidad"]}')
                print(
                    f'Precio unitario: '
                    f'S/ {venta["precio"]:.2f}'
                )
                print(
                    f'Descuento: '
                    f'{venta["descuento"]:.2f}%'
                )

                print(
                    f'Monto descuento: '
                    f'S/ {venta["monto_descuento"]:.2f}'
                )
                print(
                    f'Total venta: '
                    f'S/ {venta["total"]:.2f}'
                )
                print(
                    f'Pago recibido: '
                    f'S/ {venta["pago"]:.2f}'
                )
                print(
                    f'Vuelto: '
                    f'S/ {venta["vuelto"]:.2f}'
                )
                print('-' * 60)
                total_dia += venta['total']
                unidades_dia += venta['cantidad']
            # Resumen del día
            print(f'\nRESUMEN DEL {dia}')
            print(
                f'Total de ventas: '
                f'{len(ventas_del_dia)}'
            )
            print(
                f'Unidades vendidas: '
                f'{unidades_dia}'
            )
            print(
                f'INGRESOS DEL DÍA: '
                f'S/ {total_dia:.2f}'
            )
            print('=' * 60)
    except (
        ValueError,
        FileNotFoundError
    ) as e:
        print(f'Error al generar reporte: {e}')
# ============================================================
# MENU PRINCIPAL
# ============================================================
def main():

    verificar_archivo()
    cargar_productos()

    while True:
        print('\n' + '=' * 55)
        print('=== SISTEMA DE GESTIÓN DE INVENTARIO Y VENTAS ===')
        print('=' * 55)
        print('1. Registrar Producto')
        print('2. Mostrar Productos')
        print('3. Buscar Producto')
        print('4. Actualizar Stock')
        print('5. Editar Producto')
        print('6. Desactivar / Reactivar Producto')
        print('7. Registrar Venta')
        print('8. Reporte de Ventas')
        print('9. Salir')
        opcion = input('\nSelecciona una opción (1-9): ').strip()
        if opcion == '1':
            registrar_producto()
        elif opcion == '2':
            mostrar_productos()
        elif opcion == '3':
            buscar_producto()
        elif opcion == '4':
            actualizar_stock()
        elif opcion == '5':
            editar_producto()
        elif opcion == '6':
            eliminar_producto()
        elif opcion == '7':
            ventas()
        elif opcion == '8':
            reporte_ventas()
        elif opcion == '9':
            print('Saliendo del sistema... ¡Hasta luego!')
            break
        else:
            print('Opción no válida.')
        input('\nPresione ENTER para continuar...')
# ============================================================
# EJECUTAR PROGRAMA
# ============================================================
if __name__ == '__main__':
    main()
