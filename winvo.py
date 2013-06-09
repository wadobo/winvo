#!/usr/bin/env python2

# Copyright (C) 2013 Daniel Garcia <danigm@wadobo.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import sys
import locale
import datetime
import argparse
import ConfigParser
import gettext

from reportlab.lib.units import cm
from reportlab.lib import utils
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle,
                                Paragraph, Image, Spacer)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT


# Fake gettext
def _(text):
    return text


DEFAULT = 'default.conf'


def get_image(path, width=3*cm):
    path = path.encode('utf8')
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def genPDF(output, config):
    type = config.get('General', 'type')
    img = config.get('General', 'logo')
    address = config.get('General', 'address')
    date = config.get('General', 'date')
    dateformat = config.get('General', 'dateformat')
    expiry_date = int(config.get('General', 'expiry_date'))
    local = config.get('General', 'locale')
    to = config.get('General', 'to')
    number = config.get('General', 'number')
    project = config.get('General', 'project')
    payment = config.get('General', 'payment')
    tax = int(config.get('General', 'tax'))
    taxname = config.get('General', 'taxname')
    currency = config.get('General', 'currency')
    lang = config.get('General', 'lang')

    # Jumps for multiple lines fields
    address = address.replace('\n', '<br/>')
    to = to.replace('\n', '<br/>')
    payment = payment.replace('\n', '<br/>')

    locale.setlocale(locale.LC_ALL, local)

    x = gettext.translation('winvo', 'mo', languages=[lang])
    _ = x.gettext

    filename = output

    w, h = A4
    margin = 1*cm
    styleC = ParagraphStyle(name="centerdStyle", alignment=TA_CENTER)
    styleL = ParagraphStyle(name="leftStyle", alignment=TA_LEFT)
    styleR = ParagraphStyle(name="rightStyle", alignment=TA_RIGHT)

    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=0.8*cm,
                            leftMargin=margin, rightMargin=margin)
    elements = []

    if img != 'none':
        logo = get_image(img, width=6.0*cm)
        logo.hAlign = 'LEFT'
        elements.append(logo)
        elements.append(Spacer(5*cm, 0.4*cm))

    address = Paragraph(address, styleR)
    if date == 'now':
        d = datetime.datetime.now()
        date = d.strftime(dateformat)
    if expiry_date:
        expiry_date = d + datetime.timedelta(days=expiry_date)
        expiry_date = expiry_date.strftime(dateformat)
        expiry_date = ': '.join(['Expiration date', expiry_date])
        expiry_date = Paragraph(expiry_date, styleR)
    date = Paragraph(date, styleR)
    to = Paragraph(to, styleL)
    number = Paragraph(_('Invoice n. %s') % number, styleL)
    project = Paragraph(u'<b>%s</b>' % project, styleC)
    payment = Paragraph(payment, styleL)

    N = -4 if tax else -3

    # invoice Table
    tstyle_list = [
        ('BOX', (0, 0), (-1, N - 1), 0.25, colors.black),
        ('BOX', (0, N + 1), (-1, -1), 0.25, colors.black),
        ('INNERGRID', (0, 0), (-1, N), 0.25, colors.black),
        # Table header
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(0.85, 0.85, 0.85)),
        ('SPAN', (0, N), (-1, N)),
        ('LINEBELOW', (0, N + 1), (-1, N + 1), 0.25, colors.black),
        ('LINEBELOW', (0, N + 2), (-1, N + 2), 0.25, colors.black),
        ('BACKGROUND', (0, N + 1), (-1, N + 2),
         colors.Color(0.80, 1.00, 0.80)),
        ('BACKGROUND', (0, -1), (-1, -1),
         colors.Color(0.64, 1.00, 0.64)),
    ]
    if type == 'hours':
        tstyle_list.append(('SPAN', (0, N + 1), (2, N + 1)))
        tstyle_list.append(('SPAN', (0, N + 2), (2, N + 2)))
        tstyle_list.append(('SPAN', (0, -1), (2, -1)))

    tstyle = TableStyle(tstyle_list)
    data = []
    if type == 'total':
        head = [_('Activity'), _('Amount (%s)') % currency]
        colwidths = ['*', 3.2*cm]
    else:
        head = [_('Activity'), _('Rate/Hour'),
                _('Count'), _('Amount (%s)') % currency]
        colwidths = ['*', 2*cm, 2*cm, 3.2*cm]
    data.append(head)

    subtotal = 0
    for section in [i for i in config.sections() if i.startswith('Fee')]:
        element = [Paragraph(config.get(section, 'summary'), styleL)]
        if type == 'total':
            fee = config.get(section, 'fee')
            subtotal += float(fee)
            element.append(Paragraph(fee, styleR))
        else:
            fee = config.get(section, 'fee')
            hours = config.get(section, 'hours')
            total = float(fee) * float(hours)
            subtotal += float(total)
            element.append(Paragraph(fee, styleR))
            element.append(Paragraph(hours, styleR))
            element.append(Paragraph("%5.2f" % total, styleR))

        data.append(element)

    if type == 'total':
        data.append([""]*2)
    else:
        data.append([""]*4)

    # Subtotal
    element = []
    element.append(Paragraph(_('Subtotal'), styleL))
    if type == 'total':
        element.append(Paragraph('%5.2f' % subtotal, styleR))
    else:
        element.append("")
        element.append("")
        element.append(Paragraph('%5.2f' % subtotal, styleR))
    data.append(element)

    # Taxes
    if tax:
        element = []
        tax = subtotal * (tax / 100.0)
        element.append(Paragraph(taxname, styleL))
        if type == 'total':
            element.append(Paragraph('%5.2f' % tax, styleR))
        else:
            element.append("")
            element.append("")
            element.append(Paragraph('%5.2f' % tax, styleR))
        data.append(element)

    # total
    total = subtotal + tax
    element = []
    element.append(Paragraph(_('Total'), styleL))
    if type == 'total':
        element.append(Paragraph('%5.2f' % total, styleR))
    else:
        element.append("")
        element.append("")
        element.append(Paragraph('%5.2f' % total, styleR))
    data.append(element)

    t = Table(data, colWidths=colwidths)
    t.setStyle(tstyle)

    elements.append(address)
    elements.append(Spacer(5*cm, 0.4*cm))
    elements.append(date)
    if expiry_date:
        elements.append(expiry_date)
    elements.append(Spacer(5*cm, 1.5*cm))
    elements.append(to)
    elements.append(Spacer(5*cm, 1.5*cm))
    elements.append(number)
    elements.append(Spacer(5*cm, 0.8*cm))
    elements.append(project)
    elements.append(Spacer(5*cm, 0.4*cm))
    elements.append(t)
    elements.append(Spacer(5*cm, 1.5*cm))
    elements.append(payment)

    doc.build(elements)


def read_config(conf):
    parser = ConfigParser.ConfigParser()
    parser.read([DEFAULT, conf])
    return parser


def interactive():
    print "NOT IMPLEMENTED YET"


def main():
    parser = argparse.ArgumentParser(description='Generates invoices')
    parser.add_argument('conf', metavar='conf', type=str,
                        help='The config to generate the invoice')

    args = parser.parse_args()
    conf = args.conf
    if not conf:
        conf = interactive()
        sys.exit(0)

    print "Reading Config"
    config = read_config(conf)
    print "Generating pdf output"
    output = '.'.join(conf.split('.')[0:-1] + ['pdf'])
    genPDF(output, config)
    print "Bye"


if __name__ == '__main__':
    main()
