# :page_facing_up: DIFF LAB :page_facing_up:

An app designed to show the differences between 2 different Excel files. This is best suited for comparing files with the same format.

## Usage

Move the files you would like to compare into the main directory.

Then, run the following command:
```python
python diff_lab.py
```

When the UI appears, enter the file names for the 2 files, including their extensions, e.g. 'file_1.csv'. Hit 'DIFF' and you will see a 'Diff Complete' informational pop up box.

If the files are identical, you will get a pop up with the message 'The two files are identical to each other.'.

If the files are not identical, you will be told that a 'DIFF LAB OUTPUT' .xlsx file illustrating the differences has been created, and it will be in the same directory. The file name will contain a timestamp corresponding to when the diff was conducted and it will have 2 sheets inside it. Both sheets will contain a mixture of green and red cells, green to show values that were the same and red to show the difference in values. The first sheet called 'File 1 differences' will contain the values that only the first file has. The second sheet 'File 2 differences' will contain the values that only the second file has.
