import base64
import re
import requests
import os

def convert_svg_images_to_base64_and_save(svg_content, output_folder):
    """
    Recebe um código SVG contendo múltiplos documentos <svg>,
    substitui todas as imagens externas (<image> com href ou xlink:href) por versões em Base64.
    Salva cada SVG convertido separadamente no diretório especificado.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Expressão regular para capturar todos os SVGs no documento
    svg_pattern = r'(<svg[^>]*>.*?</svg>)'
    svg_matches = re.findall(svg_pattern, svg_content, flags=re.DOTALL)
    
    if not svg_matches:
        print("Nenhum SVG encontrado no documento.")
        return []
    
    # Expressão regular para encontrar todas as imagens dentro de um SVG
    image_pattern = r'(<image\b[^>]+(?:xlink:href|href)\s*=\s*[\"\'])(https?://[^"\'\r\n]+)([\"\'])'
    
    def replace_image(match):
        prefix, url, suffix = match.groups()
        print(f"Processando imagem: {url}")
        
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Erro ao baixar a imagem {url}. Status: {response.status_code}")
                return match.group(0)
        except Exception as e:
            print(f"Exceção ao baixar a imagem {url}: {e}")
            return match.group(0)
        
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        mime_type = response.headers.get("Content-Type", "image/png")
        data_uri = f"data:{mime_type};base64,{image_base64}"
        
        return f"{prefix}{data_uri}{suffix}"
    
    output_files = []
    
    for index, svg in enumerate(svg_matches):
        updated_svg = re.sub(image_pattern, replace_image, svg, flags=re.DOTALL)
        
        # Garante que o namespace xlink esteja definido na tag <svg>
        if 'xmlns:xlink' not in updated_svg:
            updated_svg = re.sub(
                r'<svg\b',
                '<svg xmlns:xlink="http://www.w3.org/1999/xlink"',
                updated_svg,
                count=1
            )
        
        output_file = os.path.join(output_folder, f"svg_converted_{index+1}.svg")
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(updated_svg)
        
        output_files.append(output_file)
        print(f"SVG convertido e salvo em: {output_file}")
    
    return output_files

# EXEMPLO DE USO
if __name__ == "__main__":
    svg_code = """<svg width='1080' height='1350' viewBox='0 0 1080 1350' fill='none' xmlns='http://www.w3.org/2000/svg'><rect width='1080' height='1350' fill='white'/><image href='https://www.cnnbrasil.com.br/wp-content/uploads/sites/12/2023/09/GettyImages-1668971338-e1694439970587.jpg?w=1200&h=900&crop=1' x='0' y='0' width='1080' height='1350' preserveAspectRatio='xMidYMid slice'/><rect x='0' y='850' width='1080' height='500' fill='black' opacity='0.9'/><text x='80' y='100' fill='white' font-family='Inter' font-size='50' font-weight='bold'>@pedrodelvalle</text><text x='50' y='950' fill='white' font-family='Inter' font-size='80' font-weight='bold' letter-spacing='-0.02em'><tspan x='50' dy='0'>VOCÊ PISCOU E O NEYMAR</tspan><tspan x='50' dy='100'>TROCOU OS CAMPOS POR</tspan><tspan x='50' dy='100'>UM MERCADO BILIONÁRIO!</tspan></text><text x='60' y='1270' fill='white' font-family='Inter' font-size='40' font-weight='bold'>O golpe de mestre que ninguém percebeu 👉</text></svg><svg width='1080' height='1350' viewBox='0 0 1080 1350' fill='none' xmlns='http://www.w3.org/2000/svg'><rect width='1080' height='1350' fill='white'/><defs><clipPath id='circleClip'><circle cx='165' cy='242' r='64'/></clipPath></defs><g clip-path='url(#circleClip)'><image xlink:href='https://assets.goal.com/images/v3/blt47f09058442f3c14/neymar-close.jpg' x='101' y='178' width='128' height='128' preserveAspectRatio='xMidYMid slice'/></g><text fill='black' font-family='Inter' font-size='32' font-weight='bold'><tspan x='237' y='227'>Pedro Del Valle</tspan></text><text fill='#8E8E8E' font-family='Inter' font-size='32'><tspan x='237' y='272'>@pedrodelvalle</tspan></text><text fill='black' font-family='Inter' font-size='50'><tspan x='117' y='437'>Turma, o Neymar não voltou só pra</tspan><tspan x='117' y='512'>jogar bola...</tspan><tspan x='117' y='670'>Ele voltou pra jogar o jogo dos negócios</tspan><tspan x='117' y='750'>e esse ele tá levando de lavada...</tspan><tspan x='117' y='890'>No meio do seu maior hype de todos os</tspan><tspan x='117' y='970'>tempos ele lançou a Next10, a sua própria</tspan><tspan x='117' y='1050'>marca de suplementos...</tspan></text></svg><svg width='1080' height='1350' viewBox='0 0 1080 1350' fill='none' xmlns='http://www.w3.org/2000/svg'><rect width='1080' height='1350' fill='white'/><defs><clipPath id='circleClip'><circle cx='165' cy='242' r='64'/></clipPath></defs><g clip-path='url(#circleClip)'><image xlink:href='https://assets.goal.com/images/v3/blt47f09058442f3c14/neymar-close.jpg' x='101' y='178' width='128' height='128' preserveAspectRatio='xMidYMid slice'/></g><text fill='black' font-family='Inter' font-size='32' font-weight='bold'><tspan x='237' y='227'>Pedro Del Valle</tspan></text><text fill='#8E8E8E' font-family='Inter' font-size='32'><tspan x='237' y='272'>@pedrodelvalle</tspan></text><text fill='black' font-family='Inter' font-size='50'><tspan x='117' y='437'>Enquanto todos só viam o retorno dele</tspan><tspan x='117' y='512'>ao Santos, ele já olhava algo maior.</tspan><tspan x='117' y='670'>Se engana quem pensa que ele só está</tspan><tspan x='117' y='750'>lançando uma marca que vende creatina...</tspan><tspan x='117' y='890'>O mercado Wellness movimenta trilhões</tspan><tspan x='117' y='970'>de dólares todos os anos e o Brasil é</tspan><tspan x='117' y='1050'>um dos maiores mercados da área.</tspan></text></svg><svg width='1080' height='1350' viewBox='0 0 1080 1350' fill='none' xmlns='http://www.w3.org/2000/svg'><rect width='1080' height='1350' fill='white'/><defs><clipPath id='circleClip'><circle cx='165' cy='242' r='64'/></clipPath></defs><g clip-path='url(#circleClip)'><image xlink:href='https://assets.goal.com/images/v3/blt47f09058442f3c14/neymar-close.jpg' x='101' y='178' width='128' height='128' preserveAspectRatio='xMidYMid slice'/></g><text fill='black' font-family='Inter' font-size='32' font-weight='bold'><tspan x='237' y='227'>Pedro Del Valle</tspan></text><text fill='#8E8E8E' font-family='Inter' font-size='32'><tspan x='237' y='272'>@pedrodelvalle</tspan></text><text fill='black' font-family='Inter' font-size='50'><tspan x='117' y='437'>Mas isso aqui NÃO é sobre o Neymar.</tspan><tspan x='117' y='512'>É sobre como se constrói um negócio.</tspan><tspan x='117' y='670'>1) Construa um público antes de ter</tspan><tspan x='117' y='750'>lançado o produto.</tspan><tspan x='117' y='890'>2) Lance no timing certo.</tspan><tspan x='117' y='1020'>3) Venda um conceito antes de vender</tspan><tspan x='117' y='1090'>um produto...</tspan></text></svg><svg width='1080' height='1350' viewBox='0 0 1080 1350' fill='none' xmlns='http://www.w3.org/2000/svg'><rect width='1080' height='1350' fill='white'/><defs><clipPath id='circleClip'><circle cx='165' cy='242' r='64'/></clipPath></defs><g clip-path='url(#circleClip)'><image xlink:href='https://assets.goal.com/images/v3/blt47f09058442f3c14/neymar-close.jpg' x='101' y='178' width='128' height='128' preserveAspectRatio='xMidYMid slice'/></g><text fill='black' font-family='Inter' font-size='32' font-weight='bold'><tspan x='237' y='227'>Pedro Del Valle</tspan></text><text fill='#8E8E8E' font-family='Inter' font-size='32'><tspan x='237' y='272'>@pedrodelvalle</tspan></text><text fill='black' font-family='Inter' font-size='50'><tspan x='117' y='437'>Agora me diz...</tspan><tspan x='117' y='512'>Isso é só um hype passageiro?</tspan><tspan x='117' y='670'>Ou você realmente concorda que o</tspan><tspan x='117' y='750'>Neymar está construindo o seu maior</tspan><tspan x='117' y='830'>império já feito?</tspan><tspan x='117' y='1020'>Comente abaixo 👇</tspan></text></svg>"""
    output_folder = "output_svgs"
    convert_svg_images_to_base64_and_save(svg_code, output_folder)
