import unittest
import requests

class ApiTest(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/"
    Product = "Laptop"
    InitialAmount = 15
    BuyAmount = 5
    FinalAmount = InitialAmount - BuyAmount
    BuyPrice = 5200

    def test_1_get_all_products(self):
        r = requests.get(ApiTest.BASE_URL + "AllProducts")
        self.assertEqual(r.status_code, 200)
        #print(r.json())
        self.assertEqual(len(r.json()), 1)

    def test_2_get_check_status(self):
        r = requests.get(f"{ApiTest.BASE_URL}Status/{ApiTest.Product}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['Product'], ApiTest.Product)
        self.assertEqual(r.json()['Amount Available'], ApiTest.InitialAmount)

    def test_3_get_buy_product(self):
        r = requests.get(f'{ApiTest.BASE_URL}Buy/{ApiTest.Product}/{ApiTest.BuyAmount}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['cost'], ApiTest.BuyPrice)
        # Checking status after Buy request
        r = requests.get(f"{ApiTest.BASE_URL}Status/{ApiTest.Product}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['Amount Available'], ApiTest.FinalAmount)



if __name__ == '__main__':
    unittest.main()