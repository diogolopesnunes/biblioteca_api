from flask import Flask, jsonify, request
from main import app, con

@app.route('/listar_livro', methods=['GET'])
def listar_livro():
    try:
        cur = con.cursor()

        cur.execute('select id_livro, titulo, autor, ano_publicado from livros')
        livros = cur.fetchall()
        livros_lista = []
        for livro in livros:
            livros_lista.append({
                'id_livro': livro[0],
                'titulo': livro[1],
                'autor': livro[2],
                'ano_publicado': livro[3]
            })

        return jsonify(mensagem='Lista de Livros', livros=livros_lista)

    except Exception as e:
        return jsonify({'message': f'Erro ao consultar banco de dados: {e}'}), 500
    finally:
        cur.close()


@app.route('/criar_livro', methods=['POST'])
def criar_lirvo():
    try:
        cur = con.cursor()
        dados = request.get_json()

        titulo = dados.get('titulo')
        autor = dados.get('autor')
        ano_publicado = dados.get('ano_publicado')

        cur = con.cursor()

        cur.execute('select 1 from livros where titulo = ?', (titulo,))
        if cur.fetchone():
            return jsonify({'erro': 'Livro já cadastrado'}), 400

        cur.execute("""insert into livros (titulo, autor, ano_publicado)
                        values (?, ?, ?)""", (titulo, autor, ano_publicado))

        con.commit()
        return jsonify({'mensagem': 'Livro cadastrado com suuuuuuuuuuuuuuuuuuuuuuuuuuuucesso',
                         'livro': {
                        'titulo': titulo,
                        'autor': autor,
                        'ano_publicado': ano_publicado
        }
        }), 201

    except Exception as e:
        return jsonify({'message': 'Erro ao cadastrar livro'}), 500
    finally:
        cur.close()


@app.route('/deletar_livro/<int:id_livro>', methods=['DELETE'])
def deletar_livro(id_livro):
    cur = con.cursor()

    cur.execute('select 1 from livros where id_livro = ?', (id_livro,))
    if not cur.fetchone():
        cur.close()
        return jsonify({'error': 'Livro não encontrado'}), 404

    cur.execute('delete from livros where id_livro = ?', (id_livro,))
    con.commit()
    cur.close()

    return jsonify({'mensagem': 'Livro deletado com suuuuuuuuuuuuuuuuuuuucesso',
                    'id_livro':id_livro}), 201


@app.route('/editar_livro/<int:id_livro>', methods=['PUT'])
def editar_livro(id_livro):
    cur = con.cursor()
    cur.execute("""select id_livro, titulo, autor, ano_publicado
                    from livros
                    where id_livro = ?""", (id_livro,))
    tem_livro = cur.fetchone()

    if not tem_livro:
        cur.close()
        return jsonify({'error': 'Livro não encontrado'}), 404

    dados = request.get_json()
    titulo = dados.get('titulo')
    autor = dados.get('autor')
    ano_publicado = dados.get('ano_publicado')

    cur.execute(""" update livros set titulo = ?, autor = ?, ano_publicado = ?
                    where id_livro = ?""", (titulo, autor, ano_publicado, id_livro))

    con.commit()
    cur.close()

    return jsonify({'mensagem': 'Livro editado com suuuuuuuuuuuuuuuucesso',
                    'livro': {
                        'id_livro': id_livro,
                        'titulo': titulo,
                        'autor': autor,
                        'ano_publicado': ano_publicado
                    }
    }), 201

@app.route(/'senha_forte', methods=['POST'])
def senha_forte():
    dados = request.get_json()
    senha = dados.get('senha')

    if len(senha) <8:
        return jsonify({'mensagem': 'Senha fraca: deve conter pelo menos 8 caracteres'}), 400
    elif not any(char.isdigit() for char in senha) and not any(char.isalnum() for char in senha):
        return jsonify({'mensagem': 'Senha fraca: deve conter pelo menos um número e um caractér especial'}), 400
    elif not any(char.isupper() for char in senha and not any(char.islower() for char in senha)):
        return jsonify({'mensagem': 'Senha fraca: deve conter pelo menos uma letra maiúscula e uma letra minúscula'}), 400
    else: