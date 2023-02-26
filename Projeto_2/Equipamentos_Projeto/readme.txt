Pode utilizar qualquer html para iniciar, mas é indicado iniciar com o html
da pasta Equipamentos porque é necessário existir equipamentos já registrados
para criar chamados.

Durante a criação do projeto a rota utilizada pelo projeto em python utilizando 
flask era http://127.0.0.1:5000, se mudar deve-se alterar as rotas encontradas
na primeira linha de ambos index.js para não ocorrer erros.

Embora o projeto mostre componentes semelhantes que parecem ser reutilizados, o projeto 
encontra-se dividido, então os programas funcionam de maneira independente caso desejar, 
sendo necessário apenas remover o elemento <a> correpondente, porém os chamados precisam 
de ao menos um equipamento para serem criados.
