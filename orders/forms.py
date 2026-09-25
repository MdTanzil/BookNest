from django import forms


class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('Cash on Delivery', 'Cash on Delivery'),
        ('Online Payment', 'Online Payment (Placeholder)'),
    ]

    shipping_name = forms.CharField(
        max_length=255,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
        }),
    )
    shipping_phone = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your phone number',
        }),
    )
    shipping_address = forms.CharField(
        max_length=255,
        label='Street Address',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your street address',
        }),
    )
    shipping_city = forms.CharField(
        max_length=100,
        label='City',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your city',
        }),
    )
    shipping_postcode = forms.CharField(
        max_length=20,
        label='Postal Code',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your postal code',
        }),
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        label='Payment Method',
        widget=forms.Select(attrs={
            'class': 'form-control',
        }),
    )
    order_note = forms.CharField(
        max_length=500,
        required=False,
        label='Order Note (Optional)',
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Any special instructions for delivery...',
        }),
    )
