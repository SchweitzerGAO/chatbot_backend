from __future__ import annotations
import logging
import os
import glob
import shutil
from typing import Any, Dict, List, Optional, Text

from rasa.engine.graph import ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage

from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message

from rasa.shared.nlu.training_data.training_data import TrainingData

import spacy_pkuseg as pkuseg


# tokenizer = HanLPClient('https://www.hanlp.com/api', auth=auth, language='zh')  # auth不填则匿名，zh中文，mul多语种

tokenizer = pkuseg.pkuseg()
logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=True
)
class PKUTokenizer(Tokenizer):
    @staticmethod
    def supported_languages() -> Optional[List[Text]]:
        """Supported languages (see parent class for full docstring)."""
        return ["zh"]

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns default config (see parent class for full docstring)."""
        return {
            # default don't load custom dictionary
            "dictionary_path": None,
            # Flag to check whether to split intent
            "intent_tokenization_flag": False,
            # Symbol on which intent should be split
            "intent_split_symbol": "_",
            # Regular expression to detect tokens
            "token_pattern": None,
        }

    def __init__(
            self,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
    ) -> None:
        super().__init__(config)
        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> PKUTokenizer:
        """Creates a new component (see parent class for full docstring)."""
        # Path to the dictionaries on the local filesystem.
        return cls(config, model_storage, resource)

    @classmethod
    def required_packages(cls) -> List[Text]:
        return ["spacy_pkuseg"]

    def train(self, training_data: TrainingData) -> Resource:
        """Copies the dictionary to the model storage."""
        self.persist()
        return self._resource

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)

        tokenized = tokenizer.cut(text)
        # tokenized = tokenizer.tokenize(text, coarse=True)
        # tokenized = sum(tokenized, [])
        tokens = []
        start = 0
        for word in tokenized:
            tokens.append(Token(word, start))
            start += len(word)

        return self._apply_token_pattern(tokens)

    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            **kwargs: Any,
    ) -> PKUTokenizer:
        """Loads a custom dictionary from model storage."""
        return cls(config, model_storage, resource)

    @staticmethod
    def _copy_files_dir_to_dir(input_dir: Text, output_dir: Text) -> None:
        # make sure target path exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        target_file_list = glob.glob(f"{input_dir}/*")
        for target_file in target_file_list:
            shutil.copy2(target_file, output_dir)

    def persist(self) -> None:
        """Persist the custom dictionaries."""
        dictionary_path = self._config["dictionary_path"]
        if dictionary_path is not None:
            with self._model_storage.write_to(self._resource) as resource_directory:
                self._copy_files_dir_to_dir(dictionary_path, str(resource_directory))
