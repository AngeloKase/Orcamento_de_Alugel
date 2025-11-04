import csv
import os
import platform
import subprocess

while True:
    apartamento = 700
    casa = 900
    estudio = 1200
    quarto_casa = 250
    quarto_apartamento = 200 
    vaga = 300
    estudio_vaga = 250
    vaga_extra = 60
    contrato = 2000
    desconto = 5
    parcelas_valor = 0
    total = 0

    print("----------------------------------------------------------")
    print("Seja Bem-Vindo à Nossa Locadora de Imóveis!")
    print("Aqui você pode ver o orçamento mensal de um imóvel personalizado com as suas preferências.")
    nome_cliente = input("Primeiro digite seu nome: ")
    encerrar = int(input('Escolha a opção desejada: 1 - Iniciar | 2 - Encerrar: '))

    if encerrar == 2:
        print("Encerrando o serviço... Obrigado por utilizar nossa locadora!")
        break
    else:
        print("Valores: Casa = 900 | Apartamento = 700 | Estúdio = 1200")    
        imovel = int(input("Escolha um imóvel: 1 - Casa | 2 - Apartamento | 3 - Estúdio: "))

   
    if imovel == 1:
        tipo_imovel = "Casa"
        total += casa
        print("----------------------------------------------------------")
        print("A casa vem com apenas 1 quarto")
        print("O custo do quarto adicional é no valor de R$250 ")
        quarto = input("Deseja Adicionar um quarto a mais? (Sim/Não): ").strip().lower()

        if quarto in ["sim", "s"]:
            valor_booleano = True
            total += quarto_casa
            print("O custo até então esta no valor de", f"R$ {total:.2f}")
        else:
            print("Sem quarto adicioanl.")

        print("----------------------------------------------------------")
        print("A casa vem sem vaga para carros")
        print("O custo da vaga adicional sai no valor de R$300")
        casa_vaga = input("Deseja Adicionar uma vaga? (Sim/Não): ").strip().lower()

        if casa_vaga in ["sim", "s"]:
            valor_booleano2 = True
            total += vaga
            print("Vaga de garagem adicionada valor atualizado para", f"R$ {total:.2f}")
        else:
            print("Sem vaga de garagem adicionada.")

    elif imovel == 2:
        tipo_imovel = "Apartamento"
        total += apartamento
        print("----------------------------------------------------------")
        print("o apartamento vem com apenas 1 quarto")
        print("O custo do quarto adicional é no valor de R$200 ")
        quarto = input("Deseja Adicionar um quarto a mais? (Sim/Não): ").strip().lower()

        if quarto in ["sim", "s"]:
            valor_booleano = True
            total += quarto_apartamento
            print("O custo até então esta no valor de", f"R$ {total:.2f}")
        else:
            print("Sem quarto adicioanl.")

        print("----------------------------------------------------------")
        print("O apartamento vem sem vaga para carros")
        print("O custo da vaga adicional sai no valor de R$300")
        casa_vaga = input("Deseja Adicionar uma vaga? (Sim/Não): ").strip().lower()

        if casa_vaga in ["sim", "s"]:
            valor_booleano2 = True
            total += vaga
            print("Vaga de carro adicionada valor atualizado para", f"R$ {total:.2f}")
        else:
            print("Sem vaga de carro adicionada.")

        print("----------------------------------------------------------")
        print("No apartamento temos um desconto no alugel de 5% para moradores sem criança")
        casa_vaga = input("Você tem criança? (Sim/Não): ").strip().lower()

        if casa_vaga in ["não", "n", "nao"]:
            valor_booleano3 = False
            descontando = desconto * total / 100
            total -= descontando
            print("Desconto aplicado valor atualizado para", f"R$ {total:.2f}")
        else:
            print("Sem desconto aplicado.")

    elif imovel == 3:
        tipo_imovel = "Estúdio"
        total += estudio
        print("----------------------------------------------------------")
        print("O Estudio vem sem vaga para carros")
        print("Não é possivel comprar apenas uma vaga")
        print("O custo de duas vagas sai no valor de R$250")
        print("Ao adicionar mais de duas vagas, cada vaga extra custa R$60 cada.")

        estudio_vaga_input = input("Deseja Adicionar duas vaga? (Sim/Não): ").strip().lower()
        if estudio_vaga_input in ["sim", "s"]:
            valor_booleano2 = True
            total += estudio_vaga
            vaga_extra_input = int(input("Quantas vagas extra você deseja adiconar, caso não queira apenas digite 0: "))

            if vaga_extra_input >= 1:
                soma_da_vaga_extra = vaga_extra * vaga_extra_input
                total += soma_da_vaga_extra
            else:
                print("Sem vaga extra adicionada")
                print("Vaga de garagem adicionada valor atualizado para", f"R$ {total:.2f}")
        else:
            print("Sem vaga de garagem adicionada.")

    else:
        print("Resposta não identificada porfavor responda com números.")
        break


 
    print(f"\nValor do aluguel mensal: R$ {total:.2f}")
    print("Contrato: R$ 2000, parcelável em até 5x.")

    while True:
        try:
            parcelas = int(input("Deseja parcelar o contrato em quantas vezes (1 a 5)? "))
            if parcelas == 1:
                print("Pagamento à vista selecionado.")
                parcelas_valor = contrato
                break
            elif 2 <= parcelas <= 5:
                parcelas_valor = contrato / parcelas
                print(f"Contrato parcelado em {parcelas}x de R$ {parcelas_valor:.2f}.")
                break
            else:
                print("❌ Número de parcelas inválido. Tente novamente.")
        except ValueError:
            print("❌ Digite um número válido.")

    meses = []
    for mes in range(1, 13):
        if mes <= parcelas:
            total_mes = total + parcelas_valor
            parcela_mes = f"R$ {parcelas_valor:.2f}"
        else:
            total_mes = total
            parcela_mes = "R$ 0.00"
        meses.append([mes, f"R$ {total:.2f}", parcela_mes, f"R$ {total_mes:.2f}"])

    total_anual = sum(float(linha[3].replace("R$ ", "")) for linha in meses)

    nome_arquivo = f"orcamento_{nome_cliente.replace(' ', '_').lower()}.csv"
    with open(nome_arquivo, mode="w", newline="", encoding="utf-8-sig") as file:
        escritor = csv.writer(file, delimiter=';')
        escritor.writerow(["Cliente:", nome_cliente])
        escritor.writerow(["Tipo de imóvel:", tipo_imovel])
        escritor.writerow([])
        escritor.writerow(["Mês", "Aluguel Base", "Parcela do Contrato", "Total do Mês"])
        escritor.writerows(meses)
        escritor.writerow([])
        escritor.writerow(["", "", "Total Anual:", f"R$ {total_anual:.2f}"])

    print(f"\n✅ Arquivo '{nome_arquivo}' gerado com sucesso!")

  
    print("Abrindo no Excel...")
    sistema = platform.system()
    caminho_arquivo = os.path.abspath(nome_arquivo)

    try:
        if sistema == "Windows":
            os.startfile(caminho_arquivo)
        elif sistema == "Darwin":
            subprocess.call(["open", caminho_arquivo])
        else:
            subprocess.call(["xdg-open", caminho_arquivo])
    except Exception as e:
        print("⚠️ Não foi possível abrir o arquivo automaticamente:", e)

    print("----------------------------------------------------------\n")
    break
