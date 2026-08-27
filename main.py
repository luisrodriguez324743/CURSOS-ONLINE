

def main() -> None:
    datos = inicializar_crud()
    while True:
        print("\n===== CURSOS ONLINE =====")
        print("1. Iniciar sesión")
        print("2. Crear usuario")
        print("3. Salir")
        opcion = leer_opcion("Opción: ")

        if opcion == "1":
            usuario = iniciar_sesion(datos)
            if usuario is not None:
                menu_usuario(usuario, datos)
        elif opcion == "2":
            registrar_usuario(datos)
        elif opcion == "3":
            print("Hasta pronto.")
            return
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
