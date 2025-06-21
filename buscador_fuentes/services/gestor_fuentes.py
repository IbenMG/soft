import json
from pathlib import Path

RUTA_JSON = Path("etiquetas_fuentes.json")

class FuenteManager:

    def __init__(self):
        self.data = self._cargar()

    def _cargar(self):
        if RUTA_JSON.exists():
            with open(RUTA_JSON, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _guardar(self):
        with open(RUTA_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def registrar_fuente(self, nombre, url, etiquetas):
        for etiqueta in etiquetas:
            self.data.setdefault(etiqueta, []).append({
                "nombre": nombre,
                "link": url
            })
        self._guardar()

    def buscar_por_etiqueta(self, etiqueta):
        return self.data.get(etiqueta, [])

    def listar_todo(self):
        return dict(self.data)

    def eliminar_fuente(self, nombre):
        for fuentes in self.data.values():
            fuentes[:] = [f for f in fuentes if f.get("nombre") != nombre]
        self._guardar()

    def actualizar_fuente(self, nombre, nuevo_nombre=None, nuevo_url=None, nuevas_etiquetas=None):
        detalles = None
        # Buscar fuente
        for fuentes in self.data.values():
            for fuente in fuentes:
                if fuente.get("nombre") == nombre:
                    detalles = fuente.copy()
                    fuente["nombre"] = nuevo_nombre or fuente["nombre"]
                    fuente["link"] = nuevo_url or fuente["link"]

        if nuevas_etiquetas and detalles:
            self.eliminar_fuente(nombre)
            self.registrar_fuente(
                nuevo_nombre or detalles["nombre"],
                nuevo_url or detalles["link"],
                nuevas_etiquetas
            )
