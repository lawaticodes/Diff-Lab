import glob
import numpy as np
import os
import pandas as pd
import tkinter as tk

from unittest import mock
from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, Extensions


CURRENT_PATH = os.getcwd()


@mock.patch("executables.diff_lab.diff_lab.Differ.show_diff_complete_info", return_value=None)
class DiffLabIntegrationTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

	def tearDown(self):
		for file in self.get_output_files():
			os.remove(file)

	def get_output_files(self):
		return glob.glob("DIFF LAB OUTPUT*.xlsx")

	def get_output_file_path(self, file_name):
		return f"{os.getcwd()}\\{file_name}"

	def compare_files(self, file_1_name, file_2_name, extension):
		file_path = f"{os.getcwd()}\\test_data\\integration_tests\\"
		self.differ.compare_files(file_path + file_1_name, file_path + file_2_name, extension)

	def test_xlsx_files_without_merged_cells_without_differences(self, mock_show_diff_complete_info):
		self.compare_files(
			"test_file_1_without_merged_cells.xlsx", "test_file_1_without_merged_cells.xlsx", Extensions.XLSX.value
		)

		assert not self.get_output_files()

	def test_xlsx_files_without_merged_cells_with_differences(self, mock_show_diff_complete_info):
		self.compare_files(
			"test_file_1_without_merged_cells.xlsx", "test_file_2_without_merged_cells.xlsx", Extensions.XLSX.value
		)
		expected_df_1_differences = pd.DataFrame(
			{
				0: [np.nan, np.nan, 11, np.nan, np.nan],
				1: [2, np.nan, np.nan, 17, np.nan],
				2: [np.nan, 8, np.nan, np.nan, np.nan],
				3: [np.nan, 9, np.nan, np.nan, 24],
				4: [np.nan, np.nan, np.nan, np.nan, 25],
			}
		)
		expected_df_2_differences = pd.DataFrame(
			{
				0: [np.nan, np.nan, 110, np.nan, np.nan],
				1: [20, np.nan, np.nan, 170, np.nan],
				2: [np.nan, 80, np.nan, np.nan, np.nan],
				3: [np.nan, 90, np.nan, np.nan, 240],
				4: [np.nan, np.nan, np.nan, np.nan, 250],
			}
		)
		output_files = self.get_output_files()

		assert len(output_files) == 1

		output_file_path = self.get_output_file_path(output_files[0])
		df_1_differences = pd.read_excel(output_file_path, sheet_name=0, index_col=None, header=None)
		df_2_differences = pd.read_excel(output_file_path, sheet_name=1, index_col=None, header=None)

		assert df_1_differences.equals(expected_df_1_differences)
		assert df_2_differences.equals(expected_df_2_differences)

	# def test_xlsx_files_with_merged_cells_without_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.XLSX.value)
	#
	# def test_xlsx_files_with_merged_cells_with_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.XLSX.value)
	#
	# def test_csv_files_without_merged_cells_without_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
	#
	# def test_csv_files_without_merged_cells_with_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
	#
	# def test_csv_files_with_merged_cells_without_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
	#
	# def test_csv_files_with_merged_cells_with_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
