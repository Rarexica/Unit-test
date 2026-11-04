import unittest

from code_sales import ( # 
    parse_transactions,
    extract_columns,
    calculate_total_sales,
    split_thread_colors,
    color_count,
    daily_sales,
)


class TestParseTransactions(unittest.TestCase):

    def test_number_of_transactions(self):
        transactions = parse_transactions(daily_sales)
        self.assertEqual(len(transactions), 100)

    def test_each_transaction_has_4_fields(self):
        transactions = parse_transactions(daily_sales)
        for transaction in transactions:
            self.assertEqual(len(transaction), 4)

    def test_data_is_cleaned(self):
        transactions = parse_transactions(daily_sales)
        # The first transaction should not contain leading/trailing whitespace
        self.assertEqual(transactions[0][0], "Edith Mcbride")
        self.assertEqual(transactions[0][1], "$1.21")
        self.assertEqual(transactions[0][2], "white")
        self.assertEqual(transactions[0][3], "09/15/17")

    def test_last_transaction(self):
        transactions = parse_transactions(daily_sales)
        self.assertEqual(transactions[-1][0], "Myrtle Morris")


class TestExtractColumns(unittest.TestCase):

    def test_lists_have_equal_length(self):
        transactions = parse_transactions(daily_sales)
        customers, sales, thread_sold = extract_columns(transactions)
        self.assertEqual(len(customers), len(sales))
        self.assertEqual(len(sales), len(thread_sold))
        self.assertEqual(len(customers), 100)


class TestCalculateTotalSales(unittest.TestCase):

    def test_total_sales(self):
        transactions = parse_transactions(daily_sales)
        _, sales, _ = extract_columns(transactions)
        # assertAlmostEqual avoids floating point precision issues
        self.assertAlmostEqual(calculate_total_sales(sales), 1498.74, places=2)

    def test_small_controlled_value(self):
        self.assertEqual(calculate_total_sales(["$1.50", "$2.50"]), 4.0)


class TestThreadColors(unittest.TestCase):

    def test_total_number_of_threads(self):
        transactions = parse_transactions(daily_sales)
        _, _, thread_sold = extract_columns(transactions)
        self.assertEqual(len(split_thread_colors(thread_sold)), 181)

    def test_split_on_ampersand(self):
        self.assertEqual(split_thread_colors(["white&blue", "red"]), ["white", "blue", "red"])

    def test_color_count_controlled(self):
        colors = ["red", "white", "red", "blue"]
        self.assertEqual(color_count("red", colors), 2)
        self.assertEqual(color_count("green", colors), 0)

    def test_real_color_counts(self):
        transactions = parse_transactions(daily_sales)
        _, _, thread_sold = extract_columns(transactions)
        colors = split_thread_colors(thread_sold)
        expected = {
            "red": 24, "yellow": 34, "green": 30,
            "white": 28, "black": 26, "blue": 22, "purple": 17,
        }
        for color, count in expected.items():
            self.assertEqual(color_count(color, colors), count, msg=f"color: {color}")


if __name__ == "__main__":
    unittest.main()