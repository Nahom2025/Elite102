import unittest
import main
#TODO:fix all of this
class Testmain(unittest.TestCase):
    #u always have to start with test_
    def test_login(self):
        result = main.check_balance('nahom', 'Nahom2025')
        self.assertEqual(result, True)

    def test_create_account(self):
        result = main.create_account('nahom', '17', 'nahomtesfaye2025@gmail.com', 'male', 'Nahom2025')
        self.assertRaises(result, True)

    def test_check_balance(self):
        result = main.check_balance(5)
        self.assertEqual(result, True)

    # def test_modify_account(self):
    

if __name__ == '__main__':
    print('Performing Tests')
    unittest.main
        