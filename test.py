import unittest
import pandas as pd
from io import StringIO
from main import (
    load_data, is_consistent, is_more_general, get_minimal_generalizations,
    get_minimal_specializations, remove_less_general, remove_more_general
)

class TestCandidateElimination(unittest.TestCase):
    def setUp(self):
        csv_data = """Outlook,Temperature,Humidity,Wind,Play
Sunny,Hot,High,Weak,No
Sunny,Hot,High,Strong,No
Overcast,Hot,High,Weak,Yes
Rain,Mild,High,Weak,Yes
Rain,Cool,Normal,Weak,Yes"""
        self.df = pd.read_csv(StringIO(csv_data))
        self.unique_values = [self.df[column].unique().tolist() for column in self.df.columns]
        self.S0 = [None] * (len(self.unique_values)-1)
        self.G0 = ['?'] * (len(self.unique_values)-1)
    
    def test_load_data(self):
        df, unique_values, S, G = load_data(StringIO("""Outlook,Temperature,Humidity,Wind,Play\nSunny,Hot,High,Weak,No\n"""))
        self.assertEqual(len(df), 1)
        self.assertEqual(unique_values[0], ['Sunny'])
        self.assertEqual(S, [[None, None, None, None]])
        self.assertEqual(G, [['?', '?', '?', '?']])
    
    def test_is_consistent(self):
        self.assertTrue(is_consistent(['Sunny', '?', 'High', 'Weak'], ['Sunny', 'Hot', 'High', 'Weak']))
        self.assertFalse(is_consistent(['Sunny', 'Hot', 'High', 'Weak'], ['Rain', 'Hot', 'High', 'Weak']))
    
    def test_is_more_general(self):
        self.assertTrue(is_more_general(['?', 'Hot', '?', '?'], ['Sunny', 'Hot', '?', '?']))
        self.assertFalse(is_more_general(['Sunny', '?', '?', '?'], ['?', 'Hot', '?', '?']))
    
    def test_get_minimal_generalizations(self):
        result = get_minimal_generalizations(['Sunny', None, 'High', 'Weak'], ['Sunny', 'Hot', 'High', 'Weak'])
        self.assertIn(['Sunny', 'Hot', 'High', 'Weak'], result)
        self.assertNotIn(['?', 'Hot', 'High', 'Weak'], result)
    
    def test_get_minimal_specializations(self):
        result = get_minimal_specializations(['?', 'Hot', '?', '?'], ['Sunny', 'Hot', 'High', 'Weak'], self.unique_values[:-1])
        self.assertIn(['Overcast', 'Hot', '?', '?'], result)
        self.assertIn(['Rain', 'Hot', '?', '?'], result)
    
    def test_remove_less_general(self):
        G = [['?', '?', '?', '?'], ['Sunny', '?', '?', '?']]
        self.assertEqual(remove_less_general(G), [['Sunny', '?', '?', '?']])
    
    def test_remove_more_general(self):
        S = [['Sunny', 'Hot', '?', '?'], ['Sunny', '?', '?', '?']]
        self.assertEqual(remove_more_general(S), [['Sunny', 'Hot', '?', '?']])

if __name__ == '__main__':
    unittest.main()
