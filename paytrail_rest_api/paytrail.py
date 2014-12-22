# -*- coding: utf-8 -*-
__author__ = 'Abradox'

import requests
import hashlib
import json

from paytrail_rest_api.exceptions import PaytrailException


class PaytrailRestUrlset(object):
    """
    Urlset object describes all return urls used with the service
    """
    success_url = ''
    failure_url = ''
    notification_url = ''
    pending_url = ''

    def __init__(self, success_url, failure_url, notification_url, pending_url=None):
        super(PaytrailRestUrlset, self).__init__()
        self.success_url = success_url
        self.failure_url = failure_url
        self.notification_url = notification_url
        self.pending_url = pending_url


class PaytrailRestContact(object):
    """
    Contact data structure holds information about payment actor.
    This information is saved with the payment and is available
    with the payment in merchant's panel.
    """

    first_name = ''
    last_name = ''
    email = ''
    addr_street = ''
    addr_postal_code = ''
    addr_postal_office = ''
    addr_country = ''
    tel_no = ''
    cell_no = ''
    company = ''

    def __init__(self, first_name, last_name, email, addr_street, addr_postal_code, addr_postal_office, addr_country,
             tel_no='', cell_no='', company=''):
        """
        Contructor for Contact data structure. Contact holds information
        about the user paying the payment.

        @param string first_name
        @param string last_name
        @param string email
        @param string addr_street
        @param string addr_zip
        @param string addr_city
        @param string addr_country
        @param string tel_no
        @param string cell_no
        @param string company
        """

        super(PaytrailRestContact, self).__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.addr_street = addr_street
        self.addr_postal_code = addr_postal_code
        self.addr_postal_office = addr_postal_office
        self.addr_country = addr_country
        self.tel_no = tel_no
        self.cell_no = cell_no
        self.company = company


class PaytrailRestProduct(object):
    """
    Product object acts as a payment products. There is one product object
    for each product row. Product objects are automatically generated when
    payment function addProduct is called. You never need to directly work
    with product objects.
    """

    TYPE_NORMAL = 1
    TYPE_POSTAL = 2
    TYPE_HANDLING = 3

    title = ''
    code = ''
    amount = None
    price = None
    vat = None
    discount = None
    product_type = None

    def __init__(self, title, code, amount, price, vat, discount, product_type):
        """
        @param string title
        @param string code
        @param float amount
        @param float price
        @param flaot vat
        @param float discount
        @param int product_type
        """
        super(PaytrailRestProduct, self).__init__()

        self.title = title
        self.code = code
        self.amount = amount
        self.price = price
        self.vat = vat
        self.discount = discount
        self.product_type = product_type


class PaytrailRestResult(object):
    """
    This object is returned when a payment is processed to Paytrail
    It allows you to query for token or URL
    """

    _token = ''
    _url = ''

    def __init__(self, token, url):
        super(PaytrailRestResult, self).__init__()
        self._token = token
        self._url = url

    def get_token(self):
        return self._token

    def get_url(self):
        return self._url


