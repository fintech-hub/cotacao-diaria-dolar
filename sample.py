#!/usr/bin/python
# -*- coding: utf-8 -*-

from dolar import Cotacao

cotacao = Cotacao()

print(f'Compra PTAX: {cotacao.dolar_compra_ptax()}')
print(f'Venda PTAX: {cotacao.dolar_venda_ptax()}')
print(f'Data Cotação: {cotacao.dolar_ultimacotacao()}')
