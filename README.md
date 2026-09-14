# Calculadora de plazos procesales — Artigas Abogados

Herramienta interna. Cómputo de plazos procesales civiles (LEC) con:

- Reglas de los arts. 130, 133 y 135.5 LEC (día de gracia hasta las 15:00)
- Agosto y 24-dic/6-ene inhábiles; modo urgente (agosto corre)
- **Festivos locales según la sede del órgano judicial** (Benidorm por defecto;
  Villajoyosa y Alicante destacadas; los 129 municipios de la provincia)
- Calendarios verificados contra el DOGV: Decreto 100/2025 (laboral CV 2026),
  Decreto 42/2026 (laboral CV 2027), Resolución 12/11/2025 (fiestas locales 2026)
- Tipos de plazo predefinidos (contestación, recursos, ejecución, concursal)
  con su artículo, cómputo natural/sustantivo, y calendario visual del cómputo

Motor idéntico a `computa_plazo.py` (skill `plazos-procesales` del despacho);
paridad verificada caso a caso el 26/08/2026 (13/13).

## Mantenimiento: index.html y plantilla.html

`plantilla.html` es el molde de la familia de herramientas (lleva `__DATOS__`
como marcador de los festivos); `index.html` es lo que se publica. La lógica de
cómputo debe ser **la misma en los dos**: un arreglo aplicado solo al index
sobrevive en la plantilla y renace en la siguiente herramienta que salga de ella.

```bash
python3 build.py --check   # falla (exit 1) si la lógica diverge — antes de publicar
python3 build.py --sync    # trae a index.html la lógica de la plantilla
```

`--sync` conserva la cabecera del index (estilos y **logo del despacho embebido
en base64**, que la plantilla no tiene): solo sustituye el bloque de lógica.

El cómputo definitivo de un plazo es responsabilidad exclusiva y final del letrado.
