def evaluar_postfija(expresion):
    """
    Evalúa una expresión en notación postfija (RPN).
    
    Conexión con árboles: El recorrido POSTORDEN de un árbol de expresión
    genera exactamente esta notación, que luego puede evaluarse linealmente.
    
    Args:
        expresion: string con tokens separados por espacios
                   Ejemplo: "3 4 + 2 *" = (3 + 4) * 2 = 14
    
    Returns:
        El resultado numérico de la expresión
    """
    pila = []
    operadores = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a / b,
        '^': lambda a, b: a ** b,
        '%': lambda a, b: a % b,
    }
    
    tokens = expresion.split()
    
    for token in tokens:
        if token in operadores:
            # Es un operador: extraer dos operandos
            if len(pila) < 2:
                raise ValueError(f"Expresión inválida: faltan operandos para '{token}'")
            
            b = pila.pop()  # Segundo operando (arriba de la pila)
            a = pila.pop()  # Primer operando
            resultado = operadores[token](a, b)
            pila.append(resultado)
        else:
            # Es un operando: convertir a número y apilar
            try:
                numero = float(token)
                pila.append(numero)
            except ValueError:
                raise ValueError(f"Token inválido: '{token}'")
    
    if len(pila) != 1:
        raise ValueError("Expresión inválida: sobran operandos")
    
    return pila[0]

# Ejemplos de uso
if __name__ == "__main__":
    ejemplos = [
        ("3 4 +", "(3 + 4)"),
        ("3 4 + 2 *", "(3 + 4) * 2"),
        ("5 1 2 + 4 * + 3 -", "5 + (1 + 2) * 4 - 3"),
        ("2 3 ^ 4 +", "2^3 + 4"),
    ]
    
    print("Evaluación de expresiones postfijas:")
    print("=" * 60)
    for postfija, infija in ejemplos:
        resultado = evaluar_postfija(postfija)
        print(f"  Postfija: {postfija:25} | Infija: {infija:20} = {resultado}")