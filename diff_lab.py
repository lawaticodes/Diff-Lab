import datetime
import numpy as np
import os
import pandas as pd
import tkinter as tk
import tkinter.messagebox as messagebox


SUPPORTED_EXTENSIONS = [".csv", ".xlsx"]
FONT = ("helvetica", 12, "bold")
FILE_1_NAME = "Name of first file:"
FILE_2_NAME = "Name of second file:"
DIFF = "DIFF"
CURRENT_PATH = os.getcwd()


class Differ:
	def __init__(self, root):
		self.root = root

		self.frame = tk.Frame(self.root)

		self.description = tk.Label(
			self.frame, text=self.get_description(), font=FONT
		).grid(row=0, padx=40, pady=40)

		self.file_1_label = tk.Label(
			self.frame, text=FILE_1_NAME, font=FONT
		).grid(row=1, pady=10)

		self.file_1_value = tk.StringVar(root)
		self.file_1_input = tk.Entry(
			self.frame, textvariable=self.file_1_value
		).grid(row=2)

		self.file_2_label = tk.Label(
			self.frame, text=FILE_2_NAME, font=FONT
		).grid(row=3, pady=10)

		self.file_2_value = tk.StringVar(root)
		self.file_2_input = tk.Entry(
			self.frame, textvariable=self.file_2_value
		).grid(row=4)

		self.diff_button = tk.Button(
			self.frame, text=DIFF, command=self.diff_files, font=FONT
		).grid(row=5, pady=50)

		self.frame.pack()

	def get_description(self):
		description = (
			"Welcome to DIFF LAB!\n\nTo start diffing, please enter the full names of the files you would like to "
			"compare below (including the extensions).\n\nThe extensions currently supported are:"
		)

		for extension in SUPPORTED_EXTENSIONS:
			description += f"\n {extension}"

		return description

	def show_error(self, message):
		messagebox.showerror(title="Error", message=message)

	def show_diff_complete_info(self, message):
		messagebox.showinfo(title="Diff Complete", message=message)

	def diff_files(self):
		file_1_name = self.file_1_value.get()
		file_2_name = self.file_2_value.get()

		if not self.validate_file_names(file_1_name, file_2_name):
			return

		file_1_path = self.get_file_path(file_1_name)
		file_2_path = self.get_file_path(file_2_name)

		for file_path in [file_1_path, file_2_path]:
			if not self.validate_file_path(file_path):
				return

		self.compare_files(file_1_path, file_2_path)

	def validate_file_names(self, file_1_name, file_2_name):
		if not file_1_name or not file_2_name:
			self.show_error("You must provide both file names.")
			return False

		file_1_ext = os.path.splitext(file_1_name)[1]
		file_2_ext = os.path.splitext(file_2_name)[1]

		if not file_1_ext or not file_2_ext:
			self.show_error("You must include the extension for both files.")
			return False

		for extension in [file_1_ext, file_2_ext]:
			if extension not in SUPPORTED_EXTENSIONS:
				self.show_error(f"The extension '{extension}' is not supported.")
				return False

		if file_1_ext != file_2_ext:
			self.show_error("The two files have different extensions.")
			return False

		return True

	def get_file_path(self, file_name):
		return f"{CURRENT_PATH}\\{file_name}"

	def validate_file_path(self, file_path):
		if not os.path.exists(file_path):
			self.show_error(f"There is no file for the path '{file_path}'.")
			return False

		return True

	def compare_files(self, file_1_path, file_2_path):
		df_1 = pd.read_excel(file_1_path, index_col=None, header=None)
		df_2 = pd.read_excel(file_2_path, index_col=None, header=None)

		df_1_col_len = df_1.shape[1]
		df_2_col_len = df_2.shape[1]

		if df_1_col_len != df_2_col_len:
			self.show_error(
				f"Cannot compare files with different structure. File 1 has {df_1_col_len} columns and file 2 has {df_2_col_len} columns."
			)
			return

		df_1_row_len = df_1.shape[0]
		df_2_row_len = df_2.shape[0]

		if df_1_row_len != df_2_row_len:
			self.show_error(
				f"Cannot compare files with different structure. File 1 has {df_1_row_len} rows and file 2 has {df_2_row_len} rows."
			)
			return

		columns = df_1.columns.tolist()

		if df_1.equals(df_2):
			self.show_diff_complete_info("The two files are identical to each other.")
			return

		df_1_differences = {}
		df_2_differences = {}

		for col in columns:
			df_1_values = []
			df_2_values = []

		for df_1_value, df_2_value in zip(df_1[col].tolist(), df_2[col].tolist()):
			if df_1_value == df_2_value:
				df_1_values.append(np.nan)
				df_2_values.append(np.nan)
			else:
				df_1_values.append(df_1_value)
				df_2_values.append(df_2_value)

		df_1_differences[col] = df_1_values
		df_2_differences[col] = df_2_values

		df_1_differences_df = pd.DataFrame.from_dict(df_1_differences)
		df_2_differences_df = pd.DataFrame.from_dict(df_2_differences)

		now = datetime.datetime.now()
		now_str = now.strftime("%d-%m-%Y_%H-%M-%S")
		diff_file_name = f"DIFF LAB OUTPUT {now_str}.xlsx"

		df_1_differences_df = df_1_differences_df.style.applymap(lambda v: self.apply_background_colour(v))
		df_2_differences_df = df_2_differences_df.style.applymap(lambda v: self.apply_background_colour(v))

		with pd.ExcelWriter(diff_file_name, mode="w") as writer:
			df_1_differences_df.to_excel(writer, sheet_name="File 1 differences", header=False, index=False)
			df_2_differences_df.to_excel(writer, sheet_name="File 2 differences", header=False, index=False)

		self.show_diff_complete_info(
			"The two files are not identical to each other. Please open the file titled 'DIFF LAB OUTPUT' with the "
			"appropriate time stamp in your current directory to view the differences."
		)

		# TODO: Tidy code and break up into smaller functions.
		# TODO: Write tests.
		# TODO: Handle merged cells.

	def apply_background_colour(self, value):
		colour = "green" if pd.isnull(value) else "red"
		return f"background-color: {colour}"


if __name__ == "__main__":
	root = tk.Tk()
	root.title("DIFF LAB")
	Differ(root)
	root.mainloop()
