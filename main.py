import qrcode
from PIL import Image, ImageDraw, ImageFont
from pydantic import validate_call


@validate_call
def gerar_qrcode_com_texto(dados: str, texto: str, nome_arquivo: str):

    # CONSTANTENS
    tamanho_imagem = 20
    tamanho_borda = 20
    tamanho_fonte = 20
    cor_do_fundo = "white"
    cor_da_letra = "black"
    modo = "RGB"
    fonte = "Arial.ttf"
    extencao_do_arquivo = ".png"

    # Gerar o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(dados)
    qr.make(fit=True)

    # Criar uma nova imagem
    largura_total_imagem, altura_total_imagem = qr.modules_count * tamanho_imagem + tamanho_borda, qr.modules_count * tamanho_imagem + tamanho_borda  # Tamanho do QR Code com bordas
    img = Image.new(modo, (largura_total_imagem, altura_total_imagem), cor_do_fundo)

    # Desenhar o QR Code na imagem
    desenho = ImageDraw.Draw(img)
    qr_imagem = qr.make_image(fill_color=cor_da_letra, back_color=cor_do_fundo)
    img.paste(qr_imagem)

    # Adicionar o texto abaixo do QR Code
    fonte = ImageFont.truetype(fonte, tamanho_fonte)

    # ORIGINAL: largura_texto, altura_texto = desenho.textsize(texto, font=fonte), 5
    # AttributeError: 'ImageDraw' object has no attribute 'textsize'

    # ORIGINAL: posicao_texto: tuple = ((largura_total_imagem) // 2 - 20, altura_total_imagem - 50)
    posicao_horizontal_central: float = largura_total_imagem // 2
    posicao_texto: float = altura_total_imagem - tamanho_borda

    posicao_texto: tuple = (
        posicao_horizontal_central,
        posicao_texto)
    
    desenho.text(posicao_texto, texto, fill=cor_da_letra, font=fonte)

    # Salvar a imagem
    img.save(nome_arquivo + extencao_do_arquivo)

if __name__ == "__main__":
    dados: str = input("Digite os dados para gerar o QR Code: ")
    texto: str = input("Digite o texto para adicionar abaixo do QR Code: ")
    nome_arquivo: str = input("Digite o nome do arquivo de imagem: ")
    gerar_qrcode_com_texto(dados, texto, nome_arquivo)
    print(f"QR Code gerado com sucesso em {nome_arquivo}.png")