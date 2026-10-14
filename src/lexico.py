import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

sys.path.append('./gerado')
from SpellScriptLexer import SpellScriptLexer

class LexerErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.erros = 0

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print(f"Erro Léxico na linha {line}, coluna {column}: caractere não reconhecido.")
        self.erros += 1

def main(arquivo):
    input_stream = FileStream(arquivo, encoding='utf-8')
    lexer = SpellScriptLexer(input_stream)

    lexer.removeErrorListeners()
    error_listener = LexerErrorListener()
    lexer.addErrorListener(error_listener)

    stream = CommonTokenStream(lexer)
    stream.fill()

    tokens_reconhecidos = 0

    for token in stream.tokens:
        if token.type == Token.EOF:
            break
        
        nome_token = lexer.symbolicNames[token.type]
        lexema = token.text
        linha = token.line
        
        print(f"{nome_token} {lexema} linha {linha}")
        tokens_reconhecidos += 1

    if error_listener.erros == 0:
        print(f"{tokens_reconhecidos} tokens reconhecidos")

if __name__ == '__main__':
    if len(sys.path) > 1 and len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Uso: python src/lexico.py <caminho_do_arquivo.spell>")