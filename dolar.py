#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import logging
from datetime import date

import requests

logger = logging.getLogger(__name__)


class Dolar:
    def __init__(self, TODAY):
        self.TODAY = TODAY
        self.CURRENT_DATE = self.TODAY.strftime('%d-%m-%Y')
        self.URL_BASE = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'
        self.URL_RESOURCE = 'CotacaoDolarDia(dataCotacao=@dataCotacao)?'
        self.URL_PARAM = f'@dataCotacao=%27{self.CURRENT_DATE}%27&$format=json'
        self.URL = f'{self.URL_BASE}{self.URL_RESOURCE}{self.URL_PARAM}'

        if self.is_weekday():
            logger.info("Sábado ou Domingo sem cotação disponível")
            return None

        req = self.getURL()
        if req.status_code != 200:
            logger.info("Erro na conexão")
            return None

        resp = req.content.decode("utf-8")
        self.json_string = json.loads(resp)

        if len(self.json_string["value"]) == 0:
            logger.info("Não tem cotações disponíveis nesta data")
            return None

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

        return requests.get(self.URL, headers=headers, timeout=None)

    def is_weekday(self):
        if date.weekday(self.TODAY) in [5, 6]:  # 5=saturday or 6=sunday
            return True
        return False

    def dolar_compra_ptax(self):
        return self.json_string["value"][0]["cotacaoCompra"]

    def dolar_venda_ptax(self):
        return self.json_string["value"][0]["cotacaoVenda"]

    def dolar_ultimacotacao(self):
        return self.json_string["value"][0]["dataHoraCotacao"]
