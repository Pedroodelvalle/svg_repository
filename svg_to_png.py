import cairosvg
import requests
from io import BytesIO

# URL do arquivo SVG armazenado no Supabase
svg_url = "https://brnwkkmdghyqezcwbyxz.supabase.co/storage/v1/object/sign/svg/saida_base64.svg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdmcvc2FpZGFfYmFzZTY0LnN2ZyIsImlhdCI6MTc0MTgwNzQxNCwiZXhwIjoxNzQyNDEyMjE0fQ.-gT45FAk5uWnQddq5-9FMoYTThi_cSjosETr5W6KsDI"

# Baixa o SVG do Supabase
response = requests.get(svg_url)
if response.status_code == 200:
    svg_data = BytesIO(response.content)
    
    # Converte o SVG para PNG e salva localmente
    output_path = "output.png"
    cairosvg.svg2png(file_obj=svg_data, write_to=output_path)
    
    print(f"Imagem convertida para PNG com sucesso! Salva como {output_path}")

else:
    print("Erro ao baixar o SVG")
