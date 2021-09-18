"""
Unit testing of mami.py and vectorizing.py with unittest
"""
import unittest
import mami
import vectorizing
import numpy as np # for testing vectorizing


class TestLowerBound(unittest.TestCase):
    def test_lowerbounds(self):
        """
        Tests mami.find_lower_bound on 3 examples (4&6, 3&6, and 4&4 pegs&colors)
        """
        tests = [{'pair': [256, 4], 'result': 5}, 
                  {'pair': [63, 3], 'result': 4}, 
                  {'pair': [46, 4], 'result': 4}]
        for i in range(len(tests)):
            with self.subTest(i=i):
                self.assertEqual(mami.find_lower_bound(*tests[i]['pair']),tests[i]['result'])

class TestRandomCodes(unittest.TestCase):
    def setUp(self):
        self.randomcode = mami.make_code()

    def test_is_list(self):
        """
        Check that the returned random code is a list (test in default values)
        """
        self.assertEqual(type(self.randomcode),list, 'Code not a list')
    def test_are_ints(self):
        """
        Check that the returned random code contains non-negative integers (test on default values)
        """
        for peg in self.randomcode:
            self.assertEqual(type(peg),int, 'Color not integer')
            self.assertTrue(peg >= 0, 'Negative number for color')
    def test_number_of_pegs(self):
        """
        Check that the returned random code has the correct number of entries (pegs)
        """
        test_dims = [[4, 6], [5, 7], [1, 1]]
        for test_dim in test_dims:
            self.assertEqual(len(mami.make_code(*test_dim)),test_dim[0], 'Wrong number of pegs in code')
    def test_number_of_colors(self):
        """
        Check that the returned random code has the correct number of colors
        """
        test_dims = [[4, 6], [5, 7], [1, 1]]
        for test_dim in test_dims:
            self.assertTrue(max(mami.make_code(*test_dim)) < test_dim[1], 'Too high color number in code')

class TestCalculateKey(unittest.TestCase):
    def test_valid_key(self):
        """
        Check the calculated key is a valid key - 10 times on random code and guess in standard game
        """
        dim = [4,6]
        for times in range(10):
            key = mami.calculate_key(mami.make_code(*dim),mami.make_code(*dim))
            self.assertEqual(type(key[0]),int)
            self.assertEqual(type(key[1]),int)
            self.assertFalse(key[0]==dim[0]-1 and key[1]==1)
            self.assertTrue(key[0]+key[1]<=dim[0])
            self.assertTrue(key[0]>=0)
            self.assertTrue(key[1]>=0)

    def test_symmetry(self):
        """
        Check that calculated key is symmetric in code/guess - 2x5 times on random code and guess in 2 dims
        """
        dims = [[2,3], [4,6]]
        for dim in dims:
            for times in range(5):
                code = mami.make_code(*dim)
                guess = mami.make_code(*dim)
                self.assertEqual(mami.calculate_key(code,guess),mami.calculate_key(guess,code))
            
    def test_key_correct(self):
        """
        Check calculated key on examples
        """
        code = [0, 0, 1, 2]
        guess = [1, 1, 0, 2]
        key = (1, 2)
        self.assertEqual(mami.calculate_key(code, guess), key)

class TestPossibleKeys(unittest.TestCase):
    def setUp(self):
        self.pegs = 4
        self.colors = 6
        self.possible_keys = mami.make_possible_keys(self.pegs, self.colors)
        self.length = (self.pegs+1)*(self.pegs+2)/2 - 1
    def test_number_of_keys(self):
        self.assertEqual(len(self.possible_keys), self.length)
        
    def test_is_tuple_list(self):
        self.assertEqual(type(self.possible_keys), list)
        for key in self.possible_keys:
            self.assertEqual(type(key), tuple)
            
    def test_are_valid(self):
        for key in self.possible_keys:
            self.assertEqual(type(key[0]),int)
            self.assertEqual(type(key[1]),int)
            self.assertFalse(key[0]==self.pegs-1 and key[1]==1)
            self.assertTrue(key[0]+key[1]<=self.pegs)
            self.assertTrue(key[0]>=0)
            self.assertTrue(key[1]>=0)

class TestFullSamplespace(unittest.TestCase):
    def setUp(self):
        self.pegs = 4
        self.colors = 6
        self.length = self.colors ** self.pegs
        self.full_samplespace = mami.make_full_samplespace(self.pegs, self.colors)
    def test_number_of_codes(self):
        self.assertEqual(len(self.full_samplespace),self.length)

