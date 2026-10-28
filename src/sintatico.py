import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'gerado'))
sys.path.insert(0, os.path.join(BASE_DIR, 'src'))

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from SpellScriptLexer import SpellScriptLexer
from SpellScriptParser import SpellScriptParser
from semantico import SemanticoVisitor


# Listener para registrar e contar erros léxicos
class LexerErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.erros += 1


def analisar_arquivo(caminho_arquivo):
    input_stream = FileStream(caminho_arquivo, encoding='utf-8')
    
    # Análise Léxica
    lexer = SpellScriptLexer(input_stream)
    lexer_listener = LexerErrorListener()
    lexer.addErrorListener(lexer_listener)
    
    tokens = CommonTokenStream(lexer)
    
    # Análise Sintática
    parser = SpellScriptParser(tokens)
    tree = parser.programa()

    # Checa erros no Lexer E no Parser
    if lexer_listener.erros > 0 or parser.getNumberOfSyntaxErrors() > 0:
        print("\n[X] Falha na Análise Léxica ou Sintática. Corrija os erros acima antes de prosseguir.")
        return

    # Análise Semântica (E4)
    visitor = SemanticoVisitor()
    erros_semanticos = visitor.visit(tree)

    if erros_semanticos:
        print("\n--- Erros Semânticos Encontrados (E4) ---")
        for erro in erros_semanticos:
            print(f" - {erro}")
    else:
        print("\n[V] Análise sintática e semântica concluídas com SUCESSO!")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        analisar_arquivo(sys.argv[1])
    else:
        print("Uso: python src/sintatico.py <caminho_do_arquivo.spell>")