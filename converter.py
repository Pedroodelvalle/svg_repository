import base64
import re
import requests

def convert_svg_images_to_base64_and_save(svg_content, output_svg_path):
    """
    Recebe o código SVG como string, 
    localiza todas as tags <image> com xlink:href ou href que contenham URL http/https,
    baixa cada imagem, converte para Base64 e substitui a URL pela string data URI,
    mantendo todo o restante do SVG intacto.
    Por fim, salva o SVG atualizado no caminho especificado.
    """
    # Expressão regular para encontrar a tag <image> com atributo xlink:href ou href
    pattern = r'(<image\b[^>]+(?:xlink:href|href)\s*=\s*["\'])(https?://[^"\'\r\n]+)(["\'])'
    
    def replace_image(match):
        prefix = match.group(1)
        url = match.group(2)
        suffix = match.group(3)
        print(f"Processando imagem: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Erro ao baixar a imagem {url}. Status: {response.status_code}")
                return match.group(0)  # Mantém a tag original se ocorrer erro
        except Exception as e:
            print(f"Exceção ao baixar a imagem {url}: {e}")
            return match.group(0)
        
        # Converte o conteúdo da imagem para Base64
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        mime_type = response.headers.get("Content-Type", "image/png")
        data_uri = f"data:{mime_type};base64,{image_base64}"
        # Retorna a tag <image> com a URL substituída pela data URI, mantendo o restante intacto
        return f"{prefix}{data_uri}{suffix}"
    
    # Substitui todas as ocorrências encontradas pela versão em Base64
    updated_svg_content = re.sub(pattern, replace_image, svg_content, flags=re.DOTALL)
    
    # Garante que o namespace xlink esteja definido na tag <svg>
    if 'xmlns:xlink' not in updated_svg_content:
        updated_svg_content = re.sub(
            r'<svg\b',
            '<svg xmlns:xlink="http://www.w3.org/1999/xlink"',
            updated_svg_content,
            count=1
        )
    
    # Salva o SVG atualizado em um arquivo
    with open(output_svg_path, "w", encoding="utf-8") as file:
        file.write(updated_svg_content)
    
    print(f"SVG convertido e salvo em: {output_svg_path}")
    return updated_svg_content

# EXEMPLO DE USO
if __name__ == "__main__":
    # Código SVG original em forma de string
    svg_code = """
  <svg width="1080" height="1350" viewBox="0 0 1080 1350" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect width="1080" height="1350" fill="white"/>
    <defs>
      <clipPath id="circleClip">
        <circle cx="165" cy="282" r="64"/>
      </clipPath>
    </defs>
    <g clip-path="url(#circleClip)">
      <image xlink:href="https://cdn.pixabay.com/photo/2023/08/06/14/34/woman-8173091_1280.jpg" x="101" y="218" width="128" height="128" preserveAspectRatio="xMidYMid slice"/>
    </g>
    <text fill="black" font-family="Inter" font-size="32" font-weight="bold" letter-spacing="-0.03em">
      <tspan x="237" y="267.136">John Kappa</tspan>
    </text>
    <text fill="#8E8E8E" font-family="Inter" font-size="32" letter-spacing="-0.03em">
      <tspan x="237" y="312.136">@johnkappa</tspan>
    </text>
    <text fill="black" font-family="Inter" font-size="50" letter-spacing="-0.03em">
      <tspan x="117" y="437.682">Sansão perdeu a força quando contou </tspan>
      <tspan x="117" y="512.682">o seu segredo. </tspan>
      <tspan x="117" y="662.682">Nem todo mundo precisa saber de </tspan>
      <tspan x="117" y="737.682">tudo. Suas maiores derrotas começam </tspan>
      <tspan x="117" y="812.682">com uma palavra mal direcionada.</tspan>
      <tspan x="117" y="962.682">Cuidado com o que fala (e pra quem </tspan>
      <tspan x="117" y="1037.68">você fala) - boca aberta, porta </tspan>
      <tspan x="117" y="1112.68">fechada.</tspan>
    </text>
  </svg>

    """
    
    output_file = "saida_base64.svg"
    convert_svg_images_to_base64_and_save(svg_code, output_file)
