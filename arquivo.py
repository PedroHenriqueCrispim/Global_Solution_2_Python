import json
import requests


""" Funcao para fazer login do usuario e paciente """
def fazer_login(tipo_usuario, usuarios, pacientes):
    print(f'Fazer login como {tipo_usuario}')

    while True:
        nome_usuario = input('Digite o nome de usuário: ')
        senha = input('Digite a senha: ')

        if tipo_usuario == 'medico':
            for usuario in usuarios:
                if 'tipo' in usuario and usuario['tipo'] == tipo_usuario and usuario['nome'] == nome_usuario and usuario['senha'] == senha:
                    print('Login bem-sucedido!')
                    return usuario['id'], tipo_usuario
        elif tipo_usuario == 'paciente':
            logins_pacientes = carregar_logins('pacientes')
            for login_paciente in logins_pacientes:
                if login_paciente['nome'] == nome_usuario and login_paciente['senha'] == senha:
                    print('Login bem-sucedido como paciente!')
                    return login_paciente['id'], 'paciente'
                print('Nome de usuário ou senha incorretos. Tente novamente.')

        opcao = input('Deseja tentar novamente? (s/n): ').lower()
        if opcao != 's':
            return None, None
        
""" Funcao para carregar o Login dos pacientes"""
def carregar_logins():
    arquivo = f'logins_pacientes.json'
    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            dados = json.load(file)
            return dados if isinstance(dados, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

""" Funcao para salvar login do pacientes """
def salvar_logins_pacientes(logins_pacientes):
    try:
        with open('logins_pacientes.json', 'w', encoding='utf-8') as file:
            json.dump(logins_pacientes, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar os logins de pacientes: {e}")

""" Funcao para cadastrar pacientes """
def cadastrar_paciente(pacientes, logins_pacientes):
    novo_paciente = input('Digite o nome do paciente: ')
    novo_email = input('Digite o email do paciente: ')
    nova_senha = input('Digite a senha: ')

    id_paciente = str(obter_proximo_id(pacientes))

    pacientes.append({
        'id': id_paciente,
        'nome': novo_paciente,
        'email': novo_email,
        'senha': nova_senha,
        'tipo': 'Paciente',
    })

    salvar_pacientes(pacientes)

    logins_pacientes.append({
        'id': id_paciente,
        'nome': novo_paciente,
        'email': novo_email,
        'senha': nova_senha,
        'tipo': 'Paciente',
    })

    salvar_logins_pacientes(logins_pacientes)

    print(f'Paciente cadastrado com sucesso. Seu ID é {id_paciente}. Faça login para continuar.')

    return id_paciente

""" Funcao para cadastrar medico """
def cadastrar_medico(usuarios):
    novo_medico = input('Digite o nome do médico: ')
    nova_senha = input('Digite a senha: ')

    id_medico = str(len(usuarios) + 1)

    while any(medico['id'] == id_medico for medico in usuarios):
        id_medico = str(int(id_medico) + 1)

    usuarios.append({
        'id': id_medico,
        'nome': novo_medico,
        'senha': nova_senha,
        'tipo': 'medico', 
    })

    salvar_usuarios(usuarios)

    print(f'Médico cadastrado com sucesso. Seu ID é {id_medico}. Faça login para continuar.')

    return id_medico

""" Funcao login """
def login():
    while True:
        print('Sistema de Cadastro de Pacientes')
        print('1 - Fazer login como Médico')
        print('2 - Fazer login como Paciente')
        print('0 - Sair')
        opcao = input('Digite o número da opção: ')

        if opcao == '1':
            id_medico, tipo_usuario = fazer_login('medico')
            return id_medico, tipo_usuario
        elif opcao == '2':
            id_paciente, tipo_usuario = fazer_login('paciente')
            return id_paciente, tipo_usuario
        elif opcao == '0':
            print('Programa encerrado.')
            return None, None
        else:
            print('Opção inválida. Tente novamente.')

""" Funcao fazer login medico """
def login_medico(usuarios):
    print('Login Médico')

    while True:
        opcao = input('Escolha uma opção:\n1 - Fazer login\n2 - Cadastrar novo médico\n0 - Sair\nOpção: ')

        if opcao == '1':
            id_medico, tipo_usuario = fazer_login('medico', usuarios, pacientes)

            if id_medico:
                print(f'Login como médico bem-sucedido. Seu ID é {id_medico}.')
                funcionalidades_medico(pacientes)
                return id_medico, tipo_usuario
            else:
                print('Login falhou. Verifique as credenciais e tente novamente.')
        elif opcao == '2':
            id_medico = cadastrar_medico(usuarios)
            return id_medico, 'medico' 
        elif opcao == '0':
            print('Programa encerrado.')
            return None, None
        else:
            print('Opção inválida. Tente novamente.')

""" Funcao para login paciente """
def login_paciente(pacientes, logins_pacientes):
    print('Login Paciente')
    
    while True:
        opcao = input('Escolha uma opção:\n1 - Fazer login\n2 - Cadastrar novo paciente\n0 - Sair\nOpção: ')

        if opcao == '1':
            id_paciente, tipo_usuario = fazer_login('paciente', usuarios, pacientes)

            if id_paciente:
                print(f'Login como paciente bem-sucedido. Seu ID é {id_paciente}.')
                funcionalidades_paciente(pacientes)
                return id_paciente, tipo_usuario
            else:
                print('Login falhou. Verifique as credenciais e tente novamente.')
        elif opcao == '2':
            id_paciente = cadastrar_paciente(usuarios, logins_pacientes)
            return id_paciente, 'paciente'
        elif opcao == '0':
            print('Programa encerrado.')
            return None, None
        else:
            print('Opção inválida. Tente novamente.')

""" Funcao carregar usuarios do arquivo json"""
def carregar_usuarios():
    try:
        with open('loginusuarios.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)

            if not dados or not isinstance(dados, list):
                print("Formato inválido do arquivo JSON. Esperado uma lista de usuários.")
                return []

            for usuario in dados:
                if not isinstance(usuario, dict) or 'id' not in usuario:
                    print("Formato inválido dos dados do usuário. Cada usuário deve ser um dicionário com um campo 'id'.")
                    return []

                usuario['id'] = int(usuario['id'])

            return dados
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
""" Função para carregar os dados de pacientes do arquivo JSON """
def carregar_pacientes():
    try:
        with open('pacientes.json', 'r', encoding='utf-8') as file:
            dados = json.load(file)

            if not dados or not isinstance(dados, list):
                return []

            for paciente in dados:
                if not isinstance(paciente, dict) or 'id' not in paciente:
                    print("Formato inválido dos dados do paciente. Cada paciente deve ser um dicionário com um campo 'id'.")
                    return []

                paciente['id'] = int(paciente['id'])

            return dados
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
""" Funcao para salvar usuarios """
def salvar_usuarios(usuarios, nome_arquivo='loginusuarios.json'):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

""" Função para salvar os dados dos pacientes no arquivo JSON """
def salvar_pacientes(pacientes, nome_arquivo='pacientes.json'):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            json.dump(pacientes, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")
        
""" Função para buscar o CEP na API ViaCEP """
def buscar_cep(cep):
    while True:
        try:
            url = f"https://viacep.com.br/ws/{cep}/json/"
            resposta = requests.get(url)
            if resposta.status_code == 200:
                dicionario = resposta.json()
                if 'erro' in dicionario:
                    print("Erro: CEP não existe. ")
                    novo_cep = input("Digite o CEP novamente: ")
                    if novo_cep.isdigit() and len(novo_cep) == 8:
                        cep = novo_cep
                    else:
                        print("CEP invalido. Tente novamente. ")
                else:
                    return dicionario
            else:
                print(f"Erro: Status code {resposta.status_code}")
                novo_cep = input("Digite o CEP novamente: ")
                if novo_cep.isdigit() and len(novo_cep) == 8:  #verifica se tem 8 dígitos no CEP
                    cep = novo_cep
                else:
                    print("CEP inválido. Tente novamente. ")
        except requests.exceptions.ConnectTimeout:
            print('Erro ao carregar API, aguarde..')
            continue

""" Função para obter o id """
def obter_proximo_id(pacientes):
    if not pacientes:
        return 1
    return max(int(paciente['id']) for paciente in pacientes) + 1
    
""" Função para validar o id """
def validar_id(id_str):
    try:
        id_paciente = int(id_str)
        if id_paciente > 0:
            return id_paciente
        else:
            print('ID deve ser um número inteiro positivo.')
    except ValueError:
        print('ID deve ser um número inteiro positivo.')

""" Funcao para ver o nivel do paciente """
def gravidade_cor(nivel):
    cores = {
        "1": ("Não Urgente", "Azul"),
        "2": ("Pouco Urgente", "Verde"),
        "3": ("Urgente", "Amarelo"),
        "4": ("Muito Urgente", "Laranja"),
        "5": ("Emergencial", "Vermelho"),
        "default": ("Acompanhante", "Cinza")
    }
    return cores.get(nivel, cores["default"])

""" Funcao exiber info de cep """
def exibir_informacoes_cep(info_cep):
    print("\nConfirme as informações do CEP:")
    print(f"CEP: {info_cep['cep']}")
    print(f"Logradouro: {info_cep['logradouro']}")
    print(f"Complemento: {info_cep['complemento']}")
    print(f"Bairro: {info_cep['bairro']}")
    print(f"Localidade: {info_cep['localidade']}")
    print(f"UF: {info_cep['uf']}")

""" Funcao exibir opcao status"""
def exibir_opcoes_status():
    numero_para_status = {
        "1": "Não Atendido",
        "2": "Triagem",
        "3": "Ordem de atendimento",
        "4": "Exame",
        "5": "Pronto de socorro",
        "6": "Pronto de atendimento",
        "7": "Alta"
    }
        # Exibir opções de status
    print("\nOpções de Status:")
    for numero, status in numero_para_status.items():
        print(f"{numero} - {status}")

""" Função para adicionar um novo pacientes """
def inserir_pacientes(pacientes):
    while True:
        id_paciente = obter_proximo_id(pacientes)

        nome = input("Digite o nome completo do paciente: ")
        if not nome.replace(" ", "").isalpha():
            print("O nome deve conter apenas letras. Tente novamente.")
            continue

        idade = input("Digite a idade do paciente: ")
        try:
            idade = int(idade)
        except ValueError:
            print("A idade deve ser um número inteiro. Tente novamente.")
            continue

        documento = input("Digite o número do CPF de identificação do paciente: ")
        if len(documento) != 11 or not documento.isdigit():
            print("O número do CPF de identificação deve conter 11 dígitos numéricos. Tente novamente.")
            continue


        cep = input('Digite o CEP do pacientes: ')
        endereco = buscar_cep(cep)
        print("\nConfirme as informações do CEP:")
        print(f"CEP: {endereco['cep']}")
        print(f"Logradouro: {endereco['logradouro']}")
        print(f"Complemento: {endereco['complemento']}")
        print(f"Bairro: {endereco['bairro']}")
        print(f"Localidade: {endereco['localidade']}")
        print(f"UF: {endereco['uf']}")
        
        confirmar_cep = input("As informações do CEP estão corretas? (s/n): ").lower()
        if confirmar_cep != 's':
            print("Cadastro cancelado.")
            return

        if not endereco:
            print('CEP não encontrado. Verifique o CEP e tente novamente.')
            return

        rua = endereco.get('logradouro', '')
        bairro = endereco.get('bairro', '')
        municipio = endereco.get('localidade', '')
        uf = endereco.get('uf', '')
        complemento = endereco.get('complemento','')

        numero_para_status = {
            "1": "Não Atendido",
            "2": "Triagem",
            "3": "Ordem de atendimento",
            "4": "Exame",
            "5": "Pronto de socorro",
            "6": "Pronto de atendimento",
            "7": "Alta"
        }

        # Exibir opções de status
        print("\nOpções de Status:")
        for numero, status in numero_para_status.items():
            print(f"{numero} - {status}")

        opcao_status = input("Digite o número correspondente ao status do paciente: ")
        opcao_nivel = "Não Especificado"

        # Exibir opções de nível para status específicos
        if opcao_status:
            print("\nOpções de Nível:")
            print("1 - Não Urgente")
            print("2 - Pouco Urgente")
            print("3 - Urgente")
            print("4 - Muito Urgente")
            print("5 - Emergencial")

        opcao_nivel = input("Digite o número correspondente ao nível do paciente: ")

        gravidade, cor_pulseira = gravidade_cor(opcao_nivel)

        observacao = input("Digite uma observação para o paciente: ")

        paciente = {
            'id': id_paciente,
            'nome': nome,
            'idade': idade,
            'CPF': documento,
            'endereco': {
                'rua': rua,
                'numero': numero,
                'complemento': complemento,
                'bairro': bairro,
                'municipio': municipio,
                'uf': uf,
                'cep': cep
            },
            'Status': numero_para_status[opcao_status],
            'Nivel': opcao_nivel,
            'Observacao': observacao,
            'Gravidade': gravidade,
            'Cor_Pulseira': cor_pulseira,
        }

        pacientes.append(paciente)
        salvar_pacientes(pacientes)  # Corrigindo para passar a lista completa

        print('Pacientes cadastrado com sucesso. ID:', id_paciente)
        return
        
""" Função para excluir um pacientes """
def excluir_pacientes(pacientes, id_paciente):
    id_paciente = int(id_paciente)
    for paciente in pacientes:
        if paciente['id'] == id_paciente:
            pacientes.remove(paciente)
            salvar_pacientes(pacientes)
            print(f'Pacientes com ID {id_paciente} excluído com sucesso.')
            return
    print(f'Pacientes com ID {id_paciente} não encontrado.')

""" Função para alterar os dados de um pacientes """
def alterar_pacientes(pacientes, id_paciente):
    id_paciente = int(id_paciente)

    numero_para_status = {
        "1": "Não Atendido",
        "2": "Triagem",
        "3": "Ordem de atendimento",
        "4": "Exame",
        "5": "Pronto de socorro",
        "6": "Pronto de atendimento",
        "7": "Alta"
    }


    for paciente in pacientes:
        if paciente['id'] == id_paciente:
            print('O que deseja alterar?')
            print('1 - Nome')
            print('2 - Idade')
            print('3 - CPF')
            print('4 - CEP')
            print('5 - Status')
            print('6 - Nivel')
            print('7 - Obervacao')
            print('8 - Gravidade')
            opcao = input('Digite o número da opção: ')
            
            if opcao == '1':
                novo_nome = input('Digite o novo nome: ')
                paciente['nome'] = novo_nome

            elif opcao == '2':
                novo_idade = int(input('Digite o nova idade: '))
                paciente['idade'] = novo_idade

            elif opcao == '3':
                nova_cpf = input('Digite o novo CPF (tem que ter 11 caracteres): ')
                while len(nova_cpf) < 11:
                    nova_cpf = input('O CPF deve ter 11 caracteres. Digite a senha novamente: ')
                    paciente['senha'] = nova_cpf

            elif opcao == '4':
                novo_cep = input('Digite o novo CEP: ')
                endereco = buscar_cep(novo_cep)
                if not endereco:
                    print('CEP não encontrado. Verifique o CEP e tente novamente.')
                    return
                paciente['endereco']['cep'] = novo_cep
                paciente['endereco']['rua'] = endereco.get('logradouro', '')
                paciente['endereco']['bairro'] = endereco.get('bairro', '')
                paciente['endereco']['municipio'] = endereco.get('localidade', '')
                paciente['endereco']['uf'] = endereco.get('uf', '')
                paciente['endereco']['numero'] = endereco.get('Digite o novo número: ')
                paciente['endereco']['complemento'] = endereco.get('Digite o novo complemento: ')

            elif opcao == '5':
                exibir_opcoes_status()  
                novo_status = input('Digite o novo status (número correspondente): ')
                if novo_status in numero_para_status:
                    paciente['Status'] = numero_para_status[novo_status]
                else:
                    print('Opção de status inválida.')

            elif opcao == '6':

                print("\nOpções de Nível:")
                print("1 - Não Urgente")
                print("2 - Pouco Urgente")
                print("3 - Urgente")
                print("4 - Muito Urgente")
                print("5 - Emergencial")

                novo_nivel = input('Digite o novo nível (número correspondente): ')
                paciente['Nivel'] = novo_nivel

            elif opcao == '7':
                nova_observacao = input('Digite a nova observação: ')
                paciente['Observacao'] = nova_observacao

            elif opcao == '8':
                print("\nOpções de Gravidade:")
                print("1 - Não Urgente")
                print("2 - Pouco Urgente")
                print("3 - Urgente")
                print("4 - Muito Urgente")
                print("5 - Emergencial")

                nova_gravidade = input('Digite a nova gravidade (número correspondente): ')
                paciente['Gravidade'] = nova_gravidade
        else:
            print('Opção inválida.')
            return

        salvar_pacientes(pacientes)
        print('Dados do pacientes alterados com sucesso.')
        return
    print(f'Pacientes com ID {id_paciente} não encontrado.')

""" Função para listar todos os pacientes """
def listar_pacientes(pacientes):
    if not pacientes:
        print('Nenhum pacientes cadastrado.')
    else:
        print('ID - Nome')
        for paciente in pacientes:
            print(f'{paciente["id"]} - {paciente["nome"]}')
    print()

""" Função consultar os pacientes"""
def consultar_pacientes(pacientes):
    listar_pacientes(pacientes)
    id_consultar = input('Digite o ID do pacientes que deseja consultar ou pressione Enter para sair: ')

    if id_consultar:
        id_consultar = int(id_consultar)
        for paciente in pacientes:
            if paciente['id'] == id_consultar:
                print('\nInformações do pacientes:')
                print(f'ID: {paciente["id"]}')
                print(f'Nome: {paciente["nome"]}')
                print(f'Idade: {paciente["idade"]}')
                print(f'Status: {paciente["Status"]}')
                print(f'Nível: {paciente["Nivel"]}')
                print(f'Observação: {paciente["Observacao"]}')
                print(f'Gravidade: {paciente["Gravidade"]}')
                print(f'Cor da Pulseira: {paciente["Cor_Pulseira"]}')
                print('Endereço:')
                endereco = paciente['endereco']
                print(f'Rua: {endereco["rua"]}')
                print(f'Número: {endereco["numero"]}')
                print(f'Complemento: {endereco["complemento"]}')
                print(f'Bairro: {endereco["bairro"]}')
                print(f'Município: {endereco["municipio"]}')
                print(f'UF: {endereco["uf"]}')
                print(f'CEP: {endereco["cep"]}')
                break
        else:
            print(f'Pacientes com ID {id_consultar} não encontrado.')
    print()

""" Funcao para ver se o login ja existe """
def login_existente(usuarios, pacientes):
    id_existente = input("Digite o seu ID: ")
    senha_existente = input("Digite a sua senha: ")

    for usuario in usuarios:
        if 'tipo' in usuario and usuario['id'] == id_existente and usuario['senha'] == senha_existente:
            return usuario['id'], 'existente' 
    
    for paciente in pacientes:
        if paciente['id'] == id_existente:
            return paciente['id'], 'paciente' 

    print('Login existente falhou. Verifique as credenciais e tente novamente.')
    return None, None

""" Funcao para salvar o ususarios """
def salvar_usuarios(usuarios, nome_arquivo='loginusuarios.json'):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

""" Função para o medico """
def funcionalidades_medico(pacientes):
    while True:
        print('Sistema de Cadastro de Pacientes')
        print('1 - Inserir pacientes')
        print('2 - Excluir pacientes')
        print('3 - Alterar pacientes')
        print('4 - Consultar pacientes')
        print('0 - Sair')
        opcao = input('Digite o número da opção: ')

        if opcao == '1':
            inserir_pacientes(pacientes)
        elif opcao == '2':
            listar_pacientes(pacientes)
            id_paciente = int(input('Digite o ID do paciente a ser excluído: '))
            excluir_pacientes(pacientes, id_paciente)
        elif opcao == '3':
            listar_pacientes(pacientes)
            id_paciente = int(input('Digite o ID do paciente a ser alterado: '))
            alterar_pacientes(pacientes, id_paciente)
        elif opcao == '4':
            consultar_pacientes(pacientes)
        elif opcao == '0':
            print('Programa encerrado.')
            salvar_pacientes(pacientes)
            break
        else:
            print('Opção inválida. Tente novamente.')

""" Funcao para o paceinte """
def funcionalidades_paciente(pacientes):
    while True:
        print('Sistema de Cadastro de Pacientes')
        print('1 - Consultar pacientes')
        print('0 - Sair')
        opcao = input('Digite o número da opção: ')

        if opcao == '1':
            consultar_pacientes(pacientes)
        elif opcao == '0':
            print('Programa encerrado.')
            salvar_pacientes(pacientes)
            break
        else:
            print('Opção inválida. Tente novamente.')

""" Funcao principal do codigo """
if __name__ == "__main__":
    pacientes = carregar_pacientes()
    usuarios = carregar_usuarios()
    logins_pacientes = carregar_logins()

    while True:
        print('Escolha uma opção:')
        print('1 - Fazer login como Médico')
        print('2 - Fazer login como Paciente')
        print('0 - Sair')

        opcao = input('Digite o número da opção desejada: ')

        if opcao == '1':
            id_medico, tipo_usuario = login_medico(usuarios)
            if id_medico:
                print(f'Login como médico bem-sucedido. Seu ID é {id_medico}.')
                funcionalidades_medico(pacientes)
            else:
                print('Login falhou. Verifique as credenciais e tente novamente.')

        elif opcao == '2':
            id_paciente, tipo_usuario = login_paciente(pacientes, logins_pacientes)
            if id_paciente:
                print(f'Login como paciente bem-sucedido. Seu ID é {id_paciente}.')
                funcionalidades_paciente(pacientes)
            else:
                print('Login falhou. Verifique as credenciais e tente novamente.')

        elif opcao == '0':
            print('Programa encerrado.')
            salvar_pacientes(pacientes)
            salvar_usuarios(usuarios)
            salvar_logins_pacientes(logins_pacientes)
            break

        else:
            print('Opção inválida. Tente novamente.')