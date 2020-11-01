#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from datetime import date
import enum

from workalendar.america.brazil import BrazilSaoPauloCity
import requests


class ModosDeConsulta(enum.Enum):
    PorDia = 1
    PorPeriodo = 2
    Error = 3


class BancoCentralException(BaseException):
    pass


class Dolar:
    def __init__(self, mode: ModosDeConsulta, data: date = None, periodo: dict = None):
        if (mode == ModosDeConsulta.PorDia):
            if self.is_weekday(data):
                raise BancoCentralException('Sábado e Domingo não há cotações')
            if self.is_holiday(data):
                raise BancoCentralException('Feriados não há cotações')
            self.setUrl(_mode=mode, _data=data)
        elif (mode == ModosDeConsulta.PorPeriodo):
            self.setUrl(_mode=mode, _periodo=periodo)
        else:
            raise BancoCentralException('Tipo de consulta inválida')

        req = self.getURL()
        if req.status_code != 200:
            raise BancoCentralException('Erro na conexão')

        resp = req.content.decode("utf-8")
        self.json_string = json.loads(resp)

    def setUrl(self, _mode: ModosDeConsulta, _data: date = None, _periodo: dict = None):
        self.URL_BASE = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/'

        if (_mode == ModosDeConsulta.PorDia):
            d = _data.strftime('%m-%d-%Y')
            self.URL_RESOURCE = 'CotacaoDolarDia(dataCotacao=@dataCotacao)?'
            self.URL_PARAM = f'@dataCotacao=%27{d}%27&$format=json'
        elif (_mode == ModosDeConsulta.PorPeriodo):
            i = _periodo["inicio"].strftime('%m-%d-%Y')
            f = _periodo["final"].strftime('%m-%d-%Y')
            self.URL_RESOURCE = 'CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?'
            self.URL_PARAM = f'@dataInicial=%27{i}%27&@dataFinalCotacao=%27{f}%27&$top=100&$format=json'
        else:
            return None

        self.URL = f'{self.URL_BASE}{self.URL_RESOURCE}{self.URL_PARAM}'

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

    def is_holiday(self, day):
        cal = BrazilSaoPauloCity()
        if cal.is_working_day(day):
            return False
        return True

    def is_weekday(self, day):
        if date.weekday(day) in [5, 6]:  # 5=saturday or 6=sunday
            return True
        return False

    def dolar_compra_ptax(self):
        return self.json_string["value"][0]["cotacaoCompra"]

    def dolar_venda_ptax(self):
        return self.json_string["value"][0]["cotacaoVenda"]

    def dolar_ultimacotacao(self):
        return self.json_string["value"][0]["dataHoraCotacao"]
