#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
from dolar import Dolar, ModosDeConsulta


day = date(2020, 10, 2)
periodo = {
    "inicio": date(2020, 9, 28),
    "final": date(2020, 10, 2)
}

cotacao = Dolar(mode=ModosDeConsulta.PorDia, data=day)
# cotacao = Dolar(mode=ModosDeConsulta.PorPeriodo, periodo=periodo)

print(f'Compra PTAX: {cotacao.dolar_compra_ptax()}')
print(f'Venda PTAX: {cotacao.dolar_venda_ptax()}')
print(f'Data Cotação: {cotacao.dolar_ultimacotacao()}')
