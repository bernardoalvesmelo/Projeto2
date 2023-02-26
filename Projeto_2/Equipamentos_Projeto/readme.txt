Pode utilizar qualquer html para iniciar, mas é indicado iniciar com o html
da pasta Equipamentos porque é necessário existir equipamentos já registrados
para criar chamados.

Durante a criação do projeto a rota utilizada pelo projeto em python utilizando 
flask era http://127.0.0.1:5000, se mudar deve-se alterar as rotas encontradas
na primeira linha de ambos index.js para não ocorrer erros.

A ideia inicial do projeto era migrar a lógica para vue, por isso mesmo apresentando
componentes semelhantes que poderiam ser reutilizados, encontra-se dividido.
Os programas funcionam de maneira independente caso desejar apenas removendo o elemento <a>,
porém os chamados precisam de ao menos um equipamento para serem criados. O projeto utiliza
alguns métodos de limpeza para inputs do usuário, então se alguns caracteres especiais como <
estiverem não aparacendo nos campos, é por isso. 
