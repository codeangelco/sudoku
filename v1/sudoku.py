import itertools as it
import time
    
class Sudoku:
    def __init__(self) -> None:
        columnas : str = "ABCDEFGHI"
        keys : list[tuple[int, str]] = list(it.product(range(1,10), columnas))
        
        self.strKeys : list[str] = [f"{key[1]}{key[0]}" for key in keys]
        self.tab_dom : dict[str, set[int]] = {key: set(range(1, 10)) for key in self.strKeys}
    
    
    def __str__(self) -> str:
        resultado = ""
        for i in range(9):
            for j in range(9):
                key = self.strKeys[i * 9 + j]
                if len(self.tab_dom[key]) == 1:
                    resultado += str(list(self.tab_dom[key])[0])
                else:
                    resultado += "."
                if (j + 1) % 3 == 0 and j < 8:
                    resultado += "|"
            resultado += "\n"
            if (i + 1) % 3 == 0 and i < 8:
                resultado += "-" * 11 + "\n"
        return resultado
                
        
    def establecerValoresIniciales(self, logs : bool = False) -> None:
        with open("C:\\Users\\jaram\\codes\\sudoku\\v1\\src\\tablas.txt", "r") as f:
            tabla: str = input("Ingrese el numero de tabla a tratar: ")
            lineas: list[str] = f.readlines()
            id: int = lineas.index(f"Grid {tabla}\n")
            for linea, i in zip(lineas[id + 1 : id + 10], range(9)):
                for key, valor in zip(self.strKeys[i * 9 : i * 9 + 9], linea):
                    if int(valor) == 0:
                        continue
                    if logs:
                        print(f"Asignando en {key} el valor {valor}")
                    self.tab_dom[key] = {int(valor)}
    
    
    def allDif(self, logs : bool = False, contador : int = 0):
        actualizacion = False
        for i in range(9):
            for j in range(9):
                key = self.strKeys[i * 9 + j]
                if len(self.tab_dom[key]) != 1:
                    continue
                if logs:
                    print(f"Valor unico {self.tab_dom[key]} en {key}")
                letra, numero = key
                for _letra in "ABCDEFGHI":
                    if _letra == letra:
                        continue
                    llave = f"{_letra}{numero}"
                    if len(self.tab_dom[llave].intersection(self.tab_dom[key])) == 0 :
                        continue
                    actualizacion = True
                    if logs:
                        print(f"Retirando {self.tab_dom[key]} de {llave}")
                    self.tab_dom[llave].difference_update(self.tab_dom[key])
                for _numero in range(1,10):
                    if _numero == int(numero):
                        continue
                    llave: str = f"{letra}{_numero}"
                    if len(self.tab_dom[llave].intersection(self.tab_dom[key])) == 0 :
                        continue
                    actualizacion = True
                    if logs:
                        print(f"Retirando {self.tab_dom[key]} de {llave}")
                    self.tab_dom[llave].difference_update(self.tab_dom[key])
        if actualizacion:
            if logs:
                print("Hubo actualizaciones, repitiendo proceso. (allDif)")
                time.sleep(10) 
            return self.allDif(logs, contador + 1)
        else:
            return contador
    
    
    def finBlock(self, logs : bool = False, contador : int = 0):
        actualizacion = False
        for i in range(9):
            for j in range(9):
                key = self.strKeys[i * 9 + j]
                dominio = self.tab_dom[key].copy()
                if len(dominio) == 1:
                    continue
                if logs:
                    print(f"Revisando {key} con dominio {dominio}")
                for x in range(i // 3 * 3, i // 3 * 3 + 3):
                    for y in range(j // 3 * 3, j // 3 * 3 + 3):
                        llave = self.strKeys[x * 9 + y]
                        if key == llave:
                            continue
                        if dominio - self.tab_dom[llave] == dominio:
                            continue
                        dominio -= self.tab_dom[llave]
                if len(dominio) > 0 and dominio != self.tab_dom[key]:
                    if logs:
                        print("Descartando...")
                    actualizacion = True
                    self.tab_dom[key] = dominio
        if actualizacion:
            if logs:
                print("Hubo actualizaciones, repitiendo proceso. (finBlock)")
                time.sleep(10)
            return self.finBlock(logs, contador + 1)
        else:
            return contador
    

    def resolver(self, logs : bool = False):
        contador = 1
        while contador > 0:
            contador = self.allDif(logs)
            contador += self.finBlock(logs)
            if logs:
                if contador > 0:
                    print("\tSe siguen encontrando valores. (resolver)")
                else:
                    print("\tSe dejaron de encontar valores. (resolver)")
                time.sleep(5)
                