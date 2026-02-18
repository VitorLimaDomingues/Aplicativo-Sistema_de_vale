def formatar_moeda(valor):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
def converter_moeda_para_float(valor_str):
    """
    Converte valores como:
    1200
    1.200
    1.200,50
    1200,50
    1200.50
    para float corretamente.
    """

    valor_str = valor_str.strip()

    # Remove pontos de milhar
    valor_str = valor_str.replace(".", "")

    # Troca vírgula decimal por ponto
    valor_str = valor_str.replace(",", ".")

    return float(valor_str)
