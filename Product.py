import decimal

from Status import Status
from mongoengine import *
from datetime import datetime
from PriceChange import PriceChange
# from OrderItemProduct import OrderItem


class Product(Document):
    """An agreement between the enterprise and a single customer to exchange for
    a specified quantity of some number of products for an agreed upon price."""
    productCode = StringField(db_field='product_code', max_length=15, required=True)
    productName = StringField(db_field='product_name', max_length=70, required=True)
    productDescription = StringField(db_field='product_description', max_length=800, required=True)
    quantityInStock = IntField(db_field='quantity_in_stock', min_value=0, required=True)
    buyPrice = Decimal128Field(db_field='buy_price', min_value=.01, precision= 2, required=True)
    msrp = Decimal128Field(db_field='msrp', min_value=.01, precision= 2, required=True)
    priceHistory = EmbeddedDocumentListField(PriceChange, db_field='price_history')
    orderItems = ListField(ReferenceField('OrderItem'))

    meta = {'collection': 'products',
            'indexes': [
                {'unique': True, 'fields': ['productCode'], 'name': 'product_uk_01'},
                {'unique': True, 'fields': ['productName'], 'name': 'product_uk_02'}
            ]}

    def change_price(self, new_price: PriceChange):
        """
        Every time the status changes for the order, we add another instance of StatusChange to
        the history list of status changes.
        :param new_status:  An instance of StatusChange representing the latest status change.
        :return:            None
        """
        if self.priceHistory:
            current_price = self.priceHistory[-1]
            if current_price.newPrice == new_price.newPrice:
                raise ValueError('It is already this price.')
            if current_price.priceChangeDate >= new_price.priceChangeDate:
                raise ValueError('New price must be later than the latest price change.')
            if new_price.priceChangeDate > datetime.utcnow():
                raise ValueError('The status change cannot occur in the future.')
            self.priceHistory.append(new_price)
        else:
            self.priceHistory = [new_price]

    def get_current_status(self) -> Status:
        """
        Get the current status of the order.
        :return: The current status of the order.  Note, if there is no status for
        this order, then this method will return a None.
        """
        if self.statusHistory:
            return self.statusHistory[-1].status
        else:
            return None

    def __init__(self, productCode: str, productName: str, productDescription: str, quantityInStock: int, buyPrice: decimal, msrp: decimal, *args, **values):
        super().__init__(*args, **values)
        if self.orderItems is None:
            self.orderItems = []  # initialize to no items in the order, yet.
        self.productCode = productCode
        self.productName = productName
        self.productDescription = productDescription
        self.quantityInStock = quantityInStock
        self.quantityInStock = quantityInStock
        self.buyPrice = buyPrice
        self.msrp = msrp

    def __str__(self):
        """
        Returns a string representation of the Order instance.
        :return: A string representation of the Order instance.
        """
        return f'Product Code: {self.productCode} Name: {self.productName}, Description: {self.quantityInStock}, Quantity In Stock: {self.quantityInStock}, Price: {self.buyPrice}, MSRP: {self.msrp}'
    def add_item(self, item):
        """
        Adds an item to the Order.  Note that the item argument is an instance of the
        OrderItem class, and as such has both the product that is ordered and
        the quantity.  We cannot have more than one OrderItem for any Order for the
        same product.
        :param item:    An instance of OrderItem class to be added to this Order.  If
        an OrderItem    this Product is already in the order, this call is ignored.
        :return:    None
        """
        for already_ordered_item in self.orderItems:
            if item.equals(already_ordered_item):
                return  # Already in the order, don't add it.
        self.orderItems.append(item)
        # There is no need to update the OrderItem to point to this Order because the
        # constructor for OrderItem requires an Order and that constructor calls this
        # method.  Of course, the liability here is that someone could create an instance
        # of OrderItem withOUT using our constructor.  Argh.

    def remove_item(self, item):
        """
        Removes a Product from the order.  Note that the item argument is an instance of the
        OrderItem class, but we ignore the quantity.
        :param item:    An instance of the OrderItem class that includes the Product that
                        we are removing from the order.  If this Product is not already in
                        the order, the call is ignored.
        :return:        None
        """
        for already_ordered_item in self.orderItems:
            # Check to see whether this next order item is the one that they want to delete
            if item.equals(already_ordered_item):
                # They matched on the Product, so they match.  For the remove_item use
                # case, it doesn't really matter what quantity is called for.  I only used
                # an instance of OrderItem here to be consistent with add_item.
                self.orderItems.remove(already_ordered_item)
                # At this point, the OrderItem object should be deleted since there is
                # no longer a reference to it from Order.
                #                already_ordered_item.delete()
                return