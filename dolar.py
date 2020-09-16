#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
import logging

import requests
import json

logger = logging.getLogger(__name__)


class APIBancoCentral:
    def __init__(self, url):
        self.url = url

    def getURL(self):
        headers = {
            "Host": "olinda.bcb.gov.br",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Mobile Safari/537.36",
            "DNT": "1",
            "Content-Type": "application/json;charset=UTF-8;odata.metadata=minimal",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,mt;q=0.6,gl;q=0.5,he;q=0.4,ru;q=0.3,pl;q=0.2,la;q=0.1,es;q=0.1,fr;q=0.1,de;q=0.1,cy;q=0.1,und;q=0.1",
        }

        # Testa 10 vezes a resposta do site/api
        for _ in range(10):
            try:
                request = requests.get(self.url, headers=headers, timeout=None)
                if request.status_code == 200:
                    return request
                elif request.status_code != 200:
                    continue
            except requests.ConnectionError:
                return False


class Cotacao:
    def __init__(self, data_cotacao=None):
        self.cotation = False
        data_atual = data_cotacao

        # Se passar uma data específica como parâmetro na
        # instância do objeto Cotacao, então busca a cotação daquela data.
        # Senão busca a cotação da data atual.
        if data_atual is None:
            data_atual = date.today()

        ano = str(data_atual.year).zfill(4)
        mes = str(data_atual.month).zfill(2)
        dia = str(data_atual.day).zfill(2)
        data_base = f"{mes}-{dia}-{ano}"
        weekno = date.weekday(data_atual)
        if weekno in [5, 6]:  # 5=sabado e 6=domingo
            logger.info("Hoje não tem cotação disponível")
            exit()

        url_base = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
        url_recurso = 'CotacaoDolarDia(dataCotacao=@dataCotacao)?'
        url_param = f'@dataCotacao=%27{data_base}%27&$format=json'
        query_url = f"{url_base}{url_recurso}{url_param}"
        acesso = APIBancoCentral(query_url)
        req = acesso.getURL()
        if req.status_code != 200:
            logger.info("Erro na conexão")
            exit()
        else:
            resp = req.content.decode("utf-8")
            self.json_string = json.loads(resp)

            if len(self.json_string["value"]) == 0:
                logger.info("Não tem cotações disponíveis nesta data")
                exit()
            self.cotation = True

    def dolar_compra_ptax(self):
        return self.json_string["value"][0]["cotacaoCompra"]

    def dolar_venda_ptax(self):
        return self.json_string["value"][0]["cotacaoVenda"]

    def dolar_ultimacotacao(self):
        return self.json_string["value"][0]["dataHoraCotacao"]


if __name__ == "__main__":
    cotacao = Cotacao()
    print(cotacao.dolar_compra_ptax())
    print(cotacao.dolar_venda_ptax())
    print(cotacao.dolar_ultimacotacao())
