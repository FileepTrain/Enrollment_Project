import decimal

from mongoengine import *
import datetime


class PriceChange(EmbeddedDocument):
    """
    Each time the status changes for an order, another instance of this class is
    added to the list of status changes for that order.  They will always be
    appended to the end of the list, and never deleted, so that makes it pretty
    easy to manage the list of status changes.
    """
    newPrice = Decimal128Field(db_field='new_price', min_value=.01, precision=2, required=True)
    priceChangeDate = DateTimeField(db_field='price_change_date', required=True)

    def __init__(self, newPrice: decimal, priceChangeDate: datetime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.newPrice = newPrice
        self.priceChangeDate = priceChangeDate

    def __str__(self):
        return f'Price Change Entry: New status: {self.newPrice}, on date: {self.priceChangeDate}'
