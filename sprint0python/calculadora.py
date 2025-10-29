from operaciones import suma, resta, multiplicacion, division

def main():
    continuar = "s"

    while continuar == "s":
        n1 = float(input("Introduce el primer numero: "))
        n2 = float(input("Introduce el segundo numero: "))

        print("Operaciones disponibles: ")
        print("1. Suma\n"
              "2. Resta\n"
              "3. Multiplicacion\n"
              "4. Division")
        op = input("Que operacion deseas realizar (1-4): ")

        if op == "1":
            res = suma(n1, n2)
            print("El resultado es: ", res)
        elif op == "2":
            res = resta(n1, n2)
            print("El resultado es: ", res)
        elif op == "3":
            res = multiplicacion(n1, n2)
            print("El resultado es: ", res)
        elif op == "4":
            res = division(n1, n2)
            print("El resultado es: ", res)

        continuar = input("Desea continuar? (s/n): ")

    print("Fin del programa")

if __name__ == "__main__":
    main()