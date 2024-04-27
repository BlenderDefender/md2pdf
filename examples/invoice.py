# This file sets the variables required for generating the invoice
import time

def format_amount(amount: int, currency_symbol: str = "€", thousands_separator: str = ".", decimal_separator: str = ","):
    amount_str = str(amount)[:-2]
    decimals = str(amount)[-2:]

    parts = []
    
    for i in range(0, len(amount_str), 3):
        r = len(amount_str) - i
        l = r - 3

        if l < 0:
            l = 0
        
        parts.insert(0, amount_str[l:r])

    return thousands_separator.join(parts) + decimal_separator + decimals + " " + currency_symbol

today = time.time()
in_two_weeks = time.time() + 60 * 60 * 24 * 14


invoice_number = "12345"
account_number = "132 456 789 012"
date_format = "%d. %B %Y"

invoice_information = f"""
Invoice Number: {invoice_number}\\
Date: {time.strftime(date_format, time.localtime(today))}
""".strip()

products = [
    {
        "description": "Website design",
        "price_per_unit": "34.24",
        "units_sold": 42,
        "currency_symbol": "€"
    },
    {
        "description": "Website development",
        "price_per_unit": "45.50",
        "units_sold": 180,
        "currency_symbol": "€"
    },
    {
        "description": "Website integration",
        "price_per_unit": "25.75",
        "units_sold": 16,
        "currency_symbol": "€"
    },
]

product_table = """
| Description | Price | Quantity | Subtotal |
|-------------|-------|----------|----------|
""".strip()

total_due = 0
currency_symbol = "€"

for p in products:
    ppu = int(p.get("price_per_unit", 0).replace(".", "").replace(",", ""))
    subtotal = ppu * p.get("units_sold", 0)
    currency_symbol = p.get("currency_symbol", "€")

    if subtotal == 0:
        continue

    total_due += subtotal

    row = f"""\n|{p.get("description", "")}|{format_amount(ppu, currency_symbol)}|{p.get("units_sold", 0)}|{format_amount(subtotal, currency_symbol)}|"""
    product_table += row


due_information = f"""
| Due by | Account number | Total due |
|--------|----------------|-----------|
| {time.strftime(date_format, time.localtime(in_two_weeks))} | {account_number} | {format_amount(total_due, currency_symbol)} |
""".strip()

