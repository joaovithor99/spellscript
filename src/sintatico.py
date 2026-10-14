import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

# Importa o Lexer e o Parser gerados
from gerado.SpellScriptLexer import SpellScriptLexer
from gerado.SpellScriptParser import SpellScriptParser

# Capturador customizado para erros sintáticos
class SintaticoErrorListener(ErrorListener):
    def __init__(self):
        super(SintaticoErrorListener, self).__init__()
        self.erros = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Captura erros de sintaxe (ex: faltou :, parêntese não fechado, etc.)
        self.erros.append(f"Erro Sintático na linha {line}, coluna {column}: {msg}")

def main():
    if len(sys.argv) < 2:
        print("Uso: python src/sintatico.py <caminho_do_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    input_stream = FileStream(caminho_arquivo, encoding='utf-8')
    
    # 1. Analisador Léxico
    lexer = SpellScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)

    # 2. Analisador Sintático
    parser = SpellScriptParser(stream)
    
    # Substitui os ouvintes de erro padrão pelo nosso customizado
    error_listener = SintaticoErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    # 3. Chama a regra inicial (programa)
    tree = parser.programa()

    # 4. Verifica se houveram erros
    if error_listener.erros:
        print(f"❌ {len(error_listener.erros)} erro(s) sintático(s) encontrado(s):")
        for erro in error_listener.erros:
            print("  -", erro)
        sys.exit(1)
    else:
        print("✅ Sintaxe correta!")
        print("\nÁrvore Sintática (Parse Tree):")
        print(tree.toStringTree(recog=parser))

if __name__ == "__main__":
    main()
