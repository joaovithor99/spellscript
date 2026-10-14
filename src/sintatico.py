import sys
import os

# Adiciona a raiz do projeto ao caminho de busca do Python
sys.path.insert(0, os.path.abspath('.'))

from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from gerado.SpellScriptLexer import SpellScriptLexer
from gerado.SpellScriptParser import SpellScriptParser

class SintaticoErrorListener(ErrorListener):
    def __init__(self):
        super(SintaticoErrorListener, self).__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.erros.append(f"Erro Sintático na linha {line}, coluna {column}: {msg}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/sintatico.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]
    input_stream = FileStream(caminho_arquivo, encoding='utf-8')
    
    lexer = SpellScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)

    parser = SpellScriptParser(stream)
    
    error_listener = SintaticoErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    # Executa a regra inicial (programa)
    tree = parser.programa()

    if error_listener.erros:
        print(f"❌ {len(error_listener.erros)} erro(s) sintático(s) encontrado(s):")
        for erro in error_listener.erros:
            print("  -", erro)
        sys.exit(1)
    else:
        print("✅ Sintaxe analisada com sucesso! Sem erros sintáticos.")
        print("\nÁrvore Sintática (Parse Tree):")
        print(tree.toStringTree(recog=parser))

if __name__ == "__main__":
    main()