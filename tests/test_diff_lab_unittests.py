import numpy as np
import os
import pandas as pd
import tkinter as tk

from unittest import mock
from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, DESCRIPTION, Extensions


CURRENT_PATH = os.getcwd()


@mock.patch("executables.diff_lab.diff_lab.Differ.show_error", return_value=None)
class DiffLabUnitTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())
		cls.test_file_path = f"{CURRENT_PATH}\\test_data\\unittests\\"

	# Test get_description().

	def test_get_description(self, mock_show_error):
		assert self.differ.get_description() == f"{DESCRIPTION}\n {Extensions.XLSX.value}\n {Extensions.CSV.value}"

	# Test diff_files().

	@mock.patch("executables.diff_lab.diff_lab.Differ.validate_file_names", return_value=(False, None))
	def test_invalid_file_name(self, mock_show_error, mock_validate_file_names):
		assert self.differ.diff_files() is None

	@mock.patch("executables.diff_lab.diff_lab.Differ.validate_file_path", return_value=False)
	def test_invalid_file_path(self, mock_show_error, mock_file_path):
		assert self.differ.diff_files() is None

	# Test validate_file_names().

	def test_missing_file_1_name(self, mock_show_error):
		assert self.differ.validate_file_names(None, "file_2.xlsx") == (False, None)

	def test_missing_file_2_name(self, mock_show_error):
		assert self.differ.validate_file_names("file_1.xlsx", None) == (False, None)

	def test_missing_file_1_extension(self, mock_show_error):
		assert self.differ.validate_file_names("file_1", "file_2.xlsx") == (False, None)

	def test_missing_file_2_extension(self, mock_show_error):
		assert self.differ.validate_file_names("file_1.xlsx", "file_2") == (False, None)

	def test_file_1_extension_not_supported(self, mock_show_error):
		assert self.differ.validate_file_names("file_1.zip", "file_2.xlsx") == (False, None)

	def test_file_2_extension_not_supported(self, mock_show_error):
		assert self.differ.validate_file_names("file_1.xlsx", "file_2.zip") == (False, None)

	def test_files_have_different_extensions(self, mock_show_error):
		assert self.differ.validate_file_names("file_1.xlsx", "file_2.csv") == (False, None)

	def test_valid_file_names(self, mock_show_error):
		assert self.differ.validate_file_names("file_1.xlsx", "file_2.xlsx") == (True, Extensions.XLSX.value)
		assert self.differ.validate_file_names("file_1.csv", "file_2.csv") == (True, Extensions.CSV.value)

	# Test get_file_path().

	def test_get_file_path(self, mock_show_error):
		assert self.differ.get_file_path("file_name.xlsx") == f"{CURRENT_PATH}\\file_name.xlsx"

	# Test validate_file_path().

	def test_file_path_exists(self, mock_show_error):
		assert self.differ.validate_file_path(self.test_file_path + "test_file_path_exists.xlsx")

	def test_file_path_does_not_exist(self, mock_show_error):
		assert not self.differ.validate_file_path(self.test_file_path + "invalid_file_path.xlsx")

	# Test compare_files().

	@mock.patch("executables.diff_lab.diff_lab.Differ.validate_dataframe_structures", return_value=False)
	def test_dataframe_structures_not_valid(self, mock_show_error, mock_validate_dataframe_structures):
		assert self.differ.compare_files("", "", "") is None

	def dataframes_not_equal(self, mock_show_error):
		assert self.differ.compare_files(
			"test_dataframes_are_equal_file_1.xlsx", "test_dataframes_are_equal_file_2.xlsx", Extensions.XLSX.value
		) is None

	# Test open_file_as_dataframe().

	def test_xlsx_extension(self, mock_show_error):
		file_path = self.test_file_path + "test_open_file_as_dataframe.xlsx"
		result = self.differ.open_file_as_dataframe(file_path, Extensions.XLSX.value)

		assert isinstance(result, pd.DataFrame)

	def test_csv_extension(self, mock_show_error):
		file_path = self.test_file_path + "test_open_file_as_dataframe.csv"
		result = self.differ.open_file_as_dataframe(file_path, Extensions.CSV.value)

		assert isinstance(result, pd.DataFrame)

	def test_other_extension(self, mock_show_error):
		assert self.differ.open_file_as_dataframe("", ".zip") is None

	# Test validate_dataframe_structures().

	def test_different_number_of_columns(self, mock_show_error):
		df_1 = pd.DataFrame({0: [1, 2]})
		df_2 = pd.DataFrame({0: [1, 2], 1: [3, 4]})

		assert not self.differ.validate_dataframe_structures(df_1, df_2)

	def test_different_number_of_rows(self, mock_show_error):
		df_1 = pd.DataFrame({0: [1, 2]})
		df_2 = pd.DataFrame({0: [1, 2, 3]})

		assert not self.differ.validate_dataframe_structures(df_1, df_2)

	def test_same_number_of_columns_and_rows(self, mock_show_error):
		df_1 = pd.DataFrame({0: [1, 2], 1: [3, 4]})
		df_2 = pd.DataFrame({0: [1, 2], 1: [3, 4]})

		assert self.differ.validate_dataframe_structures(df_1, df_2)

	# Test get_dataframe_differences().

	def test_get_dataframe_differences(self, mock_show_error):
		df_1 = pd.DataFrame({0: [1, 2, 3, 4], 1: [5, 6, 7, 8], 2: [9, 10, 11, 12], 3: [13, 14, 15, 16]})
		df_2 = pd.DataFrame({0: [1, 20, 3, 4], 1: [5, 6, 70, 80], 2: [90, 10, 11, 12], 3: [130, 14, 15, 160]})
		expected_df_1_differences = pd.DataFrame(
			{
				0: [np.nan, 2, np.nan, np.nan],
				1: [np.nan, np.nan, 7, 8],
				2: [9, np.nan, np.nan, np.nan],
				3: [13, np.nan, np.nan, 16],
			}
		)
		expected_df_2_differences = pd.DataFrame(
			{
				0: [np.nan, 20, np.nan, np.nan],
				1: [np.nan, np.nan, 70, 80],
				2: [90, np.nan, np.nan, np.nan],
				3: [130, np.nan, np.nan, 160],
			}
		)
		df_1_differences, df_2_differences = self.differ.get_dataframe_differences(df_1, df_2)

		assert df_1_differences.equals(expected_df_1_differences)
		assert df_2_differences.equals(expected_df_2_differences)
