import os
print("Directorio actual:", os.getcwd())
print("Variables de entorno:")
for key, value in os.environ.items():
    if 'DATABASE' in key or 'REHAB' in key.upper():
        print(f"  {key}: {value}")