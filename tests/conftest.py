"""Configuración compartida de pytest — agrega src/ al path de importación.

Los scripts de src/ están pensados para ejecutarse como scripts sueltos
(`python pipeline.py`), no como paquete instalado, así que los tests los
importan agregando src/ al sys.path acá en vez de necesitar un `pip install -e .`.
Importar estos módulos NO debe correr el pipeline ni tocar el disco más allá
de leer sus propios constantes — todo el código con efectos (leer archivos,
escribir CSV) vive dentro de `main()`, protegido por `if __name__ == "__main__"`.
"""
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
