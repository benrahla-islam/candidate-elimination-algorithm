import unittest
import pandas as pd
import numpy as np
from main import (
    is_consistent, 
    is_more_general, 
    get_minimal_generalizations, 
    get_minimal_specializations, 
    load_data,
    remove_less_general,  # Add this line
    remove_more_general   # Add this line
)

class TestCandidateElimination(unittest.TestCase):
    
    def test_is_consistent(self):
        # Test with matching examples
        self.assertTrue(is_consistent(['sunny', 'warm', '?'], ['sunny', 'warm', 'normal']))
        
        # Test with wildcard in hypothesis
        self.assertTrue(is_consistent(['?', 'warm', 'normal'], ['sunny', 'warm', 'normal']))
        self.assertTrue(is_consistent(['?', '?', '?'], ['sunny', 'warm', 'normal']))
        
        # Test with wildcard in example (less common but should work)
        self.assertTrue(is_consistent(['sunny', 'warm', 'normal'], ['sunny', '?', 'normal']))
        
        # Test inconsistent examples
        self.assertFalse(is_consistent(['sunny', 'warm', 'normal'], ['rainy', 'warm', 'normal']))
        
        # Test length mismatch
        self.assertFalse(is_consistent(['sunny', 'warm'], ['sunny', 'warm', 'normal']))
    
    def test_is_more_general(self):
        # h1 is more general than h2
        self.assertTrue(is_more_general(['?', 'warm', '?'], ['sunny', 'warm', 'normal']))
        self.assertTrue(is_more_general(['?', '?', '?'], ['sunny', 'warm', 'normal']))
        
        # Same specificity
        self.assertTrue(is_more_general(['sunny', 'warm', 'normal'], ['sunny', 'warm', 'normal']))
        
        # h1 is not more general than h2
        self.assertFalse(is_more_general(['sunny', 'warm', 'normal'], ['?', 'warm', 'normal']))
        self.assertFalse(is_more_general(['sunny', 'warm', 'normal'], ['rainy', 'warm', 'normal']))
        
        # Length mismatch
        self.assertFalse(is_more_general(['sunny', 'warm'], ['sunny', 'warm', 'normal']))
    
    def test_get_minimal_generalizations(self):
        # Test with completely specific hypothesis matching example
        result = get_minimal_generalizations(['sunny', 'warm', 'normal'], ['sunny', 'warm', 'normal'])
        self.assertEqual(len(result), 0)  # Should be empty as no generalization needed
        
        # Test with None hypothesis (most specific boundary initialization)
        result = get_minimal_generalizations([None, None, None], ['sunny', 'warm', 'normal'])
        self.assertEqual(result, [['sunny', 'warm', 'normal']])
        
        # Test with partially initialized hypothesis
        result = get_minimal_generalizations(['sunny', None, 'normal'], ['sunny', 'warm', 'normal'])
        self.assertEqual(result, [['sunny', 'warm', 'normal']])
        
        # Test with conflicting attribute
        result = get_minimal_generalizations(['sunny', 'cold', 'normal'], ['sunny', 'warm', 'normal'])
        self.assertEqual(result, [['sunny', '?', 'normal']])
        
        # Length mismatch
        result = get_minimal_generalizations(['sunny', 'warm'], ['sunny', 'warm', 'normal'])
        self.assertEqual(result, [])
    
    def test_get_minimal_specializations(self):
        # Define unique values for each attribute
        unique_values = [
            ['sunny', 'rainy'],     # For attribute 0
            ['warm', 'cold'],       # For attribute 1
            ['normal', 'high']      # For attribute 2
        ]
        
        # Test 1: Completely general hypothesis ['?', '?', '?']
        # With x = ['sunny', 'warm', 'normal']
        # Expected specializations:
        #   attribute 0: replace '?' with 'rainy' -> ['rainy', '?', '?']
        #   attribute 1: replace '?' with 'cold'   -> ['?', 'cold', '?']
        #   attribute 2: replace '?' with 'high'    -> ['?', '?', 'high']
        result = get_minimal_specializations(['?', '?', '?'], ['sunny', 'warm', 'normal'], unique_values)
        self.assertEqual(len(result), 3)
        self.assertIn(['rainy', '?', '?'], result)
        self.assertIn(['?', 'cold', '?'], result)
        self.assertIn(['?', '?', 'high'], result)
        
        # Test 2: Hypothesis with a mix of specified and general values
        # For h = ['sunny', 'warm', '?'] and x = ['sunny', 'warm', 'high'],
        # index 2 should produce a specialization replacing '?' with 'normal' only.
        result = get_minimal_specializations(['sunny', 'warm', '?'], ['sunny', 'warm', 'high'], unique_values)
        self.assertEqual(result, [['sunny', 'warm', 'normal']])
        
        # Test 3: Length mismatch should return an empty list
        result = get_minimal_specializations(['sunny', 'warm'], ['sunny', 'warm', 'normal'], unique_values)
        self.assertEqual(result, [])
    
    def test_load_data(self):
        # Create a simple test CSV file
        test_df = pd.DataFrame({
            'attr1': ['sunny', 'sunny', 'rainy'],
            'attr2': ['warm', 'cold', 'cold'],
            'class': ['Yes', 'No', 'No']
        })
        test_df.to_csv('test_data.csv', index=False)
        
        # Test loading the data
        df, unique_values, S, G, CONSISTENCY_RULE = load_data('test_data.csv')
        
        # Verify dataframe loaded correctly
        self.assertEqual(len(df), 3)
        
        # Verify unique values extracted correctly
        self.assertTrue(np.array_equal(unique_values[0], ['sunny', 'rainy']) or 
                        np.array_equal(unique_values[0], ['rainy', 'sunny']))
        
        # Verify S and G initialized correctly
        self.assertEqual(S[0], [None, None, None])
        self.assertEqual(G[0], ['?', '?', '?'])
        
        # Verify CONSISTENCY_RULE
        self.assertTrue('?' in CONSISTENCY_RULE)
        self.assertTrue(None in CONSISTENCY_RULE)
        self.assertTrue('sunny' in CONSISTENCY_RULE)
        self.assertEqual(CONSISTENCY_RULE['sunny'], {'sunny'})
        
    def test_remove_less_general(self):
        # Test removing less general hypotheses
        G = [
            ['?', '?', '?'],         # Most general
            ['sunny', '?', '?'],     # Less general than the first
            ['?', 'warm', '?'],      # Less general than the first
            ['sunny', 'warm', '?'],  # Less general than several others
            ['sunny', 'cold', '?']   # Less general than the first and second
        ]
        
        # Create a copy to avoid modifying the original during testing
        G_copy = G.copy()
        remove_less_general(G_copy)
        
        # Only the most general hypothesis should remain
        self.assertEqual(len(G_copy), 1)
        self.assertEqual(G_copy[0], ['?', '?', '?'])
        
        # Test with more complex relationships
        G = [
            ['sunny', '?', '?'],
            ['?', 'warm', '?'],
            ['rainy', '?', '?'],
            ['?', '?', 'normal']
        ]
        
        G_copy = G.copy()
        remove_less_general(G_copy)
        
        # All four should remain as none is more general than the others
        self.assertEqual(len(G_copy), 4)
        self.assertIn(['sunny', '?', '?'], G_copy)
        self.assertIn(['?', 'warm', '?'], G_copy)
        self.assertIn(['rainy', '?', '?'], G_copy)
        self.assertIn(['?', '?', 'normal'], G_copy)

    def test_remove_more_general(self):
        # Test removing more general hypotheses
        S = [
            ['sunny', 'warm', 'normal'],  # Most specific
            ['sunny', '?', 'normal'],     # More general than the first
            ['?', 'warm', 'normal'],      # More general than the first
            ['?', '?', 'normal'],         # More general than several others
            ['sunny', '?', '?']           # More general than the first
        ]
        
        # Create a copy to avoid modifying the original during testing
        S_copy = S.copy()
        remove_more_general(S_copy)
        
        # Only the most specific hypothesis should remain
        self.assertEqual(len(S_copy), 1)
        self.assertEqual(S_copy[0], ['sunny', 'warm', 'normal'])
        
        # Test with more complex relationships
        S = [
            ['sunny', 'warm', 'normal'],
            ['rainy', 'cold', 'high'],
            ['sunny', 'cold', 'normal'],
            ['rainy', 'warm', 'high']
        ]
        
        S_copy = S.copy()
        remove_more_general(S_copy)
        
        # All four should remain as none is more general than the others
        self.assertEqual(len(S_copy), 4)
        self.assertIn(['sunny', 'warm', 'normal'], S_copy)
        self.assertIn(['rainy', 'cold', 'high'], S_copy)
        self.assertIn(['sunny', 'cold', 'normal'], S_copy)
        self.assertIn(['rainy', 'warm', 'high'], S_copy)

if __name__ == '__main__':
    unittest.main()