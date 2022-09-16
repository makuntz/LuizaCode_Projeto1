from distutils.command.clean import clean
import enum
from re import X
from urllib import request
import fastapi 
from typing import List
from pydantic import BaseModel


app = fastapi.FastAPI()

OK = "OK"
FALHA = "FALHA"


# Classe representando os dados do endereço do cliente
class Endereco(BaseModel):
    id: int
    rua: str
    cep: str
    cidade: str
    estado: str
    


# Classe representando os dados do cliente
class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    senha: str
    


# Classe representando a lista de endereços de um cliente
class ListaDeEnderecosDoUsuario(BaseModel):
    usuario: Usuario
    enderecos: List[Endereco] = []


# Classe representando os dados do produto
class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float


# Classe representando o carrinho de compras de um cliente com uma lista de produtos
class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: List[Produto] = []
    preco_total: float
    quantidade_de_produtos: int

#alguns dados hard coded pra ajudar nos testes
db_usuarios = [
{"id": 1, "nome": "maira", "email": "mk@gmail.com", "senha": "123"}, {"id": 2, "nome": "leandro", "email": "lz@uol.com", "senha": "123"} ]
db_produtos = []
db_end = [{'id': 1, 'rua': 'Rua A', 'cep': '000000', 'cidade': 'Ribeirao Preto', 'estado': 'SP', 'id_usuario': 2},
{'id': 2, 'rua': 'Rua A', 'cep': '000000', 'cidade': 'Ribeirao Preto', 'estado': 'SP', 'id_usuario': 1},{'id': 3, 'rua': 'Rua A', 'cep': '000000', 'cidade': 'Ribeirao Preto', 'estado': 'SP', 'id_usuario': 2},
{'id': 4, 'rua': 'Rua A', 'cep': '000000', 'cidade': 'Ribeirao Preto', 'estado': 'SP', 'id_usuario': 1}]        # enderecos_dos_usuarios
db_carrinhos = []

#===========================================
# Persistencia / Repositorio
#===========================================

def persistencia_salvar_usuario(novo_usuario):
    # codigo_novo_usuario = len(db_usuarios) + 1
    # novo_usuario["id"] = codigo_novo_usuario
    db_usuarios.append(novo_usuario)
    return novo_usuario
    
def persistencia_pesquisar_usuario_pelo_id(id):
    id_procurado = None
    for item in db_usuarios:
        if item['id'] == id:
            id_procurado = item
            break
        return FALHA
    print(id_procurado)
    return id_procurado

def persistencia_pesquisar_usuario_pelo_nome(nome):
    nome_procurado = None
    for item in db_usuarios:
        if item['nome'] == nome:
            nome_procurado = item
            break
        return FALHA
    print(nome_procurado)
    return nome_procurado

def persistencia_deletar_usuario_pelo_id(id):
    for i in db_usuarios:
        if i['id'] == id:
            db_usuarios.remove(i)           
            print(db_usuarios)
            return OK
    return FALHA
                    
def persistencia_salvar_endereco(novo_endereco):
    # db_end.append(novo_endereco)
    return novo_endereco
            
            
def persistencia_vincular_end_ao_usuario(end_com_usuario):
    db_end.append(end_com_usuario)
    return end_com_usuario

##arrumar essa funcaos
def persistencia_deletar_endereco_pelo_id(id_usuario, id_endereco):
    for i in db_usuarios:
        if i['id'] == id_usuario:
            for x in db_end:
                if x['id'] == id_endereco:
                    db_end.remove(x)
                    print(db_end)
                    return OK
    return FALHA
        

def persistencia_buscar_enderecos_por_usuario(id_usuario):
    for i in db_end:
        if not i['id_usuario'] in db_end:
            return FALHA
        if i['id_usuario'] == id_usuario:
            print(i)
    return OK      


def persistencia_buscar_email_mesmo_dominio(dominio):
    for i in db_usuarios:
        if dominio in i['email']:
            print(i)
           
            
def persistencia_cadastrar_produto(produto):
    db_produtos.append(produto)
    return produto 

def persistencia_deletar_produto_pelo_id(id_produto):
    for i in db_produtos:
        if i['id'] == id_produto:
            db_produtos.remove(i)
            print(db_produtos)
            return OK
    return FALHA

#===========================================
# Regras / Casos de uso
#===========================================

def regras_cadastrar_usuario(novo_usuario):
    novo_usuario = persistencia_salvar_usuario(novo_usuario)
    return novo_usuario

def regras_pesquisar_usuario_pelo_id(id):
    return persistencia_pesquisar_usuario_pelo_id(id)
    
def regras_pesquisar_usuario_pelo_nome(nome):
    return persistencia_pesquisar_usuario_pelo_nome(nome)

def regras_deletar_usuario_pelo_id(id):
    return persistencia_deletar_usuario_pelo_id(id)

def regras_cadastrar_endereco(novo_endereco):
    novo_endereco = persistencia_salvar_endereco(novo_endereco)
    return novo_endereco

def regras_vincular_end_ao_usuario(end_com_usuario):
    return persistencia_vincular_end_ao_usuario(end_com_usuario)

