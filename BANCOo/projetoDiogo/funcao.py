from flask import Flask, jsonify, request
from flask_bcrypt import generate_password_hash, check_password_hash


def validar_senha(senha):
    if len(senha) <8:
        return 'Senha fraca: deve conter pelo menos 8 caracteres'
    elif not any(char.isdigit() for char in senha) or not any(char.isalnum() for char in senha):
        return 'Senha fraca: deve conter pelo menos um número e um caractér especial'
    elif not any(char.isupper() for char in senha or not any(char.islower() for char in senha)):
        return 'Senha fraca: deve conter pelo menos uma letra maiúscula e uma letra minúscula'
    else:
        return None


def criptografar(senha):
    return generate_password_hash(senha).decode('utf-8')


def checar_senha(senha, senha_criptografada):
    return check_password_hash(senha_criptografada, senha)