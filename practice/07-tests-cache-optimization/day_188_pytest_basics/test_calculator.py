import pytest
from calculator import (
    validate_price_and_quantity,
    validate_promo_code,
    calculate_discount
)

def test_validation_price_and_quantity():
    # Arrange
    true_price = 1
    false_price = 0
    quantity = 1

    # Act/Assert
    with pytest.raises(ValueError):
        validate_price_and_quantity(false_price, quantity)

    result = validate_price_and_quantity(true_price, quantity)

    assert result == True


def test_validation_promo_code():
    # Arrange
    true_promo_code = '123456'
    false_promo_code = '1234S6'
    false_len_promo_code = '12345'

    # Act/Assert
    with pytest.raises(ValueError):
        validate_promo_code(false_len_promo_code)
    
    with pytest.raises(ValueError):
        validate_promo_code(false_promo_code)

    result = validate_promo_code(true_promo_code)

    assert result == True


def test_calculate_discount():
    #Arrange
    price = 100
    discount = 10

    # Act
    result = calculate_discount(price, discount)
    
    # Assert
    assert result == 90.0