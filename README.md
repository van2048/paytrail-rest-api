paytrail-rest-api
=================

Python PayTrail REST api implementation

Example:

views.py:

 def index(request):
    context = RequestContext(request)
    paytrail_urlset = PaytrailRestUrlset(success_url='http://localhost:8000/success',
                                         failure_url='http://localhost:8000/failure',
                                         notification_url='http://localhost:8000/notification'
    )

    payment = PaytrailRestPaymentS1(order_number='1', urlset=paytrail_urlset, price='10.00')

    paytrail_api = PaytrailRest(merchant_id='13466', merchant_secret='6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ')
    result = paytrail_api.process_payment(payment)
    context_dict = {}
    context_dict['result'] = result
    return render_to_response('index.html', context_dict, context)
    
index.html:
  
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<a href="{{ result.get_url }}">Test paytrail</a>

</body>
</html>
