lexer grammar SpellScript;

// --- PALAVRAS-CHAVE ---
KW_NIVEL     : 'NIVEL_REQUERIDO';
KW_ELEMENTO  : 'ELEMENTO';
KW_ALCANCE   : 'ALCANCE';
KW_AREA      : 'AREA';
KW_MANA      : 'MANA';
KW_TURNO     : 'TURNO';
KW_DANO      : 'DANO';
KW_EFEITO    : 'EFEITO';
KW_POR       : 'POR';

// --- VALORES FIXOS ENUMERADOS ---
ELEMENTO_VAL : 'FOGO' | 'GELO' | 'RAIO' | 'TERRA' | 'AGUA' | 'AR' | 'LUZ' | 'TREVAS';

// --- OPERADORES E PONTUAÇÃO ---
DOIS_PONTOS  : ':';
MAIS         : '+';
MENOS        : '-';
MULT         : '*';
DIV          : '/';
ABRE_PAR     : '(';
FECHA_PAR    : ')';

// --- TIPOS DE DADOS GENÉRICOS ---
// Identificadores (nomes de variáveis/atributos)
IDENT        : [a-zA-Z_] [a-zA-Z_0-9]*;

// Números inteiros e reais
NUMERO       : [0-9]+ ('.' [0-9]+)?;

// Literais de texto entre aspas duplas
TEXTO        : '"' ~['"\r\n]* '"';

// --- REGRAS DE DESCARTE (SKIP) ---
COMENT       : '#' ~[\r\n]* -> skip;
ESPACO       : [ \t\r\n]+ -> skip;
