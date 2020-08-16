import os
import tkinter as tk

from unittest import mock
from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, DESCRIPTION, Extensions


CURRENT_PATH = os.getcwd()


@mock.patch("executables.diff_lab.diff_lab.Differ.show_error", return_value=None)
class DiffLabTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

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
		assert self.differ.validate_file_path(f"{CURRENT_PATH}\\test_data\\test_file_path_exists.xlsx")

	def test_file_path_does_not_exist(self, mock_show_error):
		assert not self.differ.validate_file_path(f"{CURRENT_PATH}\\test_data\\invalid_file_path.xlsx")


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
