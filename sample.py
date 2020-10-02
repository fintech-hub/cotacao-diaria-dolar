#!/usr/bin/python
# -*- coding: utf-8 -*-

from dolar import Cotacao

cotacao = Cotacao()
print(cotacao.dolar_compra_ptax())
print(cotacao.dolar_venda_ptax())
print(cotacao.dolar_ultimacotacao())
