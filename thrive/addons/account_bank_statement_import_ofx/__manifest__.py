# -*- coding: utf-8 -*-
# Part of Thrive Bureau ERP. See LICENSE file for full copyright and licensing details.

{
    'name': 'Import OFX Bank Statement',
    'category': 'Accounting/Accounting',
    'version': '1.0',
    'depends': ['account_bank_statement_import'],
    'description': """
Module to import OFX bank statements.
======================================

This module allows you to import the machine readable OFX Files in Thrive: they are parsed and stored in human readable format in
Accounting \ Bank and Cash \ Bank Statements.

Bank Statements may be generated containing a subset of the OFX information (only those transaction lines that are required for the
creation of the Financial Accounting records).
    """,
    'data': [
    ],
    'installable': True,
    'auto_install': True,
    'license': 'OEEL-1',
}