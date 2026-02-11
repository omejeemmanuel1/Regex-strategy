import unittest
from parser import parse_invoice_line, parse_invoice_text

class TestParser(unittest.TestCase):

    def test_parse_total_price_qty(self):
        # Sugar – Rs. 6,000 (50 kg)
        line = "Sugar – Rs. 6,000 (50 kg)"
        expected = {
            "product_name": "Sugar",
            "quantity": 50.0,
            "unit": "kg",
            "price": 6000.0,
            "unit_price": 120.0,
        }
        self.assertEqual(parse_invoice_line(line), expected)

        line = "Rice - Rs. 1,200 (10.5 kg)"
        expected = {
            "product_name": "Rice",
            "quantity": 10.5,
            "unit": "kg",
            "price": 1200.0,
            "unit_price": 114.28571428571429,
        }
        self.assertEqual(parse_invoice_line(line), expected)

    def test_parse_qty_at_price(self):
        # Wheat Flour (10kg @ 950)
        line = "Wheat Flour (10kg @ 950)"
        expected = {
            "product_name": "Wheat Flour",
            "quantity": 10.0,
            "unit": "kg",
            "price": 9500.0,
            "unit_price": 950.0,
        }
        self.assertEqual(parse_invoice_line(line), expected)

        line = "Milk (2L @ 150.50)"
        expected = {
            "product_name": "Milk",
            "quantity": 2.0,
            "unit": "L",
            "price": 301.0,
            "unit_price": 150.50,
        }
        self.assertEqual(parse_invoice_line(line), expected)

    def test_parse_qty_price_per_unit(self):
        # Cooking Oil: Qty 5 bottles Price 1200/bottle
        line = "Cooking Oil: Qty 5 bottles Price 1200/bottle"
        expected = {
            "product_name": "Cooking Oil",
            "quantity": 5.0,
            "unit": "bottles",
            "price": 6000.0,
            "unit_price": 1200.0,
        }
        self.assertEqual(parse_invoice_line(line), expected)

        line = "Juice: Qty 3 pcs Price 250/pc"
        expected = {
            "product_name": "Juice",
            "quantity": 3.0,
            "unit": "pcs",
            "price": 750.0,
            "unit_price": 250.0,
        }
        self.assertEqual(parse_invoice_line(line), expected)

    def test_parse_name_price(self):
        # Salt - Rs. 100
        line = "Salt - Rs. 100"
        expected = {
            "product_name": "Salt",
            "quantity": 1,
            "unit": "pcs",
            "price": 100.0,
            "unit_price": 100.0,
        }
        self.assertEqual(parse_invoice_line(line), expected)

        line = "Bread Rs. 50"
        expected = {
            "product_name": "Bread",
            "quantity": 1,
            "unit": "pcs",
            "price": 50.0,
            "unit_price": 50.0,
        }
        self.assertEqual(parse_invoice_line(line), expected)

    def test_parse_invoice_text(self):
        example_input = """
Al Noor Traders
Invoice #88912
Sugar – Rs. 6,000 (50 kg)
Wheat Flour (10kg @ 950)
Cooking Oil: Qty 5 bottles Price 1200/bottle
Salt - Rs. 100
Extra Line - Not a product
"""
        expected_output = [
            {
                "product_name": "Sugar",
                "quantity": 50.0,
                "unit": "kg",
                "price": 6000.0,
                "unit_price": 120.0,
            },
            {
                "product_name": "Wheat Flour",
                "quantity": 10.0,
                "unit": "kg",
                "price": 9500.0,
                "unit_price": 950.0,
            },
            {
                "product_name": "Cooking Oil",
                "quantity": 5.0,
                "unit": "bottles",
                "price": 6000.0,
                "unit_price": 1200.0,
            },
            {
                "product_name": "Salt",
                "quantity": 1,
                "unit": "pcs",
                "price": 100.0,
                "unit_price": 100.0,
            },
        ]
        self.assertEqual(parse_invoice_text(example_input), expected_output)

    def test_empty_input(self):
        self.assertEqual(parse_invoice_text(""), [])

    def test_no_product_lines(self):
        input_text = """
Al Noor Traders
Invoice #88912
Some random text
Another random line
"""
        self.assertEqual(parse_invoice_text(input_text), [])

if __name__ == "__main__":
    unittest.main()
