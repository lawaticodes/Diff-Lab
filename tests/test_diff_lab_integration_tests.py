import glob
import numpy as np
import os
import pandas as pd
import tempfile
import tkinter as tk

from unittest import mock
from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, Extensions


@mock.patch("executables.diff_lab.diff_lab.Differ.show_diff_complete_info", return_value=None)
class DiffLabIntegrationTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

	def get_test_file_path(self, test_file_name):
		return f"{os.getcwd()}\\test_data\\integration_tests\\{test_file_name}"

	def get_output_files(self, dir_path):
		return glob.glob(f"{dir_path}\\DIFF LAB OUTPUT*.xlsx")

	def compare_files_and_check_no_output(self, file_1_name, file_2_name, extension):
		file_1_path = self.get_test_file_path(file_1_name)
		file_2_path = self.get_test_file_path(file_2_name)

		with tempfile.TemporaryDirectory() as temp_dir:
			self.differ.compare_files(file_1_path, file_2_path, extension, temp_dir)

			assert not self.get_output_files(temp_dir)

	def test_xlsx_without_merged_cells_without_differences(self, mock_show_diff_complete_info):
		self.compare_files_and_check_no_output(
			"file_1_without_merged_cells.xlsx", "file_1_without_merged_cells.xlsx", Extensions.XLSX.value
		)

	def test_xlsx_without_merged_cells_with_differences(self, mock_show_diff_complete_info):
		test_file_1_path = self.get_test_file_path("file_1_without_merged_cells.xlsx")
		test_file_2_path = self.get_test_file_path("file_2_without_merged_cells.xlsx")

		expected_file_1_differences = pd.DataFrame(
			{
				0: [np.nan, np.nan, 11, np.nan, np.nan],
				1: [2, np.nan, np.nan, 17, np.nan],
				2: [np.nan, 8, np.nan, np.nan, np.nan],
				3: [np.nan, 9, np.nan, np.nan, 24],
				4: [np.nan, np.nan, np.nan, np.nan, 25],
			}
		)
		expected_file_2_differences = pd.DataFrame(
			{
				0: [np.nan, np.nan, 110, np.nan, np.nan],
				1: [20, np.nan, np.nan, 170, np.nan],
				2: [np.nan, 80, np.nan, np.nan, np.nan],
				3: [np.nan, 90, np.nan, np.nan, 240],
				4: [np.nan, np.nan, np.nan, np.nan, 250],
			}
		)

		with tempfile.TemporaryDirectory() as temp_dir:
			self.differ.compare_files(test_file_1_path, test_file_2_path, Extensions.XLSX.value, temp_dir)
			output_files = self.get_output_files(temp_dir)

			assert len(output_files) == 1

			file_1_differences = pd.read_excel(output_files[0], sheet_name=0, index_col=None, header=None)
			file_2_differences = pd.read_excel(output_files[0], sheet_name=1, index_col=None, header=None)

			assert file_1_differences.equals(expected_file_1_differences)
			assert file_2_differences.equals(expected_file_2_differences)

	# def test_xlsx_with_merged_cells_without_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.XLSX.value)
	#
	# def test_xlsx_with_merged_cells_with_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.XLSX.value)
	#
	# def test_csv_without_merged_cells_without_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
	#
	# def test_csv_without_merged_cells_with_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
	#
	# def test_csv_with_merged_cells_without_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
	#
	# def test_csv_with_merged_cells_with_differences(self, mock_show_diff_complete_info):
	# 	self.differ.compare_files("", "", Extensions.CSV.value)
