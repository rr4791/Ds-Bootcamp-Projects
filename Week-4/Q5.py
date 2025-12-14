import pandas as pd
from Q5_list_products_ordered import list_products

def main():
    products = pd.DataFrame({
        "product_id": [1, 2, 3, 4, 5],
        "product_name": [
            "Leetcode Solutions",
            "Jewels of Stringology",
            "HP",
            "Lenovo",
            "Leetcode Kit"
        ],
        "product_category": ["Book", "Book", "Laptop", "Laptop", "T-shirt"]
    })

    orders = pd.DataFrame({
        "product_id": [1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5],
        "order_date": [
            "2020-02-05", "2020-02-10",
            "2020-01-18", "2020-02-11",
            "2020-02-17", "2020-02-24",
            "2020-03-01", "2020-03-04", "2020-03-04",
            "2020-02-25", "2020-02-27"
        ],
        "unit": [60, 70, 30, 80, 2, 3, 20, 30, 60, 50, 50]
    })

    result = list_products(products, orders)
    print(result)

if __name__ == "__main__":
    main()
