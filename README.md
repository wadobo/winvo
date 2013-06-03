# WInvo

WInvo (Wadobo Invoices) is a simple python script to manage legal invoices
using a repository like git and generate final PDF invoices to send to the
client and to print.

## WInvo file format

Each invoice is a .conf file with the invoice information like:

```
    [General]
    type: hours
    lang: es
    number: 1

    to: Fake Company Name S.L.<br/>
        CIF: XXXXXXXXX<br/>
        Fake address<br/>
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
    address: No es magia es Wadobo S.L.L.<br/>
        CIF: B90032236<br/>
        C/Arqueros nº 4, Local<br/>
        41011, Sevilla, España<br/>
        info@wadobo.com

    # this will be added to the invoice at the bottom
    payment: Forma de pago: Transferencia bancaria<br/>
        Número de cuenta corriente: XXXX XXXX XX XXXXXXXXXX<br/>
        Entidad: Bank

    # now or a date string like 'April 3th 2013'
    date: now
    dateformat: %d de %B de %Y
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
