import boto3
import uuid
import re
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
usuarios_table = dynamodb.Table('Usuarios')
filmes_table = dynamodb.Table('Filmes')
avaliacoes_table = dynamodb.Table('Avaliacoes')

def gerar_filme_id(titulo):
    return re.sub(r'[^a-zA-Z0-9]', '', titulo.lower())

def menu():
    print("1. Criar novo usuário")
    print("2. Criar novo filme")
    print("3. Avaliar filme")
    print("4. Ver perfil de usuário")
    print("5. Ver detalhes de um filme")
    print("6. Listar minhas avaliações")
    print("7. Atualizar nota de uma avaliação")
    print("8. Adicionar filme aos favoritos")
    print("9. Deletar avaliação")
    print("0. Sair")

def criar_usuario():
    nome = input("Digite o nome do usuário: ").strip()
    email = input("Digite o e-mail do usuário: ").strip().lower()
    if not nome or not email:
        print("Nome e e-mail são obrigatórios!")
        return
    user_id = str(uuid.uuid4())
    try:
        usuarios_table.put_item(
            Item={
                'user_id': user_id,
                'nome': nome,
                'email': email,
                'filmes_favoritos': []
            }
        )
        print(f"Usuário criado com sucesso! ID: {user_id[:8]}...")
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")

def criar_filme():
    titulo = input("Título do filme: ").strip()
    genero = input("Gênero: ").strip()
    try:
        ano = int(input("Ano de lançamento: "))
    except ValueError:
        print("Ano inválido!")
        return
    if not titulo or not genero:
        print("Título e gênero são obrigatórios!")
        return
    filme_id = gerar_filme_id(titulo)
    try:
        filmes_table.put_item(
            Item={
                'filme_id': filme_id,
                'titulo': titulo,
                'genero': genero,
                'ano': ano,
                'nota_media': Decimal("0.0"),
                'total_avaliacoes': 0
            }
        )
        print(f"Filme '{titulo}' criado com ID: {filme_id}")
    except Exception as e:
        print(f"Erro ao criar filme: {e}")

def avaliar_filme():
    user_id = input("Digite o user_id do usuário: ").strip()
    filme_id = input("Digite o filme_id: ").strip().lower()
    try:
        nota_str = (input("Sua nota (de 0 a 5): ")).strip()
        nota = Decimal(nota_str)
        if nota < 0 or nota > 5:
            print("Nota deve estar entre 0 e 5!")
            return
    except ValueError:
        print("Nota inválida!")
        return
    comentario = input("Comentário: ").strip()
    try:
        avaliacoes_table.put_item(
            Item={
                'user_id': user_id,
                'filme_id': filme_id,
                'nota': nota,
                'comentario': comentario
            }
        )
        print("Avaliação registrada com sucesso!")
    except Exception as e:
        print(f"Erro ao avaliar filme: {e}")

def ver_usuario():
    user_id = input("Digite o user_id: ").strip()
    try:
        usuario = usuarios_table.get_item(Key={'user_id': user_id}).get('Item')
        if usuario:
            print("\nPerfil do usuário:")
            print(f"Nome: {usuario['nome']}")
            print(f"E-mail: {usuario['email']}")
            favoritos = usuario.get('filmes_favoritos', [])
            print(f"Favoritos: {favoritos if favoritos else 'Nenhum'}")
        else:
            print("Usuário não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

def ver_filme():
    filme_id = input("Digite o filme_id: ").strip().lower()
    try:
        filme = filmes_table.get_item(Key={'filme_id': filme_id}).get('Item')
        if filme:
            print(f"\nFilme: {filme['titulo']}")
            print(f"Gênero: {filme['genero']}")
            print(f"Ano: {filme['ano']}")
            print(f"Nota média: {filme['nota_media']}")
            print(f"Avaliações: {filme['total_avaliacoes']}")
        else:
            print("Filme não encontrado.")
    except Exception as e:
        print(f"Erro: {e}")

def listar_avaliacoes():
    user_id = input("Digite o user_id: ").strip()
    try:
        avaliacoes = avaliacoes_table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
        ).get('Items', [])
        if avaliacoes:
            print(f"\nAvaliações de {user_id[:8]}...:")
            for aval in avaliacoes:
                print(f"{aval['filme_id']} - {aval['nota']} - '{aval.get('comentario', '')}'")
        else:
            print("Nenhuma avaliação encontrada.")
    except Exception as e:
        print(f"Erro: {e}")

def atualizar_nota():
    user_id = input("user_id: ").strip()
    filme_id = input("filme_id: ").strip().lower()
    try:
        nova_notastr = input("Nova nota (0 a 5): ")
        nova_nota = Decimal(nova_notastr)
        if nova_nota < 0 or nova_nota > 5:
            print("Nota inválida!")
            return
    except ValueError:
        print("Valor inválido!")
        return
    try:
        avaliacoes_table.update_item(
            Key={'user_id': user_id, 'filme_id': filme_id},
            UpdateExpression='SET nota = :n',
            ExpressionAttributeValues={':n': nova_nota}
        )
        print("Nota atualizada com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

def favoritar_filme():
    user_id = input("user_id: ").strip()
    filme_id = input("filme_id a favoritar: ").strip().lower()
    
    try:
        response = usuarios_table.get_item(Key={'user_id': user_id})
        usuario = response.get('Item')
        if not usuario:
            print("Usuário não encontrado.")
            return
        favoritos = usuario.get('filmes_favoritos', [])
        if filme_id not in favoritos:
            favoritos.append(filme_id)
        else:
            print("Filme já está nos favoritos.")
            return

        usuarios_table.put_item(
            Item={
                'user_id': user_id,
                'nome': usuario['nome'],
                'email': usuario['email'],
                'filmes_favoritos': favoritos
            }
        )
        print("Filme adicionado aos favoritos!")
        
    except Exception as e:
        print(f"Erro ao favoritar filme: {e}")

def deletar_avaliacao():
    user_id = input("user_id: ").strip()
    filme_id = input("filme_id da avaliação a deletar: ").strip().lower()
    confirm = input(f"Tem certeza que deseja deletar a avaliação de '{filme_id}'? (s/N): ").lower()
    if confirm != 's':
        print("Operação cancelada.")
        return
    try:
        avaliacoes_table.delete_item(Key={'user_id': user_id, 'filme_id': filme_id})
        print("Avaliação deletada.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == '1':
            criar_usuario()
        elif opcao == '2':
            criar_filme()
        elif opcao == '3':
            avaliar_filme()
        elif opcao == '4':
            ver_usuario()
        elif opcao == '5':
            ver_filme()
        elif opcao == '6':
            listar_avaliacoes()
        elif opcao == '7':
            atualizar_nota()
        elif opcao == '8':
            favoritar_filme()
        elif opcao == '9':
            deletar_avaliacao()
        elif opcao == '0':
            print("Desligando...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        input("\nPressione ENTER para continuar...")