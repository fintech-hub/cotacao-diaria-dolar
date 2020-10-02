#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
from dolar import Dolar

TODAY = date(2020, 10, 2)
cotacao = Dolar(TODAY)

print(f'Compra PTAX: {cotacao.dolar_compra_ptax()}')
print(f'Venda PTAX: {cotacao.dolar_venda_ptax()}')
print(f'Data Cotação: {cotacao.dolar_ultimacotacao()}')