class PaytrailRestPaymentBase(object):
    _order_number = ''
    _urlset = ''
    _reference_number = ''
    _description = ''
    _currency = 'EUR'
    _locale = 'fi_FI'

    def __init__(self, order_number, urlset):
        super(PaytrailRestPaymentBase, self).__init__()
        self._order_number = order_number
        self._urlset = urlset

    def get_order_number(self):
        """
        @return string order number for this payment
        """
        return self._order_number

    def get_urlset(self):
        """
        @return PaytrailE1Urlset payment return url object for this payment
        """
        return self._urlset

    def set_custom_reference_number(self, reference_number):
        """
        You can set a reference number for a payment but it is *not* recommended.

        Reference number set using this function will only be used for interface payments.
        Interface payment means a payment done with such a payment method that is used
        with own contract (using Paytrail only as a technical API). If payment is made
        with payment method that is used directly with Paytrail contract, this value
        is not used - instead Paytrail uses auto generated reference number.

        Using custom reference number may be useful if you need to automatically confirm
        payments paid directly to your own account with your own contract. With custom
        reference number you can match payments with it.

        @param referenceNumber Customer reference number
        """
        self._reference_number = reference_number

    def get_custom_reference_number(self):
        """
        @return string Custom reference number attached to this payment
        """
        return self._reference_number

    def set_locale(self, locale):
        """
        Change used locale. Locale affects language and number and date presentation formats.

        Paytrail supports currently three locales: Finnish (fi_FI), English (en_US)
        and Swedish (sv_SE). Default locale is fi_FI.

        @param string locale
        """

        if locale not in ('fi_F', 'en_US', 'sv_SE'):
            raise PaytrailException('Given locale is unsupported: %r .' % locale)

        self._locale = locale

    def get_locale(self):
        """
        @return string Locale attached to this payment
        """

        return self._locale

    def set_currency(self, currency):
        """
        Set non-default currency. Currently the default currency (EUR) is only supported value.

        @param currency Currency in which product prices are given
        """

        if currency != 'EUR' and currency != 'SEK':
            raise PaytrailException('Currently EUR and SEK are the only supported currency.')

        self._currency = currency

    def get_currency(self):
        """
        @return string Currency attached to this payment
        """
        return self._currency

    def set_description(self, description):
        """
        You may optionally set description for the payment. This message
        will only be visible in merchant's panel with the payment - nowhere else.
        It allows you to save additional data with payment when necessary.

        @param string description Private payment description
        """

        self._description = description

    def get_description(self):
        """
        @return string Description attached to this payment
        """
        return self._description

    def get_json_data(self):
        """
        Get payment data as array

        @return array REST API compatible payment data
        @throws Paytrail_Exception
        """
        raise PaytrailException('PaytrailRestPayment is not meant to be used directly. Use E1 or S1 module instead.')


class PaytrailRestPaymentS1(PaytrailRestPaymentBase):

    _price = None

    def __init__(self, order_number, urlset, price):
        super(PaytrailRestPaymentS1, self).__init__(order_number, urlset)
        self._price = price

    def get_price(self):
        return self._price

    def get_json_data(self):
        """
        Get payment data as array

        @return array REST API compatible payment data
        @throws Paytrail_Exception
        """

        data = {
            "orderNumber": self.get_order_number(),
            "referenceNumber": self.get_custom_reference_number(),
            "description": self.get_description(),
            "currency": self.get_currency(),
            "locale": self.get_locale(),
            "urlSet": {
                "success": self.get_urlset().success_url,
                "failure": self.get_urlset().failure_url,
                "pending": self.get_urlset().pending_url,
                "notification": self.get_urlset().notification_url,
                },
            "price": self.get_price(),
        }

        return data


class PaytrailRestPaymentE1(PaytrailRestPaymentBase):
    """
    Payment object represents the actual payment to be transmitted
    to Paytrail interface

    E1 references to Paytrail interface version E1, which
    is extended and recommended version.
    """

    _contact = None
    _products = []
    _include_vat = 1

    def __init__(self, order_number, urlset, contact):
        super(PaytrailRestPaymentE1, self).__init__(order_number, urlset)

        self._order_number = order_number
        self._contact = contact
        self._urlset = urlset

    def add_product(self, title, no, amount, price, tax, discount, product_type = 1):
        """
        Use this function to add each order product to payment.

        Please group same products using $amount. Paytrail
        supports up to 500 product rows in a single payment.

        @param string $title
        @param string $no
        @param float $amount
        @param float $price
        @param float $tax
        @param flaot $discount
        @param int $type
        """
        if len(self._products) >= 500:
            raise PaytrailException('Paytrail can only handle up to 500 different product rows. '
                                    'Please group products using product amount.')

        self._products = PaytrailRestProduct(title, no, amount, price, tax, discount, product_type)

    def get_contact(self):
        """
        @return PaytrailE1Contact contact data for this payment
        """
        return self._contact

    def get_products(self):
        """
        @return array List of PaytrailE1Product objects for this payment
        """
        return self._products

    def set_vat_mode(self, mode):
        """
        You can decide whether you wish to use taxless prices (mode=0) or
        prices which include taxes. Default mode is 1 (taxes are in prices).

        You should always use the same mode that your web shop uses - otherwise
        you will get problems with rounding since SV supports prices with only
        2 decimals.

        @param int $mode
        """
        self._include_vat = mode

    def get_vat_mode(self):
        """
        @return int Vat mode attached to this payment
        """
        return self._include_vat

    def get_json_data(self):
        """
        Get payment data as array

        @return array REST API compatible payment data
        @throws Paytrail_Exception
        """

        data = {
            "orderNumber": self.get_order_number(),
            "referenceNumber": self.get_custom_reference_number(),
            "description": self.get_description(),
            "currency": self.get_currency(),
            "locale": self.get_locale(),
            "urlSet": {
                "success": self.get_urlset().success_url,
                "failure": self.get_urlset().failure_url,
                "pending": self.get_urlset().pending_url,
                "notification": self.get_urlset().notification_url,
            },
            "orderDetails": {
                "includeVat": self.get_vat_mode(),
                "contact": {
                    "telephone": self.get_contact().tel_no,
                    "mobile": self.get_contact().cell_no,
                    "email": self.get_contact().email,
                    "firstName": self.get_contact().first_name,
                    "lastName": self.get_contact().last_name,
                    "companyName": self.get_contact().company,
                    "address": {
                        "street": self.get_contact().addr_street,
                        "postalCode": self.get_contact().addr_postal_code,
                        "postalOffice": self.get_contact().addr_postal_office,
                        "country": self.get_contact().addr_country,
                    },
                },
                "products": {},
            },
        }

        for product in self.get_products():
            data["orderDetails"]["products"] = {
                "title": product.title,
                "code": product.code,
                "amount": product.amount,
                "price": product.price,
                "vat": product.vat,
                "discount": product.discount,
                "type": product.product_type
            }

        return data


