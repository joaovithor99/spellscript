grammar SpellScript;
programa : EOF ;

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

// --- VALORES FIXOS ---
ELEMENTO_VAL : 'FOGO' | 'GELO' | 'RAIO' | 'TERRA' | 'AGUA' | 'AR' | 'LUZ' | 'TREVAS';

// --- OPERADORES E PONTUAÇÃO ---
DOIS_PONTOS  : ':';
MAIS         : '+';
MULT         : '*';
DIV          : '/';
ABRE_PAR     : '(';
FECHA_PAR    : ')';

// --- TIPOS DE DADOS GENÉRICOS ---
// A regra IDENT pega palavras que não caíram nas regras acima
IDENT        : [a-zA-Z_] [a-zA-Z_0-9]*;
// NUMERO aceita inteiros e reais, conforme exemplo do professor
NUMERO       : [0-9]+ ('.' [0-9]+)?;
// TEXTO aceita qualquer coisa entre aspas duplas
TEXTO        : '"' ~['"\r\n]* '"';

// --- IGNORADOS ---
// Descarta comentários que começam com # e espaços em branco
COMENT       : '#' ~[\r\n]* -> skip;
ESPACO       : [ \t\r\n]+ -> skip;
grammar SpellScript;