import unittest
import requests

class ApiTest(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5000/"
    BuyAmount = 5

    NewTestProduct = {
        'name': 'TestProduct',
        'amount': 10,
        'price': 100
    }

    NewTestProductUpdated = {
        'name': 'TestProductUpdated',
        'amount': 15,
        'price': 150
    }

    BuyPrice = (NewTestProduct['price'] * 5) + (NewTestProduct['price'] * 5) * 0.30

    def test_1_post_create_product(self):
        r = requests.post(f'{ApiTest.BASE_URL}CreateProduct', json=ApiTest.NewTestProduct)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['name'], ApiTest.NewTestProduct['name'])
        self.assertEqual(r.json()['amount'], ApiTest.NewTestProduct['amount'])
        self.assertEqual(r.json()['price'], ApiTest.NewTestProduct['price'])

    def test_2_get_all_products(self):
        r = requests.get(ApiTest.BASE_URL + "AllProducts")
        self.assertEqual(r.status_code, 200)
        for p in r.json():
            if p['name'] == ApiTest.NewTestProduct['name']:
                self.assertEqual(p['amount'], ApiTest.NewTestProduct['amount'])
                self.assertEqual(p['price'], ApiTest.NewTestProduct['price'])

    def test_3_get_check_status(self):
        r = requests.get(f"{ApiTest.BASE_URL}Status/{ApiTest.NewTestProduct['name']}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['Product'], ApiTest.NewTestProduct['name'])
        self.assertEqual(r.json()['Amount Available'], ApiTest.NewTestProduct['amount'])

    def test_4_get_buy_product(self):
        r = requests.get(f'{ApiTest.BASE_URL}Buy/{ApiTest.NewTestProduct["name"]}/{ApiTest.BuyAmount}')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['cost'], ApiTest.BuyPrice)
        # Checking status after Buy request
        r = requests.get(f"{ApiTest.BASE_URL}Status/{ApiTest.NewTestProduct['name']}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['Amount Available'], ApiTest.NewTestProduct['amount'] - ApiTest.BuyAmount)

    def test_5_post_update_product(self):
        r = requests.post(f'{ApiTest.BASE_URL}ModifyProduct/{ApiTest.NewTestProduct["name"]}', json=ApiTest.NewTestProductUpdated)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['name'], ApiTest.NewTestProductUpdated['name'])
        self.assertEqual(r.json()['amount'], ApiTest.NewTestProductUpdated['amount'])
        self.assertEqual(r.json()['price'], ApiTest.NewTestProductUpdated['price'])

    def test_6_delete_delete_product(self):
        r = requests.delete(f'{ApiTest.BASE_URL}ModifyProduct/{ApiTest.NewTestProductUpdated["name"]}')
        self.assertEqual(r.status_code, 204)


if __name__ == '__main__':
    unittest.main()