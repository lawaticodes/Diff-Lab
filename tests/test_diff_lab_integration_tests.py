import glob
import numpy as np
import os
import pandas as pd
import tempfile
import tkinter as tk

from unittest import mock
from unittest import TestCase

from diff_lab import Differ, Extensions


@mock.patch("diff_lab.Differ.show_diff_complete_info", return_value=None)
class DiffLabIntegrationTestCase(TestCase):
	"""Test the diffing of two files using Differ's compare_files function.

	Note that CSV files cannot have merged cells, which is why there are no tests for them.
	"""

	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())
		cls.expected_file_1_differences = pd.DataFrame(
			{
				0: [np.nan, np.nan, 11, np.nan, np.nan],
				1: [2, np.nan, np.nan, 17, np.nan],
				2: [np.nan, 8, np.nan, np.nan, np.nan],
				3: [np.nan, 9, np.nan, np.nan, 24],
				4: [np.nan, np.nan, np.nan, np.nan, 25],
			}
		)
		cls.expected_file_2_differences = pd.DataFrame(
			{
				0: [np.nan, np.nan, 110, np.nan, np.nan],
				1: [20, np.nan, np.nan, 170, np.nan],
				2: [np.nan, 80, np.nan, np.nan, np.nan],
				3: [np.nan, 90, np.nan, np.nan, 240],
				4: [np.nan, np.nan, np.nan, np.nan, 250],
			}
		)

	def compare_files_and_check_output(
		self, file_1_name, file_2_name, extension, expected_file_1_differences=None, expected_file_2_differences=None
	):
		test_file_dir_path = f"{os.getcwd()}\\tests\\test_data\\integration_tests\\"
		file_1_path = test_file_dir_path + file_1_name
		file_2_path = test_file_dir_path + file_2_name

		with tempfile.TemporaryDirectory() as temp_dir:
			self.differ.compare_files(file_1_path, file_2_path, extension, temp_dir)
			output_files = glob.glob(f"{temp_dir}\\DIFF LAB OUTPUT*.xlsx")

			if expected_file_1_differences is None and expected_file_2_differences is None:
				assert not output_files
			else:
				assert len(output_files) == 1

				file_1_differences = pd.read_excel(output_files[0], sheet_name=0, index_col=None, header=None)
				file_2_differences = pd.read_excel(output_files[0], sheet_name=1, index_col=None, header=None)

				assert file_1_differences.equals(expected_file_1_differences)
				assert file_2_differences.equals(expected_file_2_differences)

	def test_csv_same(self, mock_show_diff_complete_info):
		self.compare_files_and_check_output(
			"file_1_without_merged_cells.csv", "file_1_without_merged_cells.csv", Extensions.CSV.value
		)

	def test_csv_different(self, mock_show_diff_complete_info):
		self.compare_files_and_check_output(
			"file_1_without_merged_cells.csv",
			"file_2_without_merged_cells.csv",
			Extensions.CSV.value,
			self.expected_file_1_differences,
			self.expected_file_2_differences,
		)

	def test_xlsx_no_merged_cells_same(self, mock_show_diff_complete_info):
		self.compare_files_and_check_output(
			"file_1_without_merged_cells.xlsx", "file_1_without_merged_cells.xlsx", Extensions.XLSX.value
		)

	def test_xlsx_no_merged_cells_different(self, mock_show_diff_complete_info):
		self.compare_files_and_check_output(
			"file_1_without_merged_cells.xlsx",
			"file_2_without_merged_cells.xlsx",
			Extensions.XLSX.value,
			self.expected_file_1_differences,
			self.expected_file_2_differences,
		)

	def test_xlsx_with_merged_cells_same(self, mock_show_diff_complete_info):
		self.compare_files_and_check_output(
			"file_3_with_merged_cells.xlsx", "file_3_with_merged_cells.xlsx", Extensions.XLSX.value
		)

	def test_xlsx_with_merged_cells_different(self, mock_show_diff_complete_info):
		expected_file_3_differences = pd.DataFrame(
			{
				0: [1, np.nan, np.nan, np.nan, np.nan],
				1: [np.nan, np.nan, 12, 17, 22],
				2: [np.nan, np.nan, np.nan, np.nan, np.nan],
				3: [np.nan, 9, np.nan, np.nan, np.nan],
				4: [np.nan, 10, np.nan, np.nan, np.nan],
			}
		)
		expected_file_4_differences = pd.DataFrame(
			{
				0: [10, np.nan, np.nan, np.nan, np.nan],
				1: [np.nan, np.nan, 120, 170, 220],
				2: [np.nan, np.nan, np.nan, np.nan, np.nan],
				3: [np.nan, 90, np.nan, np.nan, np.nan],
				4: [np.nan, 100, np.nan, np.nan, np.nan],
			}
		)

		self.compare_files_and_check_output(
			"file_3_with_merged_cells.xlsx",
			"file_4_with_merged_cells.xlsx",
			Extensions.XLSX.value,
			expected_file_3_differences,
			expected_file_4_differences,
		)

	def test_xlsx_with_merged_cells_different_special(self, mock_show_diff_complete_info):
		# This test is special in the sense that the files involved do not have the same structure.

		expected_file_5_differences = pd.DataFrame(
			{
				0: [1, np.nan, np.nan, np.nan, np.nan],
				1: [np.nan, np.nan, np.nan, np.nan, np.nan],
				2: [np.nan, 8, 13, np.nan, 23],
				3: [np.nan, np.nan, np.nan, 19, np.nan],
				4: [np.nan, np.nan, np.nan, 20, 25],
			}
		)
		expected_file_6_differences = pd.DataFrame(
			{
				0: [10, np.nan, np.nan, 16, np.nan],
				1: [np.nan, np.nan, 12, np.nan, np.nan],
				2: [np.nan, np.nan, np.nan, np.nan, 230],
				3: [4, np.nan, np.nan, 190, np.nan],
				4: [50, np.nan, 15, np.nan, np.nan],
			}
		)

		self.compare_files_and_check_output(
			"file_5_with_merged_cells.xlsx",
			"file_6_with_merged_cells.xlsx",
			Extensions.XLSX.value,
			expected_file_5_differences,
			expected_file_6_differences,
		)