class PaytrailRest(object):
    """
    Main module
    """

    _merchantId = ''
    _merchantSecret = ''
    _serviceUrl = ''

    def __init__(self, merchant_id, merchant_secret, service_url='https://payment.paytrail.com'):
        """
        Initialize module with your own merchant id and merchant secret.

        While building and testing integration, you can use demo values
        (merchantId = 13466, merchantSecret = ...)

        @param int merchantId
        @param string merchantSecret
        """
        super(PaytrailRest, self).__init__()
        self._merchant_id = merchant_id
        self._merchant_secret = merchant_secret
        self._service_url = service_url
        self.session = requests.Session()
        self.session.auth = (merchant_id, merchant_secret)
        self.session.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Verkkomaksut-Api-Version': '1'
        }

    def get_version(self):
        """
        @return Module version as a string
        """
        return '1.0'

    def process_payment(self, payment):
        """
        Get url for payment

        @param Paytrail_Module_E1_Payment $payment
        @throws Paytrail_Exception
        @return Paytrail_Module_E1_Result
        """

        url = self._service_url + '/token/json'

        data = payment.get_json_data()

        # Create data array
        url = self._service_url + '/api-payment/create'

        result = self._post_json_request(url, data)

        if result.status_code != requests.codes.created:
            data = json.loads(result.content)
            raise PaytrailException(
                code=data['errorCode'],
                message=data['errorMessage']
            )

        data = json.loads(result.content)

        if not data:
            raise PaytrailException(result.response, 'unknown-error')

        return PaytrailRestResult(data['token'], data['url'])


    def confirm_payment(self, order_number, time_stamp, paid, method, auth_code):
        """
        This function can be used to validate parameters returned by return and notify requests.
        Parameters must be validated in order to avoid hacking of payment confirmation.
        This function is usually used like:

        $module = new Paytrail_Module_E1($merchantId, $merchantSecret);
        if ($module->validateNotifyParams($_GET["ORDER_NUMBER"], $_GET["TIMESTAMP"], $_GET["PAID"], $_GET["METHOD"], $_GET["AUTHCODE"])) {
          // Valid notification, confirm payment
        } else {
          // Invalid notification, possibly someone is trying to hack it. Do nothing or create an alert.
        }

        @param string order_number
        @param int time_stamp
        @param string paid
        @param int method
        @param string auth_code
        """
        base = '|'.join((order_number, time_stamp, paid, method, self._merchant_secret,))
        _hash = hashlib.md5(base).hexdigest().upper()
        return auth_code == _hash

    def _post_json_request(self, url, content):
        """
        This method submits given parameters to given url as a post request without
        using curl extension. This should require minimum extensions

        @param $url
        @param $params
        @throws PaytrailException
        """

        result = self.session.post(url, data=json.dumps(content))

        return result
