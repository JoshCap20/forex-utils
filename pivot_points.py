from decimal import Decimal, getcontext, InvalidOperation

getcontext().prec = 10

def calculate_standard_pivot(high: Decimal, low: Decimal, close: Decimal) -> dict[str, Decimal]:
    """Calculate Standard Pivot Points"""
    P = (high + low + close) / 3
    return {
        "P": P,
        "R3": high + 2 * (P - low),
        "R2": P + (high - low),
        "R1": (2 * P) - low,
        "S1": (2 * P) - high,
        "S2": P - (high - low),
        "S3": low - 2 * (high - P)
    }

def calculate_fibonacci_pivot(high: Decimal, low: Decimal, close: Decimal) -> dict[str, Decimal]:
    """Calculate Fibonacci Pivot Points"""
    P = (high + low + close) / 3
    return {
        "P": P,
        "R3": P + ((high - low) * Decimal('1.000')),
        "R2": P + ((high - low) * Decimal('0.618')),
        "R1": P + ((high - low) * Decimal('0.382')),
        "S1": P - ((high - low) * Decimal('0.382')),
        "S2": P - ((high - low) * Decimal('0.618')),
        "S3": P - ((high - low) * Decimal('1.000'))
    }

def calculate_camarilla_pivot(high: Decimal, low: Decimal, close: Decimal) -> dict[str, Decimal]:
    """Calculate Camarilla Pivot Points"""
    return {
        "R4": close + ((high - low) * Decimal('1.1') / 2),
        "R3": close + ((high - low) * Decimal('1.1') / 4),
        "R2": close + ((high - low) * Decimal('1.1') / 6),
        "R1": close + ((high - low) * Decimal('1.1') / 12),
        "S1": close - ((high - low) * Decimal('1.1') / 12),
        "S2": close - ((high - low) * Decimal('1.1') / 6),
        "S3": close - ((high - low) * Decimal('1.1') / 4),
        "S4": close - ((high - low) * Decimal('1.1') / 2)
    }

def calculate_woodies_pivot(high: Decimal, low: Decimal, close: Decimal) -> dict[str, Decimal]:
    """Calculate Woodie's Pivot Points"""
    P = (high + low + (2 * close)) / 4
    return {
        "P": P,
        "R2": P + (high - low),
        "R1": (2 * P) - low,
        "S1": (2 * P) - high,
        "S2": P - (high - low)
    }

def calculate_demarks_pivot(high: Decimal, low: Decimal, close: Decimal, open_price: Decimal) -> dict[str, Decimal]:
    """Calculate DeMark's Pivot Points"""
    x = high + 2 * low + close if close < open_price else 2 * high + low + close if close > open_price else high + low + 2 * close
    return {
        "P": x / 4,
        "R1": x / 2 - low,
        "S1": x / 2 - high
    }

def print_pivot_points(name: str, points: dict[str, Decimal]):
    """Print the calculated pivot points in a formatted manner."""
    print(f"\n{name} Pivot Points:")
    for key, value in points.items():
        print(f"  {key}: {value:.2f}")

def main():
    try:
        high = Decimal(input("Enter the high price: "))
        low = Decimal(input("Enter the low price: "))
        close = Decimal(input("Enter the close price: "))
        open_price = Decimal(input("Enter the open price: "))
        
        print_pivot_points("Standard", calculate_standard_pivot(high, low, close))
        print_pivot_points("Fibonacci", calculate_fibonacci_pivot(high, low, close))
        print_pivot_points("Camarilla", calculate_camarilla_pivot(high, low, close))
        print_pivot_points("Woodie's", calculate_woodies_pivot(high, low, close))
        print_pivot_points("DeMark's", calculate_demarks_pivot(high, low, close, open_price))
    except InvalidOperation as e:
        print(f"Error: {e}\nPlease enter valid decimal numbers for high, low, close, and open prices.")

if __name__ == "__main__":
    main()
