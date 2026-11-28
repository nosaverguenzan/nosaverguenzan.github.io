import os, sqlite3
BLOQUES = {
  "SOBERANIA": ("Proudhon («El Principio Federativo»), Bakunin («Estatismo y anarquia»), Stirner («El Unico y su propiedad»), Rocker («Nacionalismo y cultura»)", "estado OR soberania OR monarquia"),
  "PROPIEDAD": ("Kropotkin («La conquista del pan»), Proudhon («¿Que es la propiedad?»), Malatesta («La anarquia»)", "propiedad OR capital OR riqueza"),
  "REPRESION": ("Kropotkin («Las prisiones»), Tolstoy («El reino de Dios esta en vosotros»), Goldman («Anarquismo y otros ensayos»)", "ley OR prision OR justicia"),
  "TERRITORIO": ("Pi y Margall («Las nacionalidades»), Proudhon («El Principio Federativo»), Cappelletti («La Ideologia Anarquista»)", "federacion OR autonomia OR municipio"),
  "PATRIARCADO": ("Emma Goldman («La tragedia de la emancipacion de la mujer»), Federica Montseny, Voltairine de Cleyre", "mujer OR familia OR igualdad"),
  "ECOLOGIA": ("Elisee Reclus («El hombre y la tierra»), Murray Bookchin («Ecologia de la libertad»), Kropotkin", "tierra OR vivienda OR comunal"),
  "EDUCACION": ("Francisco Ferrer Guardia («La Escuela Moderna»), Bakunin («Dios y el Estado»), Sebastien Faure", "educacion OR escuela OR religion"),
  "RUPTURA": ("VV.AA. («La destruccion del estado»), Gustav Landauer («La revolucion»), Errico Malatesta", "revolucion OR constitucion OR pacto")
}
def obtener_bloque_doctrinal(uid, titulo):
  t = (uid + " " + titulo).upper()
  k = "PROPIEDAD" if any(x in t for x in ["31","33","35","38","128","135"]) else ("REPRESION" if any(x in t for x in ["17","24","25","117"]) else ("TERRITORIO" if any(x in t for x in ["ART_2","137","143","149","155","DA_","DT_"]) else ("PATRIARCADO" if any(x in t for x in ["14","32","39"]) else ("ECOLOGIA" if any(x in t for x in ["45","47","132"]) else ("EDUCACION" if any(x in t for x in ["16","20","27"]) else ("RUPTURA" if any(x in t for x in ["166","167","168","169","DD_","DF_"]) else "SOBERANIA"))))))
  aut, q = BLOQUES[k]
  citas = ""
  for r in ["../cerebro_filosofico.db", "/storage/emulated/0/Documents/tratado_bibliografia/cerebro_filosofico.db"]:
    if os.path.exists(r):
      try:
        cn = sqlite3.connect(r); rows = cn.execute("SELECT autor, titulo, substr(contenido,1,900) FROM libros_fts WHERE libros_fts MATCH ? ORDER BY bm25(libros_fts) LIMIT 5", (q,)).fetchall(); cn.close()
        citas = "\n".join(f"- {a} en «{ti}»: {tx}" for a,ti,tx in rows); break
      except Exception: pass
  return f"BLOQUE: {k}\nAUTORES: {aut}\n{citas}"
