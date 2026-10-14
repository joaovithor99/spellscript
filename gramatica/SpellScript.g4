grammar SpellScript;

// ==========================================
// --- REGRAS SINTÁTICAS (PARSER) ---
// ==========================================

programa : (declaracao)+ EOF ;

declaracao
    : decl_nivel
    | decl_elemento
    | decl_alcance
    | decl_area
    | decl_mana
    | decl_dano
    | decl_efeito
    ;

decl_nivel    : KW_NIVEL DOIS_PONTOS expressao ;
decl_elemento : KW_ELEMENTO DOIS_PONTOS ELEMENTO_VAL ;
decl_alcance  : KW_ALCANCE DOIS_PONTOS expressao ;
decl_area     : KW_AREA DOIS_PONTOS expressao ;
decl_mana     : KW_MANA DOIS_PONTOS expressao ;
decl_dano     : KW_DANO DOIS_PONTOS expressao ;
decl_efeito   : KW_EFEITO DOIS_PONTOS TEXTO (KW_POR expressao KW_TURNO)? ;

expressao
    : ABRE_PAR expressao FECHA_PAR            # ExpParenteses
    | expressao (MULT | DIV) expressao        # ExpMultDiv
    | expressao (MAIS | MENOS) expressao      # ExpSomSub
    | NUMERO                                 # ExpNumero
    | IDENT                                  # ExpVariavel
    | KW_TURNO                               # ExpTurno
    ;

// ==========================================
// --- REGRAS LÉXICAS (LEXER) ---
// ==========================================

KW_NIVEL     : 'NIVEL_REQUERIDO';
KW_ELEMENTO  : 'ELEMENTO';
KW_ALCANCE   : 'ALCANCE';
KW_AREA      : 'AREA';
KW_MANA      : 'MANA';
KW_TURNO     : 'TURNO';
KW_DANO      : 'DANO';
KW_EFEITO    : 'EFEITO';
KW_POR       : 'POR';

ELEMENTO_VAL : 'FOGO' | 'GELO' | 'RAIO' | 'TERRA' | 'AGUA' | 'AR' | 'LUZ' | 'TREVAS';

DOIS_PONTOS  : ':';
MAIS         : '+';
MENOS        : '-';
MULT         : '*';
DIV          : '/';
ABRE_PAR     : '(';
FECHA_PAR    : ')';

IDENT        : [a-zA-Z_] [a-zA-Z_0-9]*;
NUMERO       : [0-9]+ ('.' [0-9]+)?;
TEXTO        : '"' ~['"\r\n]* '"';

COMENT       : '#' ~[\r\n]* -> skip;
ESPACO       : [ \t\r\n]+ -> skip;