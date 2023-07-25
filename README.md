# Gerenciador_estoque
Aplicação criada em python, flask e um pouco de javascript. Desenvolvido com intuito de automatizar/simplificar uma tarefa que preciso fazer no meu serviço como almoxarife de obras.


Foi importado do sistema SIENGE, que é o software genrenciador de obras, da construtora em que trabalho, uma lista contendo todos os itens do meu estoque, a ideia aqui 
é uma aplicação web, que possua login para os usuários e permita acesso á alguns módulos, sendo o principal deles e até o momento o único implementado o módulo de "Baixa por itens".
A função desse módulo é bem simples, ler um qrcode que támbem foi gerado através de um código python, capturar esse valor e preencher o campo "código" de uma formulário, que irá fazer a busca dentro
do banco de dados e retornar ao usário o nome do item, assim o usuário poderá digitar a quantidade que deverá sair do estoque daquele item, ao final da lista, o botão gerar arquivo irá baixa um .CSV
que salvara todas as informações da lista, me permitindo assim importar essa lista no momento em que vou dar baixa no sistema SIENGE, isso economiza em 99% o meu tempo para realizar essa tarefa de forma manual.
