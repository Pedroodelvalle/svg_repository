import base64
import re
import requests
import os
import mimetypes
import cairosvg
from io import BytesIO
from typing import List, Dict


def convert_svg_images_to_base64_and_save(svg_content: str, output_folder: str) -> List[Dict[str, str]]:
    """
    Converte SVG com imagens externas para versão com Base64 e gera PNG de alta fidelidade.
    
    Melhorias principais:
    - Priorização correta das dimensões do SVG
    - Controle preciso de resolução e escala
    - Qualidade de renderização otimizada
    """
    os.makedirs(output_folder, exist_ok=True)
    
    svg_elements = re.findall(r'(<svg[\s\S]*?</svg>)', svg_content)
    if not svg_elements:
        print("Nenhum elemento SVG encontrado.")
        return []

    processed_files = []
    
    for idx, svg in enumerate(svg_elements):
        processed_svg = _process_svg_images(svg)
        processed_svg = _ensure_xlink_namespace(processed_svg)
        
        svg_path, png_path = _save_svg_and_convert(processed_svg, output_folder, idx + 1)
        processed_files.append({"svg": svg_path, "png": png_path})
    
    return processed_files


def _process_svg_images(svg: str) -> str:
    """Substitui imagens externas por versões em Base64 com tratamento otimizado"""
    pattern = r'(<image\b[\s\S]*?(?:xlink:href|href)\s*=\s*["\'])(https?://[^"\']+)(["\'])'
    
    def replace_with_base64(match: re.Match) -> str:
        prefix, url, suffix = match.groups()
        print(f"Processando imagem: {url}")
        
        try:
            response = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15
            )
            response.raise_for_status()
        except Exception as e:
            print(f"Erro ao baixar {url}: {str(e)}")
            return match.group(0)
            
        mime_type = _get_mime_type(response, url)
        base64_data = base64.b64encode(response.content).decode("utf-8")
        return f'{prefix}data:{mime_type};base64,{base64_data}{suffix}'
    
    return re.sub(pattern, replace_with_base64, svg, flags=re.IGNORECASE)


def _get_mime_type(response: requests.Response, url: str) -> str:
    """Determinação mais precisa do tipo MIME"""
    mime_type = response.headers.get("Content-Type", "")
    if not mime_type:
        mime_type, _ = mimetypes.guess_type(url.split("?")[0])
    return (mime_type or "image/png").split(';')[0]


def _ensure_xlink_namespace(svg: str) -> str:
    """Garantia de namespaces necessários para renderização correta"""
    namespaces = {
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'xmlns': 'http://www.w3.org/2000/svg'
    }
    
    for ns, value in namespaces.items():
        if ns not in svg:
            svg = re.sub(r'<svg\b', f'<svg {ns}="{value}"', svg, count=1)
    
    return svg


def _save_svg_and_convert(processed_svg: str, output_folder: str, index: int) -> tuple:
    """Conversão para PNG com parâmetros otimizados de qualidade"""
    svg_filename = f"converted_{index}.svg"
    svg_path = os.path.join(output_folder, svg_filename)
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(processed_svg)
    
    png_filename = f"converted_{index}.png"
    png_path = os.path.join(output_folder, png_filename)
    
    # Extração precisa das dimensões
    width, height = _extract_svg_dimensions(processed_svg)
    
    # Parâmetros otimizados para renderização
    convert_args = {
        "file_obj": BytesIO(processed_svg.encode()),
        "write_to": png_path,
        "output_width": width,
        "output_height": height,
        "scale": 2.0  # Renderização em resolução dobrada para suavização
    }
    
    # Controle de qualidade do CairoSVG
    cairosvg.svg2png(**convert_args)
    
    print(f"Arquivos gerados:\n- SVG: {svg_path}\n- PNG (HiRes): {png_path}")
    return svg_path, png_path


def _extract_svg_dimensions(svg: str) -> tuple:
    """Extrai dimensões com prioridade para atributos explícitos"""
    # Primeiro tenta width/height explícitos
    width_match = re.search(r'width\s*=\s*["\']([\d.]+)(?:px)?["\']', svg, re.IGNORECASE)
    height_match = re.search(r'height\s*=\s*["\']([\d.]+)(?:px)?["\']', svg, re.IGNORECASE)
    
    if width_match and height_match:
        return int(float(width_match.group(1))), int(float(height_match.group(1)))
    
    # Fallback para viewBox
    viewbox_match = re.search(r'viewBox\s*=\s*["\']\s*[\d.]+\s+[\d.]+\s+([\d.]+)\s+([\d.]+)\s*["\']', svg)
    if viewbox_match:
        return int(float(viewbox_match.group(1))), int(float(viewbox_match.group(2)))
    
    # Último recurso: valores padrão seguros
    print("Dimensões não detectadas, usando fallback 1080x1350")
    return 1080, 1350



# EXEMPLO DE USO
if __name__ == "__main__":
    svg_code = """<svg width="1080" height="1350" viewBox="0 0 1080 1350" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">
    <!-- Definição de Estilos CSS -->
    <style>
        .overlay { fill: black; opacity: 0.2; }
        .text-box { fill: white; rx: 20px; }
        .highlight { fill: #FFF2CC; rx: 10px; }
        .main-text { 
            fill: #333;
            font-family: Times New Roman, sans-serif;
            font-size: 48px;
            font-weight: bold;
            text-anchor: middle;
        }
    </style>
    
    <!-- Imagem de fundo -->
    <image href="https://images.pexels.com/photos/1447418/pexels-photo-1447418.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2" 
        x="0" y="0" width="1080" height="1350" preserveAspectRatio="xMidYMid slice"/>
    
    <!-- Sobreposição escura -->
    <rect class="overlay" width="1080" height="1350"/>
    
    <!-- Grupo principal com sistema de coordenadas centralizado -->
    <g transform="translate(540, 280)">
        <!-- Caixa de texto principal centrada na origem do grupo -->
        <rect class="text-box" x="-410" y="-100" width="830" height="220"/>
        
        <!-- Primeira linha de texto - linha superior -->
        <text class="main-text" x="0" y="-10">
            O mercado cripto não é cassino,
        </text>
        
        <!-- Destaque amarelo para a segunda linha -->
        <rect class="highlight" x="-380" y="10" width="760" height="60"/>
        
        <!-- Segunda linha de texto -->
        <text class="main-text" x="0" y="50">
            a chave é estratégia e paciência.
        </text>
    </g>
</svg>"""

    output_folder = "output_svgs"
    convert_svg_images_to_base64_and_save(svg_code, output_folder)
