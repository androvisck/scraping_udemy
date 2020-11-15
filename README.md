# scrapping_udemy
  Este scrip trata-se de um estudo prático sobre Web Scrapping.   
  Ele faz a busca por uma palavra específica na plataforma Udemy e coleta alguns dados.   
  São eles: título do curso, avaliação, duração, quantidade de alunos e o endereço.   
  E, por fim, estrai todas as informações em um arquivo CSV.


Formas de obter a chave de acesso:

1a) Acesse: https://www.udemy.com/user/edit-api-clients/
2a) Solicite acesso (geralmente em menos de 48h o acesso é liberado)
3a) Após a liberação, acesse: https://www.udemy.com/developers/affiliate/methods/get-courses-list/
4a) Coloque o seu "ID de cliente" e o "Sua senha de cliente" nos respectivos campos e clique em "Teste você mesmo!"
5a) Vá até o campo cabeçalho e copie a sua autorização

{
  "Accept": "application/json, text/plain, */*",
  "Authorization": "SUA CHAVE DE ACESSO",
  "Content-Type": "application/json;charset=utf-8"
}

6a) Cole a autorização no campo headers dentro do script.

headers = {
    "Authorization": "COLE AQUI A SUA CHAVE AUTORIZAÇÃO",
    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
}

7a) Execute o código
