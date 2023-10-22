from __future__ import annotations
import sqlite3
from numpy import source

banco = sqlite3.connect('primeiroTeste.db')
cursor = banco.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS ranking(nome text, score integer, dificuldade text)")
banco.commit()


def top3(count: int = 0, dificuldade: str = "2048") -> dict[int: tuple[None | str], int]:  # 9
    try:  # 10
        assert -1 <= count <= 3
    except AssertionError:
        raise ValueError('Invalid argument count, must be no more than 3 and no less than -1')
    cursor.execute(
        f"SELECT nome, max(score) score FROM ranking WHERE dificuldade = \"{dificuldade}\" GROUP by nome ORDER by score ASC LIMIT 3")  # 11
    source = cursor.fetchall()
    espaçamento = [source[i] for i in range(len(source)) if len(source) >= 1] + [(None, -1)] * (3 - len(source))  # 12
    resultado = {i: dict(name=espaçamento[i - 1][0], score=espaçamento[i - 1][1]) for i in range(1, 4)}  # 13
    return resultado if count == 0 else resultado[count]


def inserirResultado(nome: str, score: int, dificuldade: str) -> None:  # 14
    cursor.execute(f'INSERT INTO ranking (nome, score, dificuldade) VALUES (\"{nome}\", {score}, \"{dificuldade}\")')
    banco.commit()  # 15
