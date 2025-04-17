from sickle import Sickle
import os

# URL base do repositório OAI-PMH
BASE_URL = "https://www.arquivoalbertosampaio.org/OAI-PMH/"

# Inicializar o cliente OAI-PMH
sickle = Sickle(BASE_URL)

# Escolher o metadataPrefix - pode ser 'oai_dc' ou outro suportado
metadata_prefix = "oai_dc"

# Diretório de output
output_dir = "registos_oai"
os.makedirs(output_dir, exist_ok=True)

# Recolher os registos
records = sickle.ListRecords(metadataPrefix=metadata_prefix)

# Guardar os registos em ficheiros separados
for i, record in enumerate(records):
    with open(os.path.join(output_dir, f"record_{i}.xml"), "w", encoding="utf-8") as f:
        f.write(str(record.raw))
    if i >= 50:  # limite opcional para testes
        break

print(f"{i+1} registos guardados em '{output_dir}/'")
