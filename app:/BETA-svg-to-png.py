import cairosvg
import requests
from io import BytesIO

# URL do arquivo SVG armazenado no Supabase
svg_url = "https://brnwkkmdghyqezcwbyxz.supabase.co/storage/v1/object/sign/svg/saida_base64%20(2).svg?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzdmcvc2FpZGFfYmFzZTY0ICgyKS5zdmciLCJpYXQiOjE3NDE4MDgwMTIsImV4cCI6MTc0MjQxMjgxMn0.K0ve2oOI5jq1TqITqfHaneZXx3dGkVGQeAZHmT928BE"

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
