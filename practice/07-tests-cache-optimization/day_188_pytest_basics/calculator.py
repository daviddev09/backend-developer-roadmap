def validate_price_and_quantity(price: int, quantity: int):
    if price == 0 or quantity < 1:
        raise ValueError
    
    return True
    

def validate_promo_code(promo_code: str):
    
    if len(promo_code) != 6:
        raise ValueError
    
    for n in promo_code:
        if type(int(n)) != int:
            raise ValueError
        
    return True


def calculate_discount(price: int|float, discount_percent: int|float):

    return price - (price * (discount_percent / 100))