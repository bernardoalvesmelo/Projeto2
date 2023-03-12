# Teste02

O projeto é dividido em duas partes:

Apiback: Trata-se do backend, é realizado utilizando Flask e algumas bibliotecas auxiliares, contém uma classe destinada a criação e manutenção da database necessária 
em PostgreSQL, e possui um outro arquivo para gerenciamento de rotas, contando com uma forma simplificada de autenticação de usuário e sessão, e também limpeza dos 
eventuais inputs de usuário. A database consiste em duas tabelas simples, uma de equipamentos e outra sobre chamados de equipamentos.

Equipamentos_Projeto: O projeto é dividido em Equipamentos e Chamados, ambos possuindo um arquivo HTML, Javascript e CSS. O projeto trata da criação, remoção, 
atualização, pesquisa e visualização de equipamentos e chamados. Conta com um sistema de autenticação, e saída de sessão através de um botão de logout. Ao navegar pelo 
projeto você pode notar algumas semelhanças entre os códigos, a ideia inicial era criar um projeto utilizando Vue, e consequentemente carregar componentes dinamicamente 
em uma única página, mas por questões de tempo, foi realizado utilizando Javascript sozinho. Para mudanças serem realizadas agora, necessitaria uma enorme refatoração que eu não tenho condições de realizar no momento, mas isso é questão apenas de organização e otimização, o projeto é funcional. Eu também analisei a ideia de realizar a 
lógica de componentes utilizando Javascript apenas, mas rapidamente notei que o projeto estava ficando extremamente confuso, então optei por manter a estrutura
dividida.

Esse projeto foi realizado com intenção de verificar meu modo de programar, então eu acredito que deve conter diversas imprecisões e implementações problemáticas, então 
se você tiver alguma sugestão eu agradeceria muito pelo feedback.
