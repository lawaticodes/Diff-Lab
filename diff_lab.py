import datetime
import numpy as np
import os
import pandas as pd
import tkinter as tk
import tkinter.messagebox as messagebox

from enum import Enum


class Extensions(Enum):
	XLSX = ".xlsx"
	CSV = ".csv"


SUPPORTED_EXTENSIONS = [Extensions.XLSX.value, Extensions.CSV.value]
FONT = ("helvetica", 12, "bold")
CURRENT_PATH = os.getcwd()
DESCRIPTION = (
	"Welcome to DIFF LAB!\n\nTo start diffing, please enter below the full names of the files you would like to "
	"compare (including the extensions). Both files must be present in your current directory.\n\nThe extensions "
	"currently supported are:"
)


class Differ:
	def __init__(self, root):
		self.root = root

		# Main frame.
		self.frame = tk.Frame(self.root)

		# Description.
		self.description = tk.Label(
			self.frame, text=self.get_description(), font=FONT
		).grid(row=0, padx=40, pady=40)

		# First file input.
		self.file_1_label = tk.Label(
			self.frame, text="Name of first file:", font=FONT
		).grid(row=1, pady=10)
		self.file_1_value = tk.StringVar(root)
		self.file_1_input = tk.Entry(
			self.frame, textvariable=self.file_1_value
		).grid(row=2)

		# Second file input.
		self.file_2_label = tk.Label(
			self.frame, text="Name of second file:", font=FONT
		).grid(row=3, pady=10)
		self.file_2_value = tk.StringVar(root)
		self.file_2_input = tk.Entry(
			self.frame, textvariable=self.file_2_value
		).grid(row=4)

		# Diff button.
		self.diff_button = tk.Button(
			self.frame, text="DIFF", command=self.diff_files, font=FONT
		).grid(row=5, pady=50)

		self.frame.pack()

	def get_description(self):
		"""Return the description of the program."""
		description = DESCRIPTION

		for extension in SUPPORTED_EXTENSIONS:
			description += f"\n {extension}"

		return description

	def show_error(self, message):
		"""Show an error window with the appropriate message."""
		messagebox.showerror(title="Error", message=message)

	def show_diff_complete_info(self, message):
		"""Show an information window stating that the diffing is complete."""
		messagebox.showinfo(title="Diff Complete", message=message)

	def diff_files(self):
		"""Open the files and diff them against each other."""
		file_1_name = self.file_1_value.get()
		file_2_name = self.file_2_value.get()
		valid_file_names, extension = self.validate_file_names(file_1_name, file_2_name)

		if not valid_file_names:
			return

		file_1_path = self.get_file_path(file_1_name)
		file_2_path = self.get_file_path(file_2_name)

		for file_path in [file_1_path, file_2_path]:
			if not self.validate_file_path(file_path):
				return

		self.compare_files(file_1_path, file_2_path, extension)

	def validate_file_names(self, file_1_name, file_2_name):
		"""Validate the file names."""
		not_valid = (False, None)

		if not file_1_name or not file_2_name:
			self.show_error("You must provide both file names.")
			return not_valid

		file_1_ext = os.path.splitext(file_1_name)[1]
		file_2_ext = os.path.splitext(file_2_name)[1]

		if not file_1_ext or not file_2_ext:
			self.show_error("You must include the extension for both files.")
			return not_valid

		for extension in [file_1_ext, file_2_ext]:
			if extension not in SUPPORTED_EXTENSIONS:
				self.show_error(f"The extension '{extension}' is not supported.")
				return not_valid

		if file_1_ext != file_2_ext:
			self.show_error("The two files have different extensions.")
			return not_valid

		return True, file_1_ext

	def get_file_path(self, file_name):
		"""Get the full file path."""
		return f"{CURRENT_PATH}\\{file_name}"

	def validate_file_path(self, file_path):
		"""Check that the file path exists."""
		if not os.path.exists(file_path):
			self.show_error(f"There is no file for the path '{file_path}'.")
			return False

		return True

	def compare_files(self, file_1_path, file_2_path, extension, diff_report_dir_path=CURRENT_PATH):
		"""Compare the two files for any differences."""
		df_1 = self.open_file_as_dataframe(file_1_path, extension)
		df_2 = self.open_file_as_dataframe(file_2_path, extension)

		if not self.validate_dataframe_structures(df_1, df_2):
			return

		if df_1.equals(df_2):
			self.show_diff_complete_info("The two files are identical to each other.")
			return

		df_1_differences, df_2_differences = self.get_dataframe_differences(df_1, df_2)
		self.create_diff_report_file(df_1_differences, df_2_differences, CURRENT_PATH)

		self.show_diff_complete_info(
			"The two files are not identical to each other. Please open the file titled 'DIFF LAB OUTPUT' with the "
			"appropriate time stamp in your current directory to view the differences."
		)

	def open_file_as_dataframe(self, file_path, extension):
		"""Open the file for the given file path as a dataframe."""
		if extension == Extensions.XLSX.value:
			return pd.read_excel(file_path, index_col=None, header=None)
		elif extension == Extensions.CSV.value:
			return pd.read_csv(file_path, index_col=None, header=None)

	def validate_dataframe_structures(self, df_1, df_2):
		"""Check that the two dataframes have the same structure (same number of columns and rows)."""
		error_message = "Cannot compare files with different structures."

		df_1_cols = df_1.shape[1]
		df_2_cols = df_2.shape[1]

		if df_1_cols != df_2_cols:
			self.show_error(f"{error_message} File 1 has {df_1_cols} columns and file 2 has {df_2_cols} columns.")
			return False

		df_1_rows = df_1.shape[0]
		df_2_rows = df_2.shape[0]

		if df_1_rows != df_2_rows:
			self.show_error(f"{error_message} File 1 has {df_1_rows} rows and file 2 has {df_2_rows} rows.")
			return False

		return True

	def get_dataframe_differences(self, df_1, df_2):
		"""Return the differences in the two dataframes.

		The first return object should be a dataframe which contains values that only the first file has. The second
		return object should be a dataframe which contains values that only the second file has. In both return objects,
		if the two files have the same cell value then it should be represented as np.nan.
		"""
		columns = df_1.columns.tolist()
		num_of_rows = df_1.shape[0]
		df_1_differences = {}
		df_2_differences = {}

		for col in columns:
			df_1_values = [np.nan for n in range(num_of_rows)]
			df_2_values = [np.nan for n in range(num_of_rows)]

			for index, (df_1_value, df_2_value) in enumerate(zip(df_1[col].tolist(), df_2[col].tolist())):
				if df_1_value != df_2_value:
					df_1_values[index] = df_1_value
					df_2_values[index] = df_2_value

			df_1_differences[col] = df_1_values
			df_2_differences[col] = df_2_values

		return pd.DataFrame.from_dict(df_1_differences), pd.DataFrame.from_dict(df_2_differences)

	def create_diff_report_file(self, df_1_differences,  df_2_differences, diff_report_dir_path):
		"""Create a .xlsx file containing the differences in the two files.

		The first sheet should contain values that only the first file has. The second sheet should contain values that
		only the second file has.
		"""
		df_1_differences = df_1_differences.style.applymap(lambda v: self.apply_background_colour(v))
		df_2_differences = df_2_differences.style.applymap(lambda v: self.apply_background_colour(v))
		timestamp = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
		file_name = f"{diff_report_dir_path}\\DIFF LAB OUTPUT {timestamp}.xlsx"

		with pd.ExcelWriter(file_name, mode="w") as writer:
			df_1_differences.to_excel(writer, sheet_name="File 1 differences", header=False, index=False)
			df_2_differences.to_excel(writer, sheet_name="File 2 differences", header=False, index=False)

	def apply_background_colour(self, value):
		"""Apply colour to the cells (green if cell has no value and red if it does have a value)."""
		colour = "green" if pd.isnull(value) else "red"
		return f"background-color: {colour}"


# Run this script to launch the diffing program.
if __name__ == "__main__":
	root = tk.Tk()
	root.title("DIFF LAB")
	Differ(root)
	root.mainloop()
