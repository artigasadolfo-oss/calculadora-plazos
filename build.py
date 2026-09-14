#!/usr/bin/env python3
"""Mantiene sincronizada la LÓGICA DE CÓMPUTO entre plantilla.html e index.html.

Por qué existe: la sustitución de __DATOS__ se hacía a mano, así que index.html
y plantilla.html se desincronizaron sin que nadie lo notara. Un fallo de cómputo
corregido solo en el index sobrevivía en la plantilla, y de la plantilla nacen
las siguientes herramientas de la familia.

    python3 build.py --check    # NO escribe; sale 1 si divergen (usar antes de publicar)
    python3 build.py --sync     # trae a index.html la lógica de la plantilla

CUIDADO — por qué NO se regenera el index entero desde la plantilla:
index.html incorpora el logo del despacho embebido en base64 (~18 KB) que la
plantilla NO contiene. Sobrescribir el index con la plantilla renderizada
BORRARÍA ese logo. Por eso `--sync` conserva la cabecera del index (estilos e
iconos) y sustituye únicamente el bloque de lógica, que es lo que computa
plazos y lo único que debe estar sincronizado.
"""
import argparse
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
PLANTILLA = BASE / "plantilla.html"
DATOS = BASE / "datos_festivos.json"
INDEX = BASE / "index.html"
MARCADOR = "__DATOS__"

# Frontera entre la cabecera (estilos, iconos, maquetación: propia de cada
# fichero) y la lógica de cómputo (común y sincronizable).
ANCLA = "const TIPOS"


def parte_logica(texto: str, quien: str) -> tuple[str, str]:
    """Devuelve (cabecera, lógica) partiendo por el ancla."""
    i = texto.find(ANCLA)
    if i == -1:
        raise SystemExit(f"ERROR: no se encuentra el ancla {ANCLA!r} en {quien}. "
                         "¿Ha cambiado la estructura del fichero?")
    return texto[:i], texto[i:]


def logica_de_la_plantilla() -> str:
    plantilla = PLANTILLA.read_text(encoding="utf-8")
    if MARCADOR not in plantilla:
        raise SystemExit(f"ERROR: {PLANTILLA.name} no contiene {MARCADOR}.")
    datos = json.loads(DATOS.read_text(encoding="utf-8"))  # valida el JSON
    render = plantilla.replace(MARCADOR, json.dumps(datos, ensure_ascii=False))
    return parte_logica(render, PLANTILLA.name)[1]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true",
                   help="no escribe; falla (exit 1) si la lógica diverge")
    g.add_argument("--sync", action="store_true",
                   help="copia a index.html la lógica de la plantilla (conserva su cabecera)")
    args = ap.parse_args()
    if not (args.check or args.sync):
        args.check = True  # por defecto, el modo seguro

    if not INDEX.exists():
        print(f"FALLO: no existe {INDEX.name}.")
        return 1

    actual = INDEX.read_text(encoding="utf-8")
    cabecera_index, logica_index = parte_logica(actual, INDEX.name)
    logica_plantilla = logica_de_la_plantilla()

    if logica_index == logica_plantilla:
        print("OK: index.html y plantilla.html tienen la MISMA lógica de cómputo.")
        return 0

    if args.sync:
        INDEX.write_text(cabecera_index + logica_plantilla, encoding="utf-8")
        print(f"OK: lógica sincronizada en {INDEX.name} "
              f"(cabecera y logo del index conservados).")
        return 0

    print("FALLO: index.html y plantilla.html DIFIEREN en la lógica de cómputo.")
    print("Un arreglo aplicado a uno solo NO llegará al otro.")
    import difflib
    diff = list(difflib.unified_diff(
        logica_index.splitlines(), logica_plantilla.splitlines(),
        "index.html", "plantilla.html (renderizada)", n=1, lineterm=""))
    for linea in diff[:40]:
        print("  " + linea)
    if len(diff) > 40:
        print(f"  … y {len(diff) - 40} líneas más.")
    print("\nRevise cuál de los dos es el bueno y ejecute: python3 build.py --sync")
    return 1


if __name__ == "__main__":
    sys.exit(main())
