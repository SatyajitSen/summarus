import unittest

from allennlp.common.util import START_SYMBOL, END_SYMBOL
from allennlp.data.vocabulary import Vocabulary

from summarus.readers import CNNDailyMailReader, RIAReader
from summarus.settings import TEST_URLS_FILE, TEST_STORIES_DIR, RIA_EXAMPLE_FILE


class TestReaders(unittest.TestCase):
    def test_cnn_dailymail_reader(self):
        reader = CNNDailyMailReader(cnn_tokenized_dir=TEST_STORIES_DIR, separate_namespaces=False)
        dataset = reader.read(TEST_URLS_FILE)
        for sample in dataset:
            self.assertEqual(sample.fields["source_tokens"][0].text, START_SYMBOL)
            self.assertEqual(sample.fields["source_tokens"][-1].text, END_SYMBOL)
            self.assertGreater(len(sample.fields["source_tokens"]), 2)

            self.assertEqual(sample.fields["target_tokens"][0].text, START_SYMBOL)
            self.assertEqual(sample.fields["target_tokens"][-1].text, END_SYMBOL)
            self.assertGreater(len(sample.fields["target_tokens"]), 2)

    def test_ria_reader(self):
        reader = RIAReader()
        dataset = reader.read(RIA_EXAMPLE_FILE)
        for sample in dataset:
            self.assertEqual(sample.fields["source_tokens"][0].text, START_SYMBOL)
            self.assertEqual(sample.fields["source_tokens"][-1].text, END_SYMBOL)
            self.assertGreater(len(sample.fields["source_tokens"]), 2)

            self.assertEqual(sample.fields["target_tokens"][0].text, START_SYMBOL)
            self.assertEqual(sample.fields["target_tokens"][-1].text, END_SYMBOL)
            self.assertGreater(len(sample.fields["target_tokens"]), 2)
    
    def test_ria_copy_reader(self):
        reader = RIAReader(separate_namespaces=True, save_copy_fields=True)
        dataset = reader.read(RIA_EXAMPLE_FILE)
        vocabulary = Vocabulary.from_instances(dataset)
        
        for sample in dataset:
            sample.index_fields(vocabulary)
            print(sample.fields["source_tokens"])
            print(sample.fields["target_tokens"])
            print(sample.fields["metadata"].metadata)
            print(sample.fields["source_token_ids"].array)
            print(sample.fields["target_token_ids"].array)
            print(sample.fields["source_to_target"]._mapping_array)
            print(sample.fields["source_to_target"]._target_namespace)
