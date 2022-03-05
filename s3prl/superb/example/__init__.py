from s3prl.task import UtteranceClassification as Task
from s3prl.nn import MeanPoolingLinear as DownstreamModel

from s3prl.dataset import UtteranceClassificationDataset as TrainDataset
ValidDataset = TrainDataset
TestDataset = TrainDataset

from s3prl.preprocessor import ExampleUtteranceClassificationPreprocessor as Preprocessor
