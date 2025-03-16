import os
from flask import Flask, request, jsonify, send_file
from dotenv import load_dotenv
from converter import convert_svg_images_to_base64_and_save
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Carregar variáveis do .env
load_dotenv()

app = Flask(__name__)

# Pegando a chave de API do ambiente
API_KEY = os.getenv("API_KEY")

limiter = Limiter(get_remote_address, app=app, default_limits=["15 per minute"])

@app.route('/convert-svg', methods=['POST'])
@limiter.limit("5 per minute")  # Máximo de 5 requisições por minuto por IP
def convert_svg():
    """Protegendo a API com autenticação via API_KEY"""
    request_api_key = request.headers.get("X-API-KEY")
    if request_api_key != API_KEY:
        return jsonify({"error": "Chave de API inválida"}), 403  # HTTP 403 Forbidden

    data = request.json
    svg_content = data.get('svg_content')
    output_folder = data.get('output_folder', 'output_svgs')

    if not svg_content:
        return jsonify({'error': 'O conteúdo do SVG é obrigatório!'}), 400

    try:
        converted_files = convert_svg_images_to_base64_and_save(svg_content, output_folder)
        if not converted_files:
            return jsonify({'error': 'Nenhum arquivo foi gerado!'}), 500

        file_links = []
        for file in converted_files:
            file_links.append({
                "svg_download": f"/download/{os.path.basename(file['svg'])}",
                "png_download": f"/download/{os.path.basename(file['png'])}"
            })

        return jsonify({
            'message': 'SVGs convertidos com sucesso!',
            'files': file_links
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

