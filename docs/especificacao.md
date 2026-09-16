Especificação da Linguagem: SpellScript
1. Para que serve a linguagem
A SpellScript é uma Linguagem de Domínio Específico (DSL) declarativa voltada para a definição, estruturação e validação das regras de feitiços e habilidades em sistemas de RPG. Ela desacopla os dados balanceamento do código-fonte do jogo, permitindo que game designers criem magias em arquivos de texto simples que são validados e compilados para um formato consumível pela engine.

2. Programa de exemplo completo
Abaixo está o exemplo de um feitiço de "Bola de Fogo", com comentários linha a linha explicando cada declaração:

# Define as propriedades da magia Bola de Fogo

NIVEL_REQUERIDO: 5                 # Define o nível mínimo (5) do personagem para conjurar
ELEMENTO: FOGO                     # Associa o tipo elemental da magia como Fogo
ALCANCE: 20.5                      # Define a distância máxima de conjuração (20.5 metros)
AREA: 5                            # Define o raio de explosão ou impacto (5 metros)
MANA: 20 + 5 / TURNO               # Define um custo de 20 de mana base, mais 5 por turno mantido
DANO: 10 + (NIVEL_CONJURADOR * 3)  # Fórmula de dano baseando-se em um valor fixo e variável de escala
EFEITO: "Queimadura" POR 2 TURNO   # Aplica o status de texto "Queimadura" com duração de 2 turnos
3. Tipos de dado
A linguagem suporta os seguintes tipos de dados em suas declarações:

Número Inteiro: Utilizado para níveis, raios de área e quantidades de turnos (ex: 5, 20).

Número Real: Utilizado para precisão em distâncias e alcances (ex: 20.5).

Texto (String): Sequência de caracteres entre aspas duplas, utilizada para nomes de efeitos de status (ex: "Queimadura").

Identificadores/Variáveis: Nomes que referenciam atributos dinâmicos do jogo para as fórmulas matemáticas (ex: NIVEL_CONJURADOR).

Palavras-chave e Literais Enumerados: Constantes da própria linguagem que definem elementos e comportamentos (ex: FOGO, GELO, TURNO).

4. Comandos (Declarações)
Sendo uma linguagem declarativa, os "comandos" são palavras-chave seguidas do operador : que definem as propriedades do feitiço:

NIVEL_REQUERIDO: Declara o nível base.

ELEMENTO: Declara a afinidade elemental.

ALCANCE: Declara a distância máxima.

AREA: Declara o raio de efeito.

MANA: Declara a fórmula do custo de conjuração/manutenção.

DANO: Declara a expressão matemática que calcula o poder do feitiço.

EFEITO: Declara uma condição aplicada ao alvo e sua duração através da diretiva POR ... TURNO.

5. Operadores e precedência
A linguagem suporta expressões aritméticas para o cálculo de MANA e DANO. A precedência segue a regra matemática padrão (do mais forte para o mais fraco):

Parênteses: ( ) para agrupamento e máxima prioridade.

Multiplicação e Divisão: * e / (avaliados da esquerda para a direita).

Adição: + (avaliado da esquerda para a direita).

6. Como são os comentários
Os comentários são de linha única e inicializados pelo símbolo #. Tudo que vier após o # até o final da linha será descartado pelo analisador léxico.

7. O que a linguagem deliberadamente não faz
Para manter um escopo estrito, maduro e coeso ao domínio de design de magias, a SpellScript:

Não executa o combate em tempo real: A linguagem apenas valida e estrutura as propriedades das magias; os cálculos de dano final (considerando resistências do alvo) e a renderização ficam a cargo do motor do jogo.

Não possui estruturas de controle de fluxo genéricas: Não há suporte para laços de repetição (while, for) nem condicionais arbitrárias (if/else), mantendo a linguagem 100% declarativa.

Não gerencia fichas de personagens ou inventários: A linguagem não trata atributos globais dos jogadores (vida máxima, ouro, experiência), restringindo seu ecossistema exclusivamente ao balanceamento dos feitiços em si.