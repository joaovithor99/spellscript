# SpellScript

A SpellScript é uma Linguagem de Domínio Específico (DSL) declarativa para criar e balancear regras de feitiços em sistemas de RPG. 

**Fase atual:** Etapa E2 (Especificação e Analisador Léxico).

**Exemplo de uso:**
NIVEL_REQUERIDO: 5
ELEMENTO: FOGO
MANA: 20 + 5 / TURNO

**Como instalar as dependências (Requer Python 3):**
pip install antlr4-tools antlr4-python3-runtime

**Como gerar o analisador (ANTLR 4):**
./gerar.sh

**Como rodar o analisador léxico:**
python src/lexico.py exemplos/bola_de_fogo.spell