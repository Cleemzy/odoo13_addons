# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
import csv
import base64
from base64 import b64decode

class Alert(models.Model):
    _name = 'invoice_payment.alert'
    _inherit = 'account.move'

    transaction_ids = fields.Many2many('payment.transaction', 'test_alert_mess_transaction_rel', 'test_alert_mess_id', 'transaction_id',
                                       string='Transactions', copy=False, readonly=True)

    def func_send_mess(self, context=None):
        now = date.today()
        query = """
        select id, name, invoice_date_due, amount_residual, amount_total,invoice_origin, (select name from res_partner rp where rp.id = am.partner_id ) client,(select name from res_company rc where rc.id=am.company_id) company
from account_move am where type = 'out_invoice' and state='posted' and invoice_payment_state ='not_paid' and invoice_date_due < DATE '{}' order by write_date desc
        """.format(now)
        self.env.cr.execute(query)
        n_facture = self.env.cr.fetchall()

        with open('/mnt/c/programdata/dockerdata/odoo13entreprise/odoo/addons/invoice_payment_alert/data.csv', 'w', encoding='utf-8') as file:
            fieldnames = [ 'Societe','Facture','Date d\'echeance','Montant du','Montant total','Client', 'Document d\'origine']
            thewriter = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
            thewriter.writeheader()
            for item in n_facture:
                thewriter.writerow({'Societe': item[7], 'Facture' : item[1], 'Date d\'echeance' : item[2], 'Client': item[6],'Montant du' : item[3],'Montant total':item[4], 'Document d\'origine' : item[5]})

        files = base64.b64encode(open('/mnt/c/programdata/dockerdata/odoo13entreprise/odoo/addons/invoice_payment_alert/data.csv','rb').read())

        csv_attachment = self.env['ir.attachment'].create({
            'name' : 'paiement_arrive_echeance_{}.csv'.format(now),
            'datas' : files,
            'store_fname' : files,
            'type' : 'binary',
            'res_model' : self._name,
            'mimetype' : 'text/csv',
        })
        # print(type(self.id))

        # print(self.id)
        self.env['mail.message'].create({
            'email_from' : self.env.user.partner_id.email,
            'author_id' : self.env.user.partner_id.id,
            'body' : "La date d'échéance pour le paiement de ces factures ont été dépassé",
            'model': 'mail.channel',
            'subtype_id' : self.env.ref('mail.mt_comment').id,
            'channel_ids' :  [(4, 24)],
            'res_id' : 24,
            'attachment_ids' : [(4, csv_attachment.id)],
            })
