#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta
import logging

import requests
import json

logger = logging.getLogger(__name__)

TODAY = date.today() + timedelta(days=2)
CURRENT_DATE = TODAY.strftime('%d-%m-%Y')
URL_BASE = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
URL_RESOURCE = 'CotacaoDolarDia(dataCotacao=@dataCotacao)?'
URL_PARAM = f'@dataCotacao=%27{CURRENT_DATE}%27&$format=json'
URL = f'{URL_BASE}{URL_RESOURCE}{URL_PARAM}'


class Dolar:
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

        # Testa 10 vezes a resposta da api
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
    def __init__(self):

        if self.is_weekend():
            logger.info("Sábado ou Domingo sem cotação disponível")
            exit()

        acesso = Dolar(URL)
        req = acesso.getURL()
        if req.status_code != 200:
            logger.info("Erro na conexão")
            exit()

        resp = req.content.decode("utf-8")
        self.json_string = json.loads(resp)

        if len(self.json_string["value"]) == 0:
            logger.info("Não tem cotações disponíveis nesta data")
            exit()

    def is_weekend(self):
        if date.weekday(TODAY) in [5, 6]:  # 5=saturday or 6=sunday
            return True

    def dolar_compra_ptax(self):
        return self.json_string["value"][0]["cotacaoCompra"]

    def dolar_venda_ptax(self):
        return self.json_string["value"][0]["cotacaoVenda"]

    def dolar_ultimacotacao(self):
        return self.json_string["value"][0]["dataHoraCotacao"]
