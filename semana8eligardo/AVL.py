class NodoAVL:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # Altura del nodo (hoja = 1)

class AVL:
    def __init__(self):
        self.raiz = None
    
    def altura(self, nodo):
        """Retorna la altura de un nodo (0 si es None)."""
        return nodo.altura if nodo else 0
    
    def factor_balance(self, nodo):
        """Calcula el factor de balance: altura(izq) - altura(der)."""
        if not nodo:
            return 0
        return self.altura(nodo.izquierdo) - self.altura(nodo.derecho)
    
    def actualizar_altura(self, nodo):
        """Actualiza la altura de un nodo basándose en sus hijos."""
        nodo.altura = 1 + max(self.altura(nodo.izquierdo), 
                              self.altura(nodo.derecho))
    
    def rotacion_derecha(self, z):
        """
        Rotación simple a la derecha (caso LL).
              z                y
             / \              / \
            y   T4    →      x   z
           / \              / \ / \
          x   T3           T1 T2 T3 T4
         / \
        T1  T2
        """
        y = z.izquierdo
        T3 = y.derecho
        
        # Realizar rotación
        y.derecho = z
        z.izquierdo = T3
        
        # Actualizar alturas (¡ORDEN IMPORTA!)
        # Primero z, luego y. ¿Por qué?
        # Después de la rotación, z es HIJO de y.
        # La altura de y depende de la altura de z.
        # Si calculáramos y primero, usaríamos la altura vieja de z (incorrecta).
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        
        return y  # Nueva raíz del subárbol
    
    def rotacion_izquierda(self, z):
        """
        Rotación simple a la izquierda (caso RR).
            z                   y
           / \                 / \
          T1  y       →       z   x
             / \             / \ / \
            T2  x           T1 T2 T3 T4
               / \
              T3  T4
        """
        y = z.derecho
        T2 = y.izquierdo
        
        # Realizar rotación
        y.izquierdo = z
        z.derecho = T2
        
        # Actualizar alturas
        self.actualizar_altura(z)
        self.actualizar_altura(y)
        
        return y  # Nueva raíz del subárbol
    
    def insertar(self, valor):
        """Inserta un valor y rebalancea si es necesario."""
        self.raiz = self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo, valor):
        # 1. Inserción BST normal
        if not nodo:
            return NodoAVL(valor)
        
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar_recursivo(nodo.derecho, valor)
        else:
            return nodo  # Sin duplicados
        
        # 2. Actualizar altura del nodo actual
        self.actualizar_altura(nodo)
        
        # 3. Obtener factor de balance
        fb = self.factor_balance(nodo)
        
        # 4. Aplicar rotaciones si está desbalanceado
        
        # Caso LL: desbalance izquierdo-izquierdo
        if fb > 1 and valor < nodo.izquierdo.valor:
            return self.rotacion_derecha(nodo)
        
        # Caso RR: desbalance derecho-derecho
        if fb < -1 and valor > nodo.derecho.valor:
            return self.rotacion_izquierda(nodo)
        
        # Caso LR: desbalance izquierdo-derecho (rotación doble)
        if fb > 1 and valor > nodo.izquierdo.valor:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        
        # Caso RL: desbalance derecho-izquierdo (rotación doble)
        if fb < -1 and valor < nodo.derecho.valor:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)
        
        return nodo
    
    def inorden(self):
        """Recorrido inorden."""
        resultado = []
        self._inorden(self.raiz, resultado)
        return resultado
    
    def _inorden(self, nodo, resultado):
        if nodo:
            self._inorden(nodo.izquierdo, resultado)
            resultado.append((nodo.valor, self.factor_balance(nodo)))
            self._inorden(nodo.derecho, resultado)
    
    def mostrar_estructura(self):
        """Muestra la estructura del árbol con factores de balance."""
        def _mostrar(nodo, nivel=0, prefijo="Raíz: "):
            if nodo:
                print(" " * (nivel * 4) + prefijo + 
                      f"{nodo.valor} (FB={self.factor_balance(nodo)}, h={nodo.altura})")
                if nodo.izquierdo or nodo.derecho:
                    _mostrar(nodo.izquierdo, nivel + 1, "Izq: ")
                    _mostrar(nodo.derecho, nivel + 1, "Der: ")
        _mostrar(self.raiz)

# Ejemplo de uso
if __name__ == "__main__":
    avl = AVL()
    
    # Insertar en orden (causaría degeneración en BST normal)
    print("Insertando: 10, 20, 30, 40, 50, 25")
    for valor in [10, 20, 30, 40, 50, 25]:
        avl.insertar(valor)
        print(f"\nDespués de insertar {valor}:")
        avl.mostrar_estructura()
    
    print("\nInorden con FB:", avl.inorden())