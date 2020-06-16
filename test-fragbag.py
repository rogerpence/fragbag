import unittest, os
import newfragbag as fb

def get_template():
    contents = fb.get_template(os.path.join('tw', 'form-field-jinja2.html'))
    return contents

class TestFragBag(unittest.TestCase):
    def test_get_template_tokens(self):
        contents = get_template()
        self.assertIsNotNone(contents)
        # print(contents)

        tokens = fb.get_template_tokens(contents)
        self.assertEqual(len(tokens),  4)
        self.assertEqual(tokens[0],  'field_name')
        self.assertEqual(tokens[1],  'label')
        self.assertEqual(tokens[2],  "field_type('text', true)")
        self.assertEqual(tokens[3],  'placeholder')

        # ['field_name', 'label', "field_type('text', true)", 'placeholder']




if __name__ == '__main__':
    unittest.main()