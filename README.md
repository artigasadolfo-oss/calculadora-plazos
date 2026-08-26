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

El cómputo definitivo de un plazo es responsabilidad exclusiva y final del letrado.
