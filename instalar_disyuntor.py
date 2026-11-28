import os, time

s = open("app.py").read()
i = s.find("host = ")
j = s.find("if resp.status_code != 200:")

nuevo_motor = '''import time
            if not hasattr(SinstitucionHandler, "pausados"):
                SinstitucionHandler.pausados = {}
            ahora_ts = time.time()
            host = ".".join(["generativelanguage", "googleapis", "com"])
            cola = ["gemini-2.5-flash", "gemini-2.5-flash-lite", "gemma-3-27b-it", "gemini-2.0-flash-lite"]
            resp = None

            groq_key = os.environ.get("GROQ_API_KEY", "")
            if groq_key and SinstitucionHandler.pausados.get("groq", 0) < ahora_ts:
                gh = ".".join(["api", "groq", "com"])
                rg = requests.post("https" + f"://{gh}/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "system", "content": MASTER_PROMPT_SISTEMA}, {"role": "user", "content": prompt_usuario}]},
                    timeout=60)
                if rg.status_code == 200:
                    tg = rg.json()["choices"][0]["message"]["content"]
                    class FakeResp:
                        status_code = 200
                        def json(self): return {"candidates": [{"content": {"parts": [{"text": tg}]}}]}
                    resp = FakeResp()
                else:
                    SinstitucionHandler.pausados["groq"] = ahora_ts + 900

            if not resp:
                for m in cola:
                    if SinstitucionHandler.pausados.get(m, 0) > ahora_ts:
                        continue
                    url_api = "https" + f"://{host}/v1beta/models/{m}:generateContent"
                    if "gemma" in m:
                        pl = {"contents": [{"parts": [{"text": MASTER_PROMPT_SISTEMA + "\\n\\n" + prompt_usuario}]}]}
                    else:
                        pl = {"systemInstruction": {"parts": [{"text": MASTER_PROMPT_SISTEMA}]}, "contents": [{"parts": [{"text": prompt_usuario}]}]}
                    resp = requests.post(url_api, headers={"x-goog-api-key": GEMINI_API_KEY, "Content-Type": "application/json"}, json=pl, timeout=90)
                    if resp.status_code == 200:
                        print(f"[MOTOR OK] Respondio: {m}")
                        break
                    print(f"[DISYUNTOR] {m} dio {resp.status_code} -> aparcado 15 min.")
                    SinstitucionHandler.pausados[m] = ahora_ts + 900
            '''

open("app.py", "w").write(s[:i] + nuevo_motor + s[j:])
print("PASO 1 COMPLETADO: Disyuntor instalado en app.py")
