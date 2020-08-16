import os
import tkinter as tk

from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, DESCRIPTION, Extensions


CURRENT_PATH = os.getcwd()


class DiffLabTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

	# Test get_description().

	def test_get_description(self):
		assert self.differ.get_description() == f"{DESCRIPTION}\n {Extensions.XLSX.value}\n {Extensions.CSV.value}"

	# Test get_file_path().

	def test_get_file_path(self):
		assert self.differ.get_file_path("file_name.xlsx") == f"{CURRENT_PATH}\\file_name.xlsx"

	# Test validate_file_path().

	def test_file_path_exists(self):
		assert self.differ.validate_file_path(f"{CURRENT_PATH}\\test_data\\test_file_path_exists.xlsx")

	# def test_file_path_does_not_exist(self):
	# 	assert not self.differ.validate_file_path(f"{CURRENT_PATH}\\test_data\\invalid_file_path.xlsx")

# class ValidateFileNamesTestCase(TestCase):
# 	@classmethod
# 	def setUpClass(cls):
# 		cls.differ = Differ(tk.Tk())
# 		cls.not_valid = (False, None)
#
# 	def test_missing_file_1_name(self):
# 		assert self.differ.validate_file_names(None, "file_2.xlsx") == self.not_valid
#
# 	def test_missing_file_2_name(self):
# 		assert self.differ.validate_file_names("file_1.xlsx", None) == self.not_valid
#
# 	def test_missing_file_1_extension(self):
# 		assert self.differ.validate_file_names("file_1", "file_2.xlsx") == self.not_valid
#
# 	def test_missing_file_2_extension(self):
# 		assert self.differ.validate_file_names("file_1.xlsx", "file_2") == self.not_valid
#
# 	def test_file_1_extension_not_supported(self):
# 		assert self.differ.validate_file_names("file_1.zip", "file_2.xlsx") == self.not_valid
#
# 	def test_file_2_extension_not_supported(self):
# 		assert self.differ.validate_file_names("file_1.xlsx", "file_2.zip") == self.not_valid
#
# 	def test_files_have_different_extensions(self):
# 		assert self.differ.validate_file_names("file_1.xlsx", "file_2.csv") == self.not_valid
#
# 	def test_valid_file_names(self):
# 		assert self.differ.validate_file_names("file_1.xlsx", "file_2.xlsx") == (True, Extensions.XLSX.value)
# 		assert self.differ.validate_file_names("file_1.csv", "file_2.csv") == (True, Extensions.CSV.value)


class CompareFilesTestCase(TestCase):
	# TODO: Add tests
	pass


class OpenFileAsDataframeTestCase(TestCase):
	# TODO: Add tests
	# f"{os.getcwd()}\\test_data\\{extension}\\{file_name}.{extension}"
	pass


class ValidateDataframeStructuresTestCase(TestCase):
	# TODO: Add tests
	pass


class GetDataframeDifferencesTestCase(TestCase):
	# TODO: Add tests
	pass


class CreateDiffReportFileTestCase(TestCase):
	# TODO: Add tests
	pass
