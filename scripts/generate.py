import json
import os
from datetime import datetime, UTC

# Inputs desde env/vars para mostrar cómo parametrizar
commit = os.getenv("GITHUB_SHA", "local-dev")[:7]
run_number = os.getenv("GITHUB_RUN_NUMBER", "0")
message = os.getenv("POC_MESSAGE", "Hola mundo desde GitHub Actions!")

print(f" ✓ Generando artefactos de build desde rama feature/add-artifact")

# Directorio de salida
out_dir = os.getenv("OUT_DIR", "dist")
os.makedirs(out_dir, exist_ok=True)

# Generar archivo JSON
payload = {
    "poc": True,
    "message": message,
    "commit": commit,
    "run": run_number,
    "timestamp": datetime.now(UTC).isoformat(),
}

json_file = os.path.join(out_dir, f"build-{run_number}-{commit}.json")
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"✓ Artefacto JSON generado: {json_file}")

# Generar archivo de texto simple
txt_file = os.path.join(out_dir, f"build-{run_number}-{commit}.txt")
with open(txt_file, "w", encoding="utf-8") as f:
    f.write(f"=== Build Artifact ===\n\n")
    f.write(f"Mensaje: {message}\n")
    f.write(f"Commit: {commit}\n")
    f.write(f"Run: {run_number}\n")
    f.write(f"Timestamp: {datetime.now(UTC).isoformat()}\n")
    f.write(f"\nBuild completado exitosamente!\n")

print(f"✓ Artefacto TXT generado: {txt_file}")
print(f"\n✓ Build completado - {len(os.listdir(out_dir))} archivos generados")