def regras_deletar_endereco_pelo_id(id_usuario, id_endereco):
    return persistencia_deletar_endereco_pelo_id(id_usuario, id_endereco)

def regras_buscar_enderecos_por_usuario(id_usuario):
    return persistencia_buscar_enderecos_por_usuario(id_usuario)

def regras_buscar_email_mesmo_dominio(dominio):
    return persistencia_buscar_email_mesmo_dominio(dominio)

def regras_cadastrar_produto(produto):
    return persistencia_cadastrar_produto(produto)

def regras_deletar_produto_pelo_id(id_produto):
    return persistencia_deletar_produto_pelo_id(id_produto)

#===========================================
# API Rest / Controlador
#===========================================

###USUARIO
@app.post("/usuario/")
async def criar_usuário(novo_usuario: Usuario):
    
    ids = map(lambda x: x['id'], db_usuarios)
    if novo_usuario.id in ids:
        return FALHA
    
    if not '@' in novo_usuario.email:
        return FALHA 
    
    if len(novo_usuario.senha) < 3:
        return FALHA
    
    novo_usuario = regras_cadastrar_usuario(novo_usuario.dict())
    print(db_usuarios)
    return novo_usuario

#TODO verificar pq as duas rotas nao funcionam se as duas estiverem ativas, apenas a primeira funciona. Abaixo: (é necessario deixar uma rota comentada para que a outra funcione)
@app.get("/usuario/{nome}")
async def retornar_usuario_com_nome(nome: str):
    print('consulta pelo nome: ', nome)
    return regras_pesquisar_usuario_pelo_nome(nome)

@app.get("/usuario/{id}")
async def retornar_usuario(id: int):
    print('consulta pelo id: ', id)
    return regras_pesquisar_usuario_pelo_id(id)

#TODO lembrar de fazer deletar os enderecos vinculados a esse id
@app.delete("/usuario/{id}")
async def deletar_usuario(id: int):    
    print("deletando usuario: ", id)
    return regras_deletar_usuario_pelo_id(id)

#--------
# Se não existir usuário com o id_usuario retornar falha, 
# senão retornar uma lista de todos os endereços vinculados ao usuário
# caso o usuário não possua nenhum endereço vinculado a ele, retornar 
# uma lista vazia
### Estudar sobre Path Params (https://fastapi.tiangolo.com/tutorial/path-params/)
@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_enderecos_do_usuario(id_usuario: int):
    return regras_buscar_enderecos_por_usuario(id_usuario)


# Retornar todos os emails que possuem o mesmo domínio
# (domínio do email é tudo que vêm depois do @)
# senão retornar falha
@app.get("/emails/{dominio}")
async def retornar_emails(dominio: str):
    return regras_buscar_email_mesmo_dominio(dominio)


# Se não existir usuário com o id_usuario retornar falha, 
# senão cria um endereço, vincula ao usuário e retornar OK
@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Endereco, id_usuario: int):
    ids = map(lambda x: x['id'], db_usuarios)
    if id_usuario in ids:
        novo_endereco = regras_cadastrar_endereco(endereco.dict())   
        novo_endereco['id_usuario'] = id_usuario
        regras_vincular_end_ao_usuario(novo_endereco)
        print(db_end)
        return OK
    return FALHA


# Se não existir endereço com o id_endereco retornar falha, 
# senão deleta endereço correspondente ao id_endereco e retornar OK
# (lembrar de desvincular o endereço ao usuário)
@app.delete("/usuario/{id_usuario}/endereco/{id_endereco}")
async def deletar_endereco(id_usuario: int, id_endereco: int):
    print("deletando endereco: ", id_endereco, " do usuario: ", id_usuario)
    return regras_deletar_endereco_pelo_id(id_usuario, id_endereco)
    

# Se tiver outro produto com o mesmo ID retornar falha, 
# senão cria um produto e retornar OK
@app.post("/produto/")
async def criar_produto(produto: Produto):
    ids = map(lambda x: x['id'], db_produtos)
    if produto.id in ids:
        return FALHA
    produto = regras_cadastrar_produto(produto.dict())
    print(db_produtos)
    return produto
    

# Se não existir produto com o id_produto retornar falha, 
# senão deleta produto correspondente ao id_produto e retornar OK
# (lembrar de desvincular o produto dos carrinhos do usuário)
@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    print("deletando produto: ", id_produto) 
    return regras_deletar_produto_pelo_id(id_produto)


# Se não existir usuário com o id_usuario ou id_produto retornar falha, 
# se não existir um carrinho vinculado ao usuário, crie o carrinho
# e retornar OK
# senão adiciona produto ao carrinho e retornar OK
@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    return OK


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_carrinho(id_usuario: int):
    return CarrinhoDeCompras


# Se não existir carrinho com o id_usuario retornar falha, 
# senão retorna o o número de itens e o valor total do carrinho de compras.
@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
    numero_itens, valor_total = 0
    return numero_itens, valor_total


# Se não existir usuário com o id_usuario retornar falha, 
# senão deleta o carrinho correspondente ao id_usuario e retornar OK
@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    return OK


@app.get("/")
async def bem_vinda():
    site = "Seja bem vinda"
    return site.replace('\n', '')