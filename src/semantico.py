import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'gerado'))

from SpellScriptVisitor import SpellScriptVisitor
from SpellScriptParser import SpellScriptParser


class SemanticoVisitor(SpellScriptVisitor):
    VARIAVEIS_PERMITIDAS = {
        "NIVEL_CONJURADOR", 
        "INTELIGENCIA", 
        "FORCA", 
        "AGILIDADE", 
        "SABEDORIA",
        "TURNO"
    }

    ATRIBUTOS_OBRIGATORIOS = {
        "NIVEL_REQUERIDO", 
        "ELEMENTO", 
        "MANA"
    }

    def __init__(self):
        self.atributos_declarados = set()
        self.erros = []

    def visitPrograma(self, ctx):
        self.visitChildren(ctx)
        
        faltantes = self.ATRIBUTOS_OBRIGATORIOS - self.atributos_declarados
        for attr in faltantes:
            self.erros.append(f"Erro Semântico: Atributo obrigatório '{attr}' não foi declarado no feitiço.")
            
        return self.erros

    def _registrar_atributo(self, nome_atributo, ctx):
        if nome_atributo in self.atributos_declarados:
            linha = ctx.start.line
            self.erros.append(f"Erro Semântico (Linha {linha}): Atributo '{nome_atributo}' já foi declarado anteriormente.")
        self.atributos_declarados.add(nome_atributo)

    def visitDecl_nivel(self, ctx):
        self._registrar_atributo("NIVEL_REQUERIDO", ctx)
        return self.visitChildren(ctx)

    def visitDecl_elemento(self, ctx):
        self._registrar_atributo("ELEMENTO", ctx)
        return self.visitChildren(ctx)

    def visitDecl_mana(self, ctx):
        self._registrar_atributo("MANA", ctx)
        return self.visitChildren(ctx)

    def visitDecl_dano(self, ctx):
        self._registrar_atributo("DANO", ctx)
        return self.visitChildren(ctx)

    def visitDecl_alcance(self, ctx):
        self._registrar_atributo("ALCANCE", ctx)
        return self.visitChildren(ctx)

    def visitDecl_area(self, ctx):
        self._registrar_atributo("AREA", ctx)
        return self.visitChildren(ctx)

    def visitDecl_efeito(self, ctx):
        self._registrar_atributo("EFEITO", ctx)
        return self.visitChildren(ctx)

    # Captura universal de identificadores em qualquer nó da árvore
    def visitTerminal(self, node):
        if node.getSymbol().type == SpellScriptParser.IDENT:
            var_nome = node.getText()
            if var_nome not in self.VARIAVEIS_PERMITIDAS:
                linha = node.getSymbol().line
                self.erros.append(f"Erro Semântico (Linha {linha}): Variável '{var_nome}' não é reconhecida pelo sistema.")
        return super().visitTerminal(node)

    def visitExpMultDiv(self, ctx):
        if ctx.DIV():
            dir_text = ctx.expressao(1).getText()
            if dir_text == "0":
                linha = ctx.start.line
                self.erros.append(f"Erro Semântico (Linha {linha}): Divisão por zero detectada.")
        return self.visitChildren(ctx)