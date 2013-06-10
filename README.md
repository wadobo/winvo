# WInvo

WInvo (Wadobo Invoices) is a simple python script to manage legal invoices
using a repository like git and generate final PDF invoices to send to the
client and to print.

## Installation

You need to install the python requirements.txt and then generate the
locale with ./genlocale.sh

## Creating an invoice

We have created a handy script to create new invoices, newinv.sh:

```
    $ ./newinv.sh wadobo
    DONE, edit the file ./invoices/201306/wadobo.1/wadobo.1.conf and type ./winvo.py ./invoices/201306/wadobo.1/wadobo.1.conf to generate the pdf in place
```

This command will create a directory and file structure that we have found
useful to us to handle our invoices: the invoices of each month are grouped
inside one directory, then for each invoice there is a subdirectory with
the name "client.\<invoice number\>" which contains the source configuration file
"client.\<invoice number\>.conf" and the pdf when you generate it.

To generate the pdf, invoke the command as explained in the script:


```
    $ ./winvo.py ./invoices/201306/wadobo.1/wadobo.1.conf
    Reading Config
    Generating pdf output
    Bye
```

This will have generated the PDF ./invoices/201306/wadobo.1/wadobo.1.pdf.

You can configure the directory where invoices will be created 
editing a custom_config.sh file like this:

```
   #!/bin/bash

   export INVOICES_DIR="./invoices2"
```

By default, the first invoice will be assigned the invoice no. 1. A
file in $INVOICES_DIR/n will be created with the number "2", indicating
the number for the next invoice. You can modify this file content to
start generating invoices from any invoice number you need.

It's also worth noting that the first time the config file will be a
copy of the default.conf file, but if the script finds a previous
invoice with the same invoicename, it will use it as the source config
file.

## WInvo file format

Each invoice is a .conf file with the invoice information like:

```
    [General]
    type: hours
    lang: es
    number: 1

    to: Fake Company Name S.L.
        CIF: XXXXXXXXX
        Fake address
        41010, Sevilla, España

    currency: Euro
    project: Fake Project
    tax: 21
    taxname: IVA (21%)

    [Fee.1]
    summary: Trabajos realizados de mantenimiento y actualización del software
    fee: 30.00
    hours: 35

    [Fee.2]
    summary: Cambio de estilos
    fee: 30.00
    hours: 5
```

A default.conf file is used to fill common fields like address and so:

```
    [General]
    # logo or none, the logo will be put at the top
    logo: imgs/wadobo.png

    # Your company legal information
    address: No es magia es Wadobo S.L.L.
        CIF: B90032236
        C/Arqueros nº 4, Local
        41011, Sevilla, España
        info@wadobo.com

    # this will be added to the invoice at the bottom
    payment: Forma de pago: Transferencia bancaria
        Número de cuenta corriente: XXXX XXXX XX XXXXXXXXXX
        Entidad: Bank

    # now or a date string like 'April 3th 2013'
    date: now
    dateformat: %d de %B de %Y
    expiry_date: 30  # or 0 If you don't want it
    locale: es_ES.UTF-8

    # type can be hours|total
    type: hours

    # the output lang
    lang: es

    # the invoice currency
    currency: Euro

    # the invoice tax percentage or 0
    tax: 21
    taxname: IVA (21%)
```

# Technical info

WInvo uses reportlab to generate the pdf and it uses python standard
libraries to read .conf files and gettext for translations.

It's a simple script, it can be more configurable, patches are welcome.