class TestVectorizationTranslations(unittest.TestCase):
    def setUp(self):
        self.vectorized = np.array([[[1, 0], [0, 0], [0, 1]],[[0, 0], [1, 1], [0, 0]]])
        self.original = np.array([[[0, 2]],[[1, 1]]])
        self.colors = 3

    def test_translate_from_vect(self):
        self.assertTrue((vectorizing.translate_from_vectorization(self.vectorized) == self.original).all())

    def test_translate_to_vect(self):
        self.assertTrue((vectorizing.translate_to_vectorization(self.original, colors=self.colors) == self.vectorized).all())
        # self.assertEqual(vectorizing.translate_to_vectorization(self.original, colors=self.colors), self.vectorized)
        # self.assertTrue((vectorizing.translate_to_vectorization(self.original, colors=self.colors) == self.vectorized))

    def test_number_to_vectorization(self):
        number = 22
        self.assertEqual(number,
                         vectorizing.vectorized_code_to_number(vectorizing.number_to_vectorized_code(number)))

class TestCalculateKey(unittest.TestCase):
    def setUp(self):
        self.codes = np.array([[[1, 0], [0, 0], [0, 1]],
                               [[0, 0], [1, 1], [0, 0]]])
        self.guesses = np.array([[[1, 0], [0, 1], [0, 0]],
                                 [[0, 1], [1, 0], [0, 0]]])
        self.black = np.array([[1, 0],
                               [1, 1]])
        self.white = np.array([[0, 1],
                               [0, 0]])
        self.allcodes = vectorizing.make_possible_codes()
        self.code = np.array([[0, 0, 1, 2]]) # blue, blue, red, green
        self.guess = np.array([[1, 1, 0, 2]]) # red, red, blue, green
        self.code_vectorized = np.array([[1, 1, 0, 0],
                                         [0, 0, 1, 0],
                                         [0, 0, 0, 1],
                                         [0, 0, 0, 0],
                                         [0, 0, 0, 0],
                                         [0, 0, 0, 0]])
        self.guess_vectorized = np.array([[0, 0, 1, 0],
                                          [1, 1, 0, 0],
                                          [0, 0, 0, 1],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0],
                                          [0, 0, 0, 0]])
        self.code_number = 468
        self.guess_number = 439
        self.key = 1 + 2*(4+1) # 1 black, 2 white
        self.key_tuple = (1, 2)
        
    def test_recover_key(self):
        self.assertEqual(self.key_tuple, vectorizing.recover_key(self.key))

    def test_calculate_key_singular(self):
        self.assertEqual(self.key, vectorizing.calculate_key_singular(self.code_vectorized, self.guess_vectorized))
        self.assertEqual(self.key, vectorizing.calculate_key_singular(self.guess_vectorized, self.code_vectorized))

    def test_calculate_key(self):
        self.assertEqual(self.key,
                         vectorizing.calculate_key(self.code_vectorized.reshape(1, 6, 4),
                                                   self.guess_vectorized.reshape(1, 6, 4)))

    def test_make_possible_codes_shape(self):
        self.assertEqual(self.allcodes.shape, (6**4, 6, 4))

    def test_all_keys_example(self):
        self.assertEqual(self.key,
                         vectorizing.calculate_key(self.allcodes, self.allcodes)[self.code_number, self.guess_number])

    def test_code_to_number(self):
        self.assertEqual(vectorizing.code_to_number(self.code), self.code_number)
        self.assertEqual(vectorizing.code_to_number(self.guess), self.guess_number)

    def test_vectorized_code_to_code(self):
        self.assertTrue((vectorizing.vectorized_code_to_code(self.code_vectorized) == self.code).all())
        self.assertTrue((vectorizing.vectorized_code_to_code(self.guess_vectorized) == self.guess).all())

    def test_calculate_key_black(self):
        self.assertTrue((vectorizing.calculate_key_black(self.codes, self.guesses) == self.black).all(), "Wrong no. of black")
        self.assertTrue((vectorizing.calculate_key_black(self.codes, self.guesses) == vectorizing.calculate_key_black(self.guesses, self.codes).T).all(), "Not symmetric")

    def test_calculate_key_blackwhite(self):
        self.assertTrue((vectorizing.calculate_key_blackwhite(self.codes, self.guesses) == self.black + self.white).all(), "Wrong no. of black and/or white")
        self.assertTrue((vectorizing.calculate_key_blackwhite(self.codes, self.guesses) == vectorizing.calculate_key_blackwhite(self.guesses, self.codes).T).all(), "Not symmetric")



# class TestVectorizations(unittest.TestCase):
#     def test_format(self):
#         test_code = make_code_vect(4, 6)
#         self.assertTrue((np.sum(test_code, axis = 1, keepdims=True) == np.array([[[1, 1, 1, 1]]])).all())

#     def test_translations(self):
#         test_code = np.array([[[1, 0], [0, 0], [0, 1]],[[0, 0], [1, 1], [0, 0]]])
#         result = np.array([[[0, 2]],[[1, 1]]])
#         self.assertTrue((translation_from_vectorization(test_code)==result).all())

if __name__ == '__main__':
    unittest.main(exit=False)