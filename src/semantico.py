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

    ATRIBUTOS_NAO_NEGATIVOS = {
        "NIVEL_REQUERIDO", 
        "MANA", 
        "ALCANCE", 
        "AREA", 
        "DANO"
    }

    # Incompatibilidades elementais comuns no texto do efeito
    CONTRADICOES_ELEMENTAIS = {
        "FOGO": ["congel", "gelo", "frio", "geada"],
        "GELO": ["queim", "fogo", "chama", "incend"],
        "AGUA": ["queim", "fogo", "chama", "incend"],
        "RAIO": ["congel", "queim"],
        "TROVAO": ["congel", "queim"],
        "LUZ": ["trevas", "necro", "maldic"],
        "TREVAS": ["sagrad", "cura", "bencao"]
    }

    def __init__(self):
        self.atributos_declarados = set()
        self.valores_atributos = {}  # Guarda os nós dos atributos para validações cruzadas
        self.erros = []
        self.avisos = []

    def visitPrograma(self, ctx):
        self.visitChildren(ctx)
        
        # 1. Validação de Atributos Obrigatórios Ausentes
        faltantes = self.ATRIBUTOS_OBRIGATORIOS - self.atributos_declarados
        for attr in faltantes:
            self.erros.append(f"Erro Semântico: Atributo obrigatório '{attr}' não foi declarado no feitiço.")

        # 2. Regras de Balanceamento e Lógica de Negócio do RPG
        self._validar_regras_balanceamento()
            
        return self.erros + self.avisos

    def _registrar_e_validar_atributo(self, nome_atributo, ctx):
        # Validação de Unicidade
        if nome_atributo in self.atributos_declarados:
            linha = ctx.start.line
            self.erros.append(f"Erro Semântico (Linha {linha}): Atributo '{nome_atributo}' já foi declarado anteriormente.")
        self.atributos_declarados.add(nome_atributo)
        self.valores_atributos[nome_atributo] = ctx

        # Validação de Valor Negativo (para expressões estáticas)
        if nome_atributo in self.ATRIBUTOS_NAO_NEGATIVOS and hasattr(ctx, 'expressao'):
            val = self._avaliar_estatico(ctx.expressao())
            if val is not None and val < 0:
                linha = ctx.start.line
                self.erros.append(f"Erro Semântico (Linha {linha}): O atributo '{nome_atributo}' não pode ter valor negativo (valor: {val}).")

    def _avaliar_estatico(self, ctx):
        """Avalia estaticamente subexpressões numéricas puras."""
        if ctx is None:
            return None
        
        texto = ctx.getText()
        for var in self.VARIAVEIS_PERMITIDAS:
            if var in texto:
                return None
        
        try:
            return eval(texto)
        except Exception:
            return None

    def _validar_regras_balanceamento(self):
        nivel = self._obter_valor_numerico("NIVEL_REQUERIDO")
        mana = self._obter_valor_numerico("MANA")
        dano = self._obter_valor_numerico("DANO")
        area = self._obter_valor_numerico("AREA")
        alcance = self._obter_valor_numerico("ALCANCE")
        elemento = self._obter_texto_atributo("ELEMENTO")
        efeito_texto = self._obter_texto_efeito()

        # Regra 1: Relação Custo / Nível (Nível 1 + Mana 0 + Dano Alto > 15)
        if nivel == 1 and mana == 0 and dano is not None and dano > 15:
            linha = self.valores_atributos["MANA"].start.line if "MANA" in self.valores_atributos else 1
            self.avisos.append(f"Aviso de Balanceamento (Linha {linha}): Feitiço de Nível 1 com custo MANA: 0 possui DANO elevado ({dano} > 15).")

        # Regra 2: Consistência Área / Alcance
        if area is not None and area > 0 and alcance == 0:
            elementos_aura = {"LUZ", "TERRA", "ESCUDO"}
            linha = self.valores_atributos["AREA"].start.line if "AREA" in self.valores_atributos else 1
            if elemento not in elementos_aura:
                self.avisos.append(f"Aviso de Consistência (Linha {linha}): AREA > 0 ({area}) com ALCANCE: 0 atingirá o próprio conjurador. Verifique se é um feitiço de aura/autocast.")

        # Regra 3: Afinidade Elemental vs Texto do Efeito
        if elemento and efeito_texto:
            elemento_upper = elemento.upper()
            efeito_lower = efeito_texto.lower()
            if elemento_upper in self.CONTRADICOES_ELEMENTAIS:
                for palavra in self.CONTRADICOES_ELEMENTAIS[elemento_upper]:
                    if palavra in efeito_lower:
                        linha = self.valores_atributos["EFEITO"].start.line if "EFEITO" in self.valores_atributos else 1
                        self.avisos.append(f"Aviso de Afinidade (Linha {linha}): Contradição entre o ELEMENTO '{elemento_upper}' e o efeito '{efeito_texto}'.")
                        break

    def _obter_valor_numerico(self, nome_atributo):
        if nome_atributo not in self.valores_atributos:
            return None
        ctx = self.valores_atributos[nome_atributo]
        if hasattr(ctx, 'expressao'):
            return self._avaliar_estatico(ctx.expressao())
        return None

    def _obter_texto_atributo(self, nome_atributo):
        if nome_atributo not in self.valores_atributos:
            return None
        return self.valores_atributos[nome_atributo].getText().split(":")[-1].strip()

    def _obter_texto_efeito(self):
        if "EFEITO" not in self.valores_atributos:
            return None
        ctx = self.valores_atributos["EFEITO"]
        if hasattr(ctx, 'TEXTO') and ctx.TEXTO():
            return ctx.TEXTO().getText().strip('"')
        return ctx.getText()

    def visitDecl_nivel(self, ctx):
        self._registrar_e_validar_atributo("NIVEL_REQUERIDO", ctx)
        return self.visitChildren(ctx)

    def visitDecl_elemento(self, ctx):
        self._registrar_e_validar_atributo("ELEMENTO", ctx)
        return self.visitChildren(ctx)

    def visitDecl_mana(self, ctx):
        self._registrar_e_validar_atributo("MANA", ctx)
        return self.visitChildren(ctx)

    def visitDecl_dano(self, ctx):
        self._registrar_e_validar_atributo("DANO", ctx)
        return self.visitChildren(ctx)

    def visitDecl_alcance(self, ctx):
        self._registrar_e_validar_atributo("ALCANCE", ctx)
        return self.visitChildren(ctx)

    def visitDecl_area(self, ctx):
        self._registrar_e_validar_atributo("AREA", ctx)
        return self.visitChildren(ctx)

    def visitDecl_efeito(self, ctx):
        self._registrar_e_validar_atributo("EFEITO", ctx)
        return self.visitChildren(ctx)

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