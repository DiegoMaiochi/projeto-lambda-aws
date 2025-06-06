# Projeto AWS Lambda: Envio de E-mails com SES

Este repositório contém o código-fonte e a documentação de uma função AWS Lambda desenvolvida para o trabalho da disciplina de Arquitetura em Cloud. A função atua como um serviço para enviar e-mails através do Amazon Simple Email Service (SES).

**ARN da Função Lambda:** `arn:aws:lambda:sa-east-1:617995201077:function:minhaFuncao`

## 1. Descrição da Função

A função `minhaFuncao` é uma API serverless que recebe os detalhes de um e-mail (destinatário, assunto e corpo) através de um evento JSON. Ela utiliza o AWS SDK (Boto3) para interagir com o Amazon SES e realizar o envio do e-mail de forma segura e desacoplada.

O objetivo é demonstrar a integração entre serviços da AWS (Lambda, SES, IAM) e seguir as boas práticas, como a configuração de permissões e a passagem de dados dinâmicos via evento, em vez de hardcoding.

## 2. Configuração Necessária

Para que esta função opere corretamente, duas configurações prévias são essenciais na conta AWS:

* **Amazon SES (Simple Email Service):** A conta AWS está, por padrão, no modo "Sandbox". Isso exige que tanto o endereço de e-mail remetente (definido no código) quanto os endereços destinatários sejam previamente verificados no console do SES.
* **Permissões IAM:** A "Função de Execução" (Execution Role) associada a esta Lambda precisa ter uma política de permissão que a autorize a usar o SES. A política `AmazonSESFullAccess` foi anexada para garantir essa permissão.

## 3. Entrada (Input)

A função espera receber um evento no formato JSON contendo três chaves obrigatórias:

* `to_email` (string): O endereço de e-mail do destinatário.
* `subject` (string): O assunto do e-mail.
* `body` (string): O corpo de texto do e-mail.

**Exemplo de evento de entrada (Input):**
```json
{
  "to_email": "nome_do_destinatario@exemplo.com",
  "subject": "Teste de envio via Lambda",
  "body": "Este é o corpo da mensagem de teste. O envio foi bem-sucedido!"
}
```

## 4. Saída (Output)

A função retorna um objeto JSON com um `statusCode` HTTP e um `body` detalhando o resultado da operação.

### Saída de Sucesso (`statusCode: 200`)
Indica que o SES aceitou a solicitação de envio. O corpo da resposta contém uma mensagem de sucesso e o `MessageId` único da transação.

**Exemplo de saída de sucesso:**
```json
{
  "statusCode": 200,
  "body": "\"E-mail enviado para nome_do_destinatario@exemplo.com! Message ID: 01030197431d8aea-....\""
}
```

## 5. Dependências

A função utiliza a biblioteca **Boto3**, que é o SDK da AWS para Python. Esta dependência já vem pré-instalada no ambiente de execução do AWS Lambda, não sendo necessário incluí-la em pacotes de deploy.

## 6. Como Testar

1.  No console da AWS Lambda, navegue até a aba **"Test"**.
2.  Crie um novo evento de teste.
3.  No campo "Event JSON", cole o modelo de entrada da **Seção 3**.
4.  **Importante:** Altere o valor de `to_email` para um endereço de e-mail que também tenha sido **verificado** na sua conta do SES.
5.  Clique no botão **"Test"**.
6.  Analise a seção "Response" e "Function Logs" para verificar o resultado. Um `statusCode: 200` indica sucesso.