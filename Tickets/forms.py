from django import forms


class CheckoutForm(forms.Form):
    NameOnCard = forms.CharField(label='Name on Card', max_length= 50)
    CCN = forms.CharField(label='Credit Card Number', max_length=16)
    CCED = forms.DateField(label='Credit Card Expiration Date')
    CCCVV = forms.CharField(label='Credit Card CVV', max_length=16)
    BAddress = forms.CharField(label='Billing Address', max_length=250)
    BCity = forms.CharField(label='Billing City', max_length=25)
    BState = forms.CharField(label='Billing State', max_length=2)
    BZip = forms.CharField(label='Billing Zip', max_length=5)
    ShipName = forms.CharField(label='Name to Ship too', max_length=50)
    ShipAddress = forms.CharField(label='Shipping Address', max_length=250)
    ShipCity = forms.CharField(label='Shipping City', max_length=25)
    ShipState = forms.CharField(label='Shipping State', max_length=2)
    ShipZip = forms.CharField(label='Shipping Zip', max_length=5)

