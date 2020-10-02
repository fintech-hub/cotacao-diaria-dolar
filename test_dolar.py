#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from datetime import date

from dolar import Dolar


class TestCase(unittest.TestCase):

    def setUp(self):
        TODAY = date(2020, 10, 1)
        self.cotacao = Dolar(TODAY)

    def test_dolar_compra_ptax(self):
        self.assertIsNotNone(self.cotacao.dolar_compra_ptax())

    def test_dolar_compra_maior_zero(self):
        self.assertTrue(self.cotacao.dolar_compra_ptax() > 0)

    def test_dolar_venda_ptax(self):
        self.assertIsNotNone(self.cotacao.dolar_venda_ptax())

    def test_dolar_venda_ptax_maior_zero(self):
        self.assertTrue(self.cotacao.dolar_venda_ptax() > 0)

    def test_ultimacotacao_exist(self):
        self.assertIsNotNone(self.cotacao.dolar_ultimacotacao())

    def test_is_not_weekday(self):
        self.assertFalse(self.cotacao.is_weekday())

    def test_is_weekday(self):
        TODAY = date(2020, 10, 3)
        self.cotacao = Dolar(TODAY)
        self.assertTrue(self.cotacao.is_weekday())


if __name__ == '__main__':
    unittest.main()
