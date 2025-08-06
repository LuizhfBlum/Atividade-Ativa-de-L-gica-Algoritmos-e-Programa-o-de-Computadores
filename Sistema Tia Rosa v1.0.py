cardapio = {1: {"nome": "Café expresso", "preço": 2.50},2: {"nome": "Cappuccino", "preço": 5.00},3: {"nome": "Pão de queijo", "preço": 2.50},4: {"nome": "Biscoito de queijo", "preço": 2.50}}

clientes = {}
vendas = []

# Interface inicial > opção 1
def mostrar_cardapio():
    print("Cardápio")
    print("Promoção: Compre 6 unidades de um mesmo produto e o sexto pedido saí gratuitamente!")
    for cod, produto in cardapio.items():
        print(f"{cod}. {produto['nome']} - R${produto['preço']:.2f}")

# Interface inicial > opção 2
def fazer_pedido():
    mostrar_cardapio()
    cpf = input("CPF do cliente (deixe em branco se não é registrado): ").strip()
    if cpf and cpf not in clientes:
        print("Cliente não encontrado. Registro é necessário")
        return
    
    pedido = {"itens": [], "cliente": cpf if cpf else None, "desconto_aplicado": 0.0}
    
    while True:
        try:
            codigo = int(input("Código do item (digite 0 para finalizar): "))
            if codigo == 0:
                break
            if codigo not in cardapio:
                print("Código inválido!")
                continue
            
            quantidade = int(input("Quantidade: "))
            if quantidade <= 0:
                continue
            
            if cpf:
                qtd_paga, qtd_gratis = aplicar_desconto_fidelidade(cpf, codigo, quantidade)
                if qtd_gratis > 0:
                    print(f"Promoção: {qtd_gratis} {cardapio[codigo]['nome']}(s) grátis!")
            else:
                qtd_paga, qtd_gratis = quantidade, 0
            
            pedido["itens"].append({
                "codigo": codigo,
                "quantidade_paga": qtd_paga,
                "quantidade_gratis": qtd_gratis,
                "preço_unitario": cardapio[codigo]["preço"]
            })
        except ValueError:
            print("Digite um número válido")
    
    if pedido["itens"]:
        total = sum(item["quantidade_paga"] * item["preço_unitario"] for item in pedido["itens"])
        pedido["total"] = total
        vendas.append(pedido)
        print(f"Pedido finalizado! Total: R${total:.2f}")
        for item in pedido["itens"]:
            produto = cardapio[item["codigo"]]["nome"]
            print(f"- {produto}: {item['quantidade_paga'] + item['quantidade_gratis']}x (R${item['quantidade_paga'] * item['preço_unitario']:.2f})")

# Interface inicial > opção 3
def menu_cliente():
    while True:
        print("\nMenu Cliente")
        print("(1) Registrar cliente")
        print("(2) Ver compras e pontos")
        print("(3) Retornar para menu")
        
        opcao = input("Escolha: ")
        if opcao == "1":
            cpf = input("CPF (apenas números): ").strip()
            if not cpf.isdigit():
                print("CPF inválido! Use apenas números.")
                continue
            nome = input("Nome do cliente: ").strip()
            if not nome:
                print("Opção 'Nome' não pode ser vazia! Favor preencher.")
                continue
            clientes[cpf] = {"nome": nome, "compras": {1: 0, 2: 0, 3: 0, 4: 0}}
            print(f"Cliente {nome} registrado com sucesso!")
        elif opcao == "2":
            cpf = input("Digite o CPF: ").strip()
            if cpf in clientes:
                print(f"Cliente: {clientes[cpf]['nome']}")
                print("Itens comprados:")
                for cod, qtd in clientes[cpf]["compras"].items():
                    produto = cardapio[cod]["nome"]
                    print(f"- {produto}: {qtd}x | Próxima compra grátis em: {5 - (qtd % 5)}")
            else:
                print("Cliente não encontrado/registrado!")
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")

def aplicar_desconto_fidelidade(cpf, cod_produto, quantidade):
    """Retorna (quantidade_paga, quantidade_grátis)"""
    if cpf not in clientes:
        return quantidade, 0
    
    cliente = clientes[cpf]
    compras_anteriores = cliente["compras"][cod_produto]
    
    total_antes = compras_anteriores
    total_depois = total_antes + quantidade
    gratis = (total_depois // 6) - (total_antes // 6)
    
    cliente["compras"][cod_produto] = total_depois - gratis
    return quantidade - gratis, gratis

# Interface inicial > opção 4
def relatorio_vendas():
    if not vendas:
        print("Nenhuma venda registrada hoje!")
        return
    
    print("\nRelatório de vendas")
    total_geral = 0
    resumo = {}
    
    for pedido in vendas:
        for item in pedido["itens"]:
            produto = cardapio[item["codigo"]]["nome"]
            if produto not in resumo:
                resumo[produto] = {"quantidade": 0, "total": 0}
            resumo[produto]["quantidade"] += item["quantidade_paga"] + item["quantidade_gratis"]
            resumo[produto]["total"] += item["quantidade_paga"] * item["preço_unitario"]
            total_geral += item["quantidade_paga"] * item["preço_unitario"]
    
    for produto, dados in resumo.items():
        print(f"{produto}: {dados['quantidade']}x | R${dados['total']:.2f}")
    print(f"\nTotal geral: R${total_geral:.2f}")

# Interface inicial
print("Bem-vindo ao sistema Tia Rosa versão 1.0")
while True:
    print("\n- Interface inicial -")
    print("(1) Ver Cardápio")
    print("(2) Fazer Pedido")
    print("(3) Cliente")
    print("(4) Relatório de Vendas")
    print("(5) Sair")
    
    opcao = input("Escolha: ")
    if opcao == "1":
        mostrar_cardapio()
    elif opcao == "2":
        fazer_pedido()
    elif opcao == "3":
        menu_cliente()
    elif opcao == "4":
        relatorio_vendas()
    elif opcao == "5":
        print("Até logo!")
        break
    else:

        print("Opção inválida!")
