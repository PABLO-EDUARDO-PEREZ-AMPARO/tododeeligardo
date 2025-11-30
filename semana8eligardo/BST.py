class NodoBST:
    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None

class BST:
    """
    Árbol Binario de Búsqueda.
    
    Decisión de diseño: No permite duplicados (actúa como conjunto).
    Para permitir duplicados, se podría:
    - Agregar un contador en cada nodo
    - Insertar duplicados sistemáticamente a la izquierda o derecha
    """
    
    def __init__(self):
        self.raiz = None
    
    def insertar(self, valor):
        """Inserta un valor en el BST."""
        if not self.raiz:
            self.raiz = NodoBST(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)
    
    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierdo is None:
                nodo.izquierdo = NodoBST(valor)
            else:
                self._insertar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            if nodo.derecho is None:
                nodo.derecho = NodoBST(valor)
            else:
                self._insertar_recursivo(nodo.derecho, valor)
        # Si valor == nodo.valor, no insertamos (sin duplicados)
    
    def buscar(self, valor):
        """Busca un valor en el BST. Retorna True si existe."""
        return self._buscar_recursivo(self.raiz, valor)
    
    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if valor == nodo.valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierdo, valor)
        else:
            return self._buscar_recursivo(nodo.derecho, valor)
    
    def eliminar(self, valor):
        """
        Elimina un valor del BST.
        Maneja los 3 casos: hoja, un hijo, dos hijos.
        """
        self.raiz = self._eliminar_recursivo(self.raiz, valor)
    
    def _eliminar_recursivo(self, nodo, valor):
        # Caso base: no encontramos el valor
        if nodo is None:
            return None
        
        # Buscar el nodo a eliminar
        if valor < nodo.valor:
            nodo.izquierdo = self._eliminar_recursivo(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, valor)
        else:
            # ¡Encontramos el nodo a eliminar!
            
            # CASO 1: Nodo hoja (sin hijos)
            if nodo.izquierdo is None and nodo.derecho is None:
                return None
            
            # CASO 2a: Solo tiene hijo derecho
            if nodo.izquierdo is None:
                return nodo.derecho
            
            # CASO 2b: Solo tiene hijo izquierdo
            if nodo.derecho is None:
                return nodo.izquierdo
            
            # CASO 3: Tiene dos hijos
            # Encontrar el sucesor inorden (mínimo del subárbol derecho)
            sucesor = self._encontrar_minimo(nodo.derecho)
            
            # Copiar el valor del sucesor al nodo actual
            nodo.valor = sucesor.valor
            
            # Eliminar el sucesor del subárbol derecho
            nodo.derecho = self._eliminar_recursivo(nodo.derecho, sucesor.valor)
        
        return nodo
    
    def _encontrar_minimo(self, nodo):
        """Encuentra el nodo con valor mínimo (ir siempre a la izquierda)."""
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual
    
    def inorden(self):
        """Recorrido inorden (produce elementos ordenados)."""
        resultado = []
        self._inorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _inorden_recursivo(self, nodo, resultado):
        if nodo:
            self._inorden_recursivo(nodo.izquierdo, resultado)
            resultado.append(nodo.valor)
            self._inorden_recursivo(nodo.derecho, resultado)
    
    def preorden(self):
        """Recorrido preorden."""
        resultado = []
        self._preorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _preorden_recursivo(self, nodo, resultado):
        if nodo:
            resultado.append(nodo.valor)
            self._preorden_recursivo(nodo.izquierdo, resultado)
            self._preorden_recursivo(nodo.derecho, resultado)
    
    def postorden(self):
        """Recorrido postorden."""
        resultado = []
        self._postorden_recursivo(self.raiz, resultado)
        return resultado
    
    def _postorden_recursivo(self, nodo, resultado):
        if nodo:
            self._postorden_recursivo(nodo.izquierdo, resultado)
            self._postorden_recursivo(nodo.derecho, resultado)
            resultado.append(nodo.valor)
    
    def minimo(self):
        """Encuentra el valor mínimo."""
        if not self.raiz:
            return None
        return self._encontrar_minimo(self.raiz).valor
    
    def maximo(self):
        """Encuentra el valor máximo."""
        if not self.raiz:
            return None
        nodo = self.raiz
        while nodo.derecho:
            nodo = nodo.derecho
        return nodo.valor

# Ejemplo de uso con pruebas de eliminación
if __name__ == "__main__":
    bst = BST()
    valores = [50, 30, 70, 20, 40, 60, 80]
    
    print("Insertando:", valores)
    for v in valores:
        bst.insertar(v)
    
    print("Inorden:", bst.inorden())
    
    # Probar eliminación - Caso 1: hoja
    print("\nEliminando 20 (hoja)...")
    bst.eliminar(20)
    print("Inorden:", bst.inorden())
    
    # Probar eliminación - Caso 2: un hijo
    print("\nInsertando 25, eliminando 30 (un hijo)...")
    bst.insertar(25)
    bst.eliminar(30)
    print("Inorden:", bst.inorden())
    
    # Probar eliminación - Caso 3: dos hijos
    print("\nEliminando 50 (dos hijos, raíz)...")
    bst.eliminar(50)
    print("Inorden:", bst.inorden())