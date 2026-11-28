import time, urllib.request
unidades = ["PREAMBULO", "ART_1", "ART_2", "ART_14", "ART_33", "ART_47", "ART_56", "ART_135", "ART_168", "DD_UNICA"]
for u in unidades:
    print(f"Pre-auditando {u}...")
    try:
        urllib.request.urlopen(f"http://127.0.0{u}", timeout=60)
        print(f"  [OK] {u} guardado en cache instantanea.")
    except Exception as e:
        print(f"  [AVISO] {u}: {e}")
    time.sleep(3)
