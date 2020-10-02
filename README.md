# Cotações diárias do Dólar

[![Build Status](https://travis-ci.org/open-bacen/cotacao-diaria-dolar.svg)](https://travis-ci.org/open-bacen/cotacao-diaria-dolar)
[![codecov](https://codecov.io/gh/open-bacen/cotacao-diaria-dolar/branch/master/graph/badge.svg)](https://codecov.io/gh/open-bacen/cotacao-diaria-dolar) 


Dólar Ptax é a média aritmética das taxas obtidas em quatro consultas diárias de câmbio.

## Qual Dólar?
Dólar Comercial de venda e compra.

## Para que serve a Ptax?
Utilizada para transações em dólar, desde a definição do dólar turismo à contratos empresariais.

## Horários de atualizações
A Ptax é atualizada em 4 janelas ao longo do dia: 
  - Entre às 10h e 10h10
  - Entre às 11h e 11h10
  - Entre às 12h e 12h10
  - Entre as 13h e 13h10

## Especificação da API
A Especificação da API está definida no site [Dados Abertos do Banco Central do Brasil](https://dadosabertos.bcb.gov.br/dataset/dolar-americano-usd-todos-os-boletins-diarios).


# Iniciando com o Projeto

## Instalação

```bash
$ pipenv shell
$ pipenv install
```

## Utilização

```bash
$ ./sample.py
```

## Testes

```bash
$ ./test_dolar.py
```

## Licença
[Licença MIT](LICENSE)
