import tkinter as tk
from unittest import TestCase

from executables.diff_lab.diff_lab import Differ, DESCRIPTION, Extensions


class GetDescriptionTestCase(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.differ = Differ(tk.Tk())

	def test_get_description(self):
		assert self.differ.get_description() == f"{DESCRIPTION}\n {Extensions.XLSX.value}\n {Extensions.CSV.value}"


class DiffFilesTestCase(TestCase):
	# TODO: Add tests
	pass


class ValidateFileNamesTestCase(TestCase):
	# TODO: Add tests
	pass


class GetFilePathTestCase(TestCase):
	# TODO: Add tests
	pass


class ValidateFilePathTestCase(TestCase):
	# TODO: Add tests
	pass


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
