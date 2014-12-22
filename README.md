paytrail-rest-api
=================

Python PayTrail REST api implementation

Example:
  
  views.py:
```python  
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
  
  
  def success(request):
    context = RequestContext(request)
    print('++success++')
    context_dict = {'boldmessage': "I am bold font from the context"}
    paytrail_api = PaytrailRest(merchant_id='13466', merchant_secret='6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ')
    res = paytrail_api.confirm_payment(order_number=request.GET['ORDER_NUMBER'],
                                 time_stamp=request.GET['TIMESTAMP'],
                                 paid=request.GET['PAID'],
                                 method=request.GET['METHOD'],
                                 auth_code=request.GET['RETURN_AUTHCODE']
    )
    context_dict['valid'] = res
    return render_to_response('success.html', context_dict, context)
```
index.html:
```  html
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
```
success.html:
```html
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title></title>
</head>
<body>
<p>Success page</p>
{{ valid }}
</body>
</html>
```

