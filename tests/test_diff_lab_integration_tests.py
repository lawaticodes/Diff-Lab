import os
import tkinter as tk

from unittest import mock
from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, Extensions


@mock.patch("executables.diff_lab.diff_lab.Differ.show_diff_complete_info", return_value=None)
class DiffLabIntegrationTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

	def get_file_path(self, file_name):
		return f"{os.getcwd()}\\test_data\\integration_tests\\{file_name}"

	def test_xlsx_files_without_merged_cells_without_differences(self, mock_show_diff_complete_info):
		file_1_path = self.get_file_path("test_file_1_without_merged_cells.xlsx")
		file_2_path = self.get_file_path("test_file_1_without_merged_cells.xlsx")

		self.differ.compare_files(file_1_path, file_2_path, Extensions.XLSX.value)

	def test_xlsx_files_without_merged_cells_with_differences(self, mock_show_diff_complete_info):
		file_1_path = self.get_file_path("test_file_1_without_merged_cells.xlsx")
		file_2_path = self.get_file_path("test_file_2_without_merged_cells.xlsx")

		self.differ.compare_files(file_1_path, file_2_path, Extensions.XLSX.value)

	def test_xlsx_files_with_merged_cells_without_differences(self, mock_show_diff_complete_info):
		self.differ.compare_files("", "", Extensions.XLSX.value)

	def test_xlsx_files_with_merged_cells_with_differences(self, mock_show_diff_complete_info):
		self.differ.compare_files("", "", Extensions.XLSX.value)

	def test_csv_files_without_merged_cells_without_differences(self, mock_show_diff_complete_info):
		self.differ.compare_files("", "", Extensions.CSV.value)

	def test_csv_files_without_merged_cells_with_differences(self, mock_show_diff_complete_info):
		self.differ.compare_files("", "", Extensions.CSV.value)

	def test_csv_files_with_merged_cells_without_differences(self, mock_show_diff_complete_info):
		self.differ.compare_files("", "", Extensions.CSV.value)

	def test_csv_files_with_merged_cells_with_differences(self, mock_show_diff_complete_info):
		self.differ.compare_files("", "", Extensions.CSV.value)
