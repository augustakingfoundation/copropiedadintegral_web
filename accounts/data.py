from django.utils.translation import ugettext as _


DOCUMENT_TYPE_CC = 100
DOCUMENT_TYPE_CE = 110
DOCUMENT_TYPE_PASSPORT = 120
DOCUMENT_IDENTITY_CARD = 130

DOCUMENT_TYPE_CHOICES = (
    ('', _('Tipo de documento')),
    (DOCUMENT_TYPE_CC, 'C.C.'),
    (DOCUMENT_TYPE_CE, 'C.E.'),
    (DOCUMENT_TYPE_PASSPORT, _('Pasaporte')),
    (DOCUMENT_IDENTITY_CARD, _('Tarjeta de identidad')),
)
