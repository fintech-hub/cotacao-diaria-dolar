#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from datetime import date

from dolar import (
    Dolar,
    ModosDeConsulta,
    BancoCentralException
)


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

    def test_dolar_compra_ptax_weekend(self):
        TODAY = date(2020, 11, 1)
        with self.assertRaises(BancoCentralException) as context:
            Dolar(
                mode=ModosDeConsulta.PorDia,
                data=TODAY
            )
        self.assertTrue('Sábado e Domingo não há cotações' in str(context.exception))

    def test_dolar_compra_ptax_holiday(self):
        TODAY = date(2020, 11, 2)
        with self.assertRaises(BancoCentralException) as context:
            Dolar(
                mode=ModosDeConsulta.PorDia,
                data=TODAY
            )
        self.assertTrue('Feriados não há cotações' in str(context.exception))

    def test_mode_errors(self):
        TODAY = date(2020, 10, 31)
        with self.assertRaises(BancoCentralException) as context:
            Dolar(
                mode=ModosDeConsulta.Error,
                data=TODAY
            )
        self.assertTrue('Tipo de consulta inválida' in str(context.exception))

    def test_dolar_compra_maior_zero(self):
        self.assertTrue(self.cotacaoDia.dolar_compra_ptax() > 0)
        self.assertTrue(self.cotacaoPeriodo.dolar_compra_ptax() > 0)

    def test_dolar_venda_ptax(self):
        self.assertIsNotNone(self.cotacaoDia.dolar_venda_ptax())
        self.assertIsNotNone(self.cotacaoPeriodo.dolar_venda_ptax())

    def test_dolar_venda_ptax_maior_zero(self):
        self.assertTrue(self.cotacaoDia.dolar_venda_ptax() > 0)
        self.assertTrue(self.cotacaoPeriodo.dolar_venda_ptax() > 0)

    def test_ultimacotacao_exist(self):
        self.assertIsNotNone(self.cotacaoDia.dolar_ultimacotacao())
        self.assertIsNotNone(self.cotacaoPeriodo.dolar_ultimacotacao())

    def test_is_holiday_tiradentes(self):
        TODAY = date(2020, 4, 21)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_holiday_independencia(self):
        TODAY = date(2020, 9, 7)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_holiday_aparecida(self):
        TODAY = date(2020, 10, 12)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_holiday_finados(self):
        TODAY = date(2020, 11, 2)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_holiday_republica(self):
        TODAY = date(2020, 11, 15)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_holiday_trabalho(self):
        TODAY = date(2020, 5, 1)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_holiday_saopaulo(self):
        TODAY = date(2020, 1, 25)
        self.assertTrue(self.cotacaoDia.is_holiday(TODAY))

    def test_is_not_weekday(self):
        TODAY = date(2020, 10, 1)
        self.assertFalse(self.cotacaoDia.is_weekday(TODAY))

    def test_is_weekday(self):
        TODAY = date(2020, 10, 3)
        self.assertTrue(self.cotacaoDia.is_weekday(TODAY))


if __name__ == '__main__':
    unittest.main()
