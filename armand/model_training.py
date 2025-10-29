import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

class ML_Model_Builder:
	def __init__(self, dataset: pd.DataFrame, target: pd.DataFrame, random_state:int = 42):
		self.__model = None
		self.random_state = random_state
		
		# First split: Separate the test set from the rest
		x_train_val, test_x, y_train_val, test_y = train_test_split(
			dataset, target,
			test_size=0.2,
			random_state=self.random_state,
			stratify=target
		)

		# Second split: Separate the training and validation sets
		train_x, val_x, train_y, val_y = train_test_split(
			x_train_val, y_train_val,
			test_size=0.25, # 25% of 80 = 20
			random_state=self.random_state,
			stratify=y_train_val
		)

		self.__data_train_x = train_x
		self.__target_train_y = train_y

		self.__data_test_x = test_x
		self.__target_test_y = test_y

		self.__data_val_x = val_x
		self.__target_val_y = val_y
	
	def setModel(self, model = "decision_tree"):
		if (model == "decision_tree"):
			self.__model = "decision_tree"
		else:
			raise Exception('no valid model selected')
		
		return self
	
	def build(self):
		if self.__data_train_x is None or self.__target_train_y is None:
			error = f"training data is not loaded is x_train valid:{self.__data_train_x==None} is y_train valid:{self.__target_train_y==None}"
			raise Exception(error)
		
		if self.__data_test_x is None or self.__target_test_y is None:
			error = f"testdata is not loaded, is x_test valid:{self.__data_test_x==None}, is y_test valid:{self.__target_test_y==None}"
			raise Exception(error)
		
		if self.__data_val_x is None or self.__target_val_y is None:
			error = f"validationdata is not loaded, is x_val valid:{self.__data_val_x==None}, is y_val valid:{self.__target_val_y==None}"
			raise Exception(error)
		
		if self.__model == None:
			raise Exception(f"no model is set")
		elif self.__model == "decision_tree":		
			return Decision_Tree_Model(self.__data_train_x, self.__target_train_y, self.__data_val_x, self.__target_val_y, self.__data_test_x, self.__target_test_y)
		else:
			raise Exception(f"invalid or not supported model is set")

class Decision_Tree_Model:
	def __init__(self, x_train, y_train, x_test, y_test, x_val, y_val, random_state = 42):
		self.__x_train = x_train
		self.__y_train = y_train
		self.__x_test = x_test
		self.__y_test = y_test
		self.__x_val = x_val
		self.__y_val = y_val
		self.__random_state = random_state

	def setRandomstate(self, random_state=42):
		self.__random_state = random_state
		return self

	def train(self):
		self.__model = DecisionTreeClassifier(random_state=self.__random_state)
		self.__model.fit(self.__x_train, self.__y_train)
		return self	
	
	def getTestPrediction(self):
		y_pred_test = self.__model.predict(self.__x_test)
		return accuracy_score(self.__y_test, y_pred_test)
	
	def getValidationPrediction(self):
		y_pred_val = self.__model.predict(self.__x_val)
		return accuracy_score(self.__y_val, y_pred_val)