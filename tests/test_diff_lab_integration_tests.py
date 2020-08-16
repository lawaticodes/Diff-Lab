import glob
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
		expected_dataframe = pd.DataFrame()
		self.compare_files(
			"test_file_1_without_merged_cells.xlsx", "test_file_2_without_merged_cells.xlsx", Extensions.XLSX.value
		)
		output_files = self.get_output_files()

		assert len(output_files) == 1

		output_file_path = self.get_output_file_path(output_files[0])
		dataframe = pd.read_excel(output_file_path, index_col=None, header=None)

		assert dataframe.equals(expected_dataframe)

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
