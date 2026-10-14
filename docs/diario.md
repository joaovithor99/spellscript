# Diário de Bordo - SpellScript

## 16/09
Definimos o domínio da linguagem: criação de feitiços de RPG. Escrevemos a especificação no arquivo `especificacao.md` para delimitar bem o que a linguagem faz e, principalmente, o que não faz (não executa combate nem lida com ficha de personagem).
Criamos a primeira versão da gramática `SpellScript.g4` no ANTLR e montamos o script `lexico.py` implementando um ErrorListener customizado para poder reportar a linha e a coluna de caracteres inválidos.

