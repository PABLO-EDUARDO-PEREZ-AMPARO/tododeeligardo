import heapq
from collections import Counter

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter  # None para nodos internos
        self.frecuencia = frecuencia
        self.izquierdo = None
        self.derecho = None
    
    def __lt__(self, otro):
        # Para que heapq compare por frecuencia
        return self.frecuencia < otro.frecuencia
    
    def es_hoja(self):
        return self.izquierdo is None and self.derecho is None

class Huffman:
    """
    Implementación de codificación Huffman.
    
    Nota sobre archivos reales: El archivo comprimido debe incluir
    información para reconstruir el árbol. Opciones comunes:
    1. Guardar la tabla de frecuencias al inicio
    2. Serializar el árbol (ej: recorrido preorden con marcadores)
    3. Usar códigos canónicos (solo guardar longitudes)
    """
    
    def __init__(self):
        self.raiz = None
        self.codigos = {}
        self.codigos_inversos = {}
    
    def construir_arbol(self, texto):
        """Construye el árbol de Huffman a partir de un texto."""
        # 1. Calcular frecuencias
        frecuencias = Counter(texto)
        
        if len(frecuencias) == 0:
            return
        
        # Caso especial: un solo carácter
        if len(frecuencias) == 1:
            char = list(frecuencias.keys())[0]
            self.raiz = NodoHuffman(char, frecuencias[char])
            self.codigos[char] = '0'
            self.codigos_inversos['0'] = char
            return
        
        # 2. Crear cola de prioridad con nodos hoja
        heap = []
        for caracter, freq in frecuencias.items():
            nodo = NodoHuffman(caracter, freq)
            heapq.heappush(heap, nodo)
        
        # 3. Construir árbol combinando nodos
        while len(heap) > 1:
            # Extraer los dos nodos con menor frecuencia
            izq = heapq.heappop(heap)
            der = heapq.heappop(heap)
            
            # Crear nodo padre
            padre = NodoHuffman(None, izq.frecuencia + der.frecuencia)
            padre.izquierdo = izq
            padre.derecho = der
            
            # Reinsertar en la cola
            heapq.heappush(heap, padre)
        
        # 4. El único nodo restante es la raíz
        self.raiz = heap[0]
        
        # 5. Generar códigos
        self._generar_codigos(self.raiz, "")
    
    def _generar_codigos(self, nodo, codigo_actual):
        """Genera códigos binarios recorriendo el árbol."""
        if nodo is None:
            return
        
        if nodo.es_hoja():
            self.codigos[nodo.caracter] = codigo_actual
            self.codigos_inversos[codigo_actual] = nodo.caracter
            return
        
        # 0 para izquierda, 1 para derecha
        self._generar_codigos(nodo.izquierdo, codigo_actual + "0")
        self._generar_codigos(nodo.derecho, codigo_actual + "1")
    
    def codificar(self, texto):
        """Codifica un texto usando los códigos de Huffman."""
        return ''.join(self.codigos[c] for c in texto)
    
    def decodificar(self, bits):
        """Decodifica una cadena de bits."""
        resultado = []
        nodo_actual = self.raiz
        
        for bit in bits:
            if bit == '0':
                nodo_actual = nodo_actual.izquierdo
            else:
                nodo_actual = nodo_actual.derecho
            
            if nodo_actual.es_hoja():
                resultado.append(nodo_actual.caracter)
                nodo_actual = self.raiz
        
        return ''.join(resultado)
    
    def mostrar_codigos(self):
        """Muestra la tabla de códigos."""
        print("\nTabla de códigos Huffman:")
        print("-" * 40)
        for caracter, codigo in sorted(self.codigos.items(), 
                                        key=lambda x: (len(x[1]), x[1])):
            print(f"'{caracter}': {codigo:>10} ({len(codigo)} bits)")
    
    def calcular_compresion(self, texto):
        """Calcula estadísticas de compresión."""
        bits_original = len(texto) * 8  # ASCII
        bits_huffman = len(self.codificar(texto))
        
        print(f"\nEstadísticas de compresión:")
        print(f"  Texto original: {len(texto)} caracteres")
        print(f"  Bits ASCII (8 bits/char): {bits_original}")
        print(f"  Bits Huffman: {bits_huffman}")
        print(f"  Compresión: {(1 - bits_huffman/bits_original)*100:.1f}%")
        print(f"  Ratio: {bits_huffman/bits_original:.3f}")
        
        # Nota sobre overhead del árbol
        overhead_estimado = len(self.codigos) * 10  # Estimación simple
        print(f"  (Nota: En archivo real, agregar ~{overhead_estimado} bits para el árbol)")

# Ejemplo de uso
if __name__ == "__main__":
    texto = "ABRACADABRA"
    print(f"Texto original: '{texto}'")
    
    huff = Huffman()
    huff.construir_arbol(texto)
    huff.mostrar_codigos()
    
    # Codificar
    codificado = huff.codificar(texto)
    print(f"\nCodificado: {codificado}")
    
    # Decodificar
    decodificado = huff.decodificar(codificado)
    print(f"Decodificado: {decodificado}")
    
    # Verificar
    assert texto == decodificado, "¡Error en codificación/decodificación!"
    print("✓ Verificación exitosa")
    
    # Estadísticas
    huff.calcular_compresion(texto)