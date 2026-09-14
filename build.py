#!/usr/bin/env python3
"""Genera index.html a partir de plantilla.html + datos_festivos.json + logo-sidebar.png.

`plantilla.html` es la fuente ÚNICA de verdad: maquetación, formulario y lógica
de cómputo. `index.html` es un artefacto derivado que se publica.

    python3 build.py            # regenera index.html
    python3 build.py --check    # NO escribe; sale 1 si index.html está desfasado

Marcadores que sustituye la plantilla (son DOS, no uno):
    __DATOS__   -> datos_festivos.json embebido
    __LOGO__    -> logo-sidebar.png como data-URI base64

Historia que explica el diseño: antes se sustituía a mano solo __DATOS__, y un
arreglo del cómputo aplicado únicamente al index sobrevivió en la plantilla. Una
primera versión de este script sincronizaba solo el bloque JS y dejaba fuera el
FORMULARIO, de modo que un campo nuevo declarado en la plantilla no llegaba al
index y la página quedaba rota (el JS leía un input inexistente). Por eso ahora
se regenera el fichero ENTERO: cabecera, formulario y lógica.
"""
import argparse
import base64
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent
PLANTILLA = BASE / "plantilla.html"
DATOS = BASE / "datos_festivos.json"
LOGO = BASE / "logo-sidebar.png"
INDEX = BASE / "index.html"


def construye() -> str:
    plantilla = PLANTILLA.read_text(encoding="utf-8")
    faltan = [m for m in ("__DATOS__", "__LOGO__") if m not in plantilla]
    if faltan:
        raise SystemExit(f"ERROR: {PLANTILLA.name} no contiene {', '.join(faltan)}. "
                         "Si ha cambiado la plantilla, actualice build.py.")
    datos = json.loads(DATOS.read_text(encoding="utf-8"))  # valida el JSON
    logo = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    return (plantilla
            .replace("__DATOS__", json.dumps(datos, ensure_ascii=False))
            .replace("__LOGO__", f"data:image/png;base64,{logo}"))


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="no escribe; falla (exit 1) si index.html está desfasado")
    args = ap.parse_args()

    for f in (PLANTILLA, DATOS, LOGO):
        if not f.exists():
            print(f"FALLO: falta {f.name}.")
            return 1

    generado = construye()

    if not args.check:
        INDEX.write_text(generado, encoding="utf-8")
        print(f"OK: {INDEX.name} regenerado desde {PLANTILLA.name} "
              f"({len(generado):,} caracteres).")
        return 0

    if not INDEX.exists():
        print(f"FALLO: no existe {INDEX.name}. Ejecute: python3 build.py")
        return 1

    actual = INDEX.read_text(encoding="utf-8")
    if actual == generado:
        print("OK: index.html está al día respecto de plantilla.html.")
        return 0

    print("FALLO: index.html NO coincide con lo que genera plantilla.html.")
    print("Un cambio aplicado a uno solo de los dos no llega al otro.")
    import difflib
    a, b = actual.splitlines(), generado.splitlines()
    diff = [l for l in difflib.unified_diff(a, b, "index.html (en disco)",
                                            "plantilla.html (renderizada)",
                                            n=0, lineterm="")]
    for linea in diff[:30]:
        print("  " + (linea[:160] + " …" if len(linea) > 160 else linea))
    if len(diff) > 30:
        print(f"  … y {len(diff) - 30} líneas más.")
    print("\nRegenere con: python3 build.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
