import tkinter as tk

from unittest import TestCase

from executables.diff_lab.diff_lab import Differ


class DiffLabIntegrationTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

	def test_xlsx_files_without_merged_cells_without_differences(self):
		pass

	def test_xlsx_files_without_merged_cells_with_differences(self):
		pass

	def test_xlsx_files_with_merged_cells_without_differences(self):
		pass

	def test_xlsx_files_with_merged_cells_with_differences(self):
		pass

	def test_csv_files_without_merged_cells_without_differences(self):
		pass

	def test_csv_files_without_merged_cells_with_differences(self):
		pass

	def test_csv_files_with_merged_cells_without_differences(self):
		pass

	def test_csv_files_with_merged_cells_with_differences(self):
		pass
