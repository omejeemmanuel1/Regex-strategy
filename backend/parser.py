import re
from typing import List, Dict, Union

def parse_invoice_line(line: str) -> Union[Dict, None]:
    line = line.strip()
    if not line:
        return None

    m1 = re.match(r"^(.*?)\s*[\-\–]\s*Rs\.\s*([\d,]+)\s*\(([\d\.]+)\s*(\w+)\)$", line)
    if m1:
        product_name = m1.group(1).strip()
        price = float(m1.group(2).replace(",", ""))
        quantity = float(m1.group(3))
        unit = m1.group(4)
        return {
            "product_name": product_name,
            "quantity": quantity,
            "unit": unit,
            "price": price,
            "unit_price": price / quantity if quantity > 0 else 0
        }

    m2 = re.match(r"^(.*?)\s*\(([\d\.]+)\s*(\w+)\s*@\s*([\d\.,]+)\)$", line)
    if m2:
        product_name = m2.group(1).strip()
        quantity = float(m2.group(2))
        unit = m2.group(3)
        unit_price = float(m2.group(4).replace(",", ""))
        price = quantity * unit_price
        return {
            "product_name": product_name,
            "quantity": quantity,
            "unit": unit,
            "price": price,
            "unit_price": unit_price
        }

    m3 = re.match(r"^(.*?):\s*Qty\s*([\d\.]+)\s*(\w+)\s*Price\s*([\d\.,]+)/(\w+)$", line)
    if m3:
        product_name = m3.group(1).strip()
        quantity = float(m3.group(2))
        unit = m3.group(3)
        unit_price = float(m3.group(4).replace(",", ""))
        price = quantity * unit_price
        return {
            "product_name": product_name,
            "quantity": quantity,
            "unit": unit,
            "price": price,
            "unit_price": unit_price
        }

    m4 = re.match(r"^(.*?)\s*(?:[\-\–]?)\s*Rs\.\s*([\d,]+)$", line)
    if m4:
        product_name = m4.group(1).strip()
        price = float(m4.group(2).replace(",", ""))
        return {
            "product_name": product_name,
            "quantity": 1.0,
            "unit": "pcs",
            "price": price,
            "unit_price": price
        }


    m5 = re.match(r"^(Invoice\s*#?\s*(\d+)|[A-Za-z\s]+Traders|[A-Za-z\s]+Store)$", line, re.IGNORECASE)
    if m5:
        return {
            "product_name": line.strip(),
            "quantity": 0,
            "unit": "header",
            "price": 0.0,
            "unit_price": 0.0
        }

    return None

def parse_invoice_text(text: str) -> List[Dict]:
    items = []
    lines = text.strip().split("\n")
    for line in lines:
        parsed = parse_invoice_line(line)
        if parsed:
            items.append(parsed)
    return items
