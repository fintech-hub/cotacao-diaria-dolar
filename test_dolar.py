#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
import unittest
from dolar import Dolar, ModosDeConsulta


class TestCase(unittest.TestCase):

    def setUp(self):
        TODAY = date(2020, 10, 1)
        periodo = {
            "inicio": date(2020, 9, 28),
            "final": date(2020, 10, 2)
        }
        self.cotacaoDia = Dolar(mode=ModosDeConsulta.PorDia, data=TODAY)
        self.cotacaoPeriodo = Dolar(mode=ModosDeConsulta.PorPeriodo, periodo=periodo)

    def test_dolar_compra_ptax(self):
        self.assertIsNotNone(self.cotacaoDia.dolar_compra_ptax())
        self.assertIsNotNone(self.cotacaoPeriodo.dolar_compra_ptax())

    def test_dolar_compra_maior_zero(self):
        self.assertTrue(self.cotacaoDia.dolar_compra_ptax() > 0)
        self.assertTrue(self.cotacaoPeriodo.dolar_compra_ptax() > 0)

    def test_dolar_venda_ptax(self):
        self.assertIsNotNone(self.cotacaoDia.dolar_venda_ptax())
        self.assertIsNotNone(self.cotacaoPeriodo.dolar_venda_ptax())

    def test_dolar_venda_ptax_maior_zero(self):
        self.assertTrue(self.cotacaoDia.dolar_venda_ptax() > 0)
        self.assertTrue(self.cotacaoPeriodo.dolar_venda_ptax() > 0)

    def test_is_not_weekday(self):
        self.assertFalse(self.cotacaoDia.is_weekday())

    def test_is_weekday(self):
        TODAY = date(2020, 10, 3)
        self.cotacaoDia = Dolar(mode=ModosDeConsulta.PorDia, data=TODAY)
        self.assertTrue(self.cotacaoDia.is_weekday())


if __name__ == '__main__':
    unittest.main()
