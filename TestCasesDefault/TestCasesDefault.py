import unittest
import pandas as pd
from openpyxl import load_workbook

class ExcelTestCase(unittest.TestCase):

    def test_DEFAULT_1(self):

        # Loads the Excel file into a DataFram
        df = pd.read_excel('TestCasesDefault/Default Empty.xlsx', header=None)

        # Gets the number of rows with data beyond the headers
        num_data_rows = len(df) - 1 

        # Check if there are additional rows with data
        if num_data_rows > 0:

            self.fail("There are {} additional rows with data in the Excel file".format(num_data_rows))
        
        print(".TEST 1 DEFAULT CORRECT: The Default Empty.xlsx file not contains additional rows to the header")

    def test_DEFAULT_2(self):
    # Excel files you wish to validate along with their names
        filenames = [
            ("TestCasesDefault/time weston.xlsx", "time weston.xlsx"),
            ("TestCasesDefault/time weston minutes.xlsx", "time weston minutes.xlsx")
        ]

        # Values you want to search for in each file
        name_value = "Celestin, Elizabeth"
        glcode_value = "3050-3001-31233"

        # List to store the details of the rows that do not meet the criteria.
        failed_rows = []

        for filename, excel_name in filenames:
            # Read the Excel file
            df = pd.read_excel(filename)

            # Filter by the value in the "NAME" column
            filtered_df = df[df["NAME"] == name_value]

            # Get the rows that do not meet the validation criterion
            incorrect_rows = filtered_df[filtered_df["GLCODE"] != glcode_value]

            # If there are incorrect rows, add the details to the list of failed_rows
            if not incorrect_rows.empty:
                for index, row in incorrect_rows.iterrows():
                    failed_rows.append((excel_name, index + 2, row["GLCODE"]))

        # Check if any row did not meet the criterion
        if failed_rows:
            # Display the message with the details of the incorrect rows
            message = "Problems were found in the following records:\n"
            for excel_name, row_num, glcode in failed_rows:
                message += f"File: {excel_name}, Row {row_num}: GLCODE={glcode} does not match the expected value.\n"
            self.fail(message)
        
        print(".TEST 2 DEFAULT CORRECT: Celestin's GLCODE, contains - and is 3050-3001-31233")

    #Method required for test_DEFAULT_3
    
    def validar_glcode(self, glcode):
        # Remove dashes "-" and count the remaining digits.
        glcode_sin_guiones = glcode.replace('-', '')
        return len(glcode_sin_guiones) == 9 and glcode_sin_guiones.isdigit()

    def test_DEFAULT_3(self):
        files = ["TestCasesDefault/Combined File minutes.xlsx", "TestCasesDefault/Combined File.xlsx"]

        all_incorrect_rows = set()  # We use a set to store the incorrect rows without duplicates

        for file in files:
            try:
                with pd.ExcelFile(file) as xls:
                    sheet_name = xls.sheet_names[0]  # We assume that the sheet of interest is the first one.

                    # Load the file and convert the "GLCODE" column to "text" format.
                    df = pd.read_excel(xls, sheet_name)
                    df["GLCODE"] = df["GLCODE"].astype(str)

                    # Validate that all cells in the "GLCODE" column contain 9 digits without dashes "-".
                    incorrect_rows = []
                    for index, glcode in df["GLCODE"].items():
                        if not self.validar_glcode(glcode):
                            incorrect_rows.append((file, index + 2, glcode))

                    # Add the incorrect rows to the general set
                    all_incorrect_rows.update(incorrect_rows)
            except Exception as e:
                # If an exception occurs, it displays the error message and logs the exception..
                print(f"Error al procesar el file {file}: {str(e)}")

        # Show failure message with all incorrect rows in all files
        if all_incorrect_rows:
            error_msg = "The GLCODE does not contain 9 digits in the following rows and files:\n"
            for file, row, glcode in all_incorrect_rows:
                error_msg += f"file: {file}, row: {row}, GLCODE: {glcode}\n"
            self.fail(error_msg)

        print(".TEST 3 DEFAULT CORRECT: All GLCODEs have 9 numeric digits.")
    
    def test_Default_4_1(self):

        files = ["TestCasesDefault/6-11.xlsx", "TestCasesDefault/6-11 Minutes.xlsx"]

        all_errors = []  # List to store all the errors found

        for file in files:
            xls = pd.ExcelFile(file)
            sheet_name = xls.sheet_names[0]  # We assume that the sheet of interest is the first one.

            # Load the file and filter by "Attaway, Brooke" in the column "NAME".
            df = pd.read_excel(xls, sheet_name)
            brooke_df = df[df["NAME"] == "Attaway, Brooke"]

            # Check that the "GLCODE" column contains one of the expected values.
            incorrect_rows = []
            for index, row in brooke_df.iterrows():
                glcode = str(row["GLCODE"])
                if glcode not in ["6142", "006142"]:
                    incorrect_rows.append((file, index + 2, glcode))

            # Add errors to the general list
            all_errors.extend(incorrect_rows)

            xls.close()  # Close the file after reading it

        # Display error message with all errors encountered
        if all_errors:
            error_msg = "Errores para Attaway, Brooke:\n"
            for file, row, glcode in all_errors:
                error_msg += f"file: {file}, row: {row}, GLCODE: {glcode}\n"
            self.fail(error_msg)

        print("TEST 4.1 DEFAULT CORRECT: FILE TEST 6-11 BROOKE CORRECT: All GLCODEs for Brooke are valid.")

    def test_Default_4_2(self):    
        files = ["TestCasesDefault/6-11.xlsx", "TestCasesDefault/6-11 Minutes.xlsx"]

        all_errors = []  # List for storing all errors found

        for file in files:
            xls = pd.ExcelFile(file)
            sheet_name = xls.sheet_names[0]  # We assume that the sheet of interest is the first one.

            # Load the file and filter by "Barr, Brieann" in the column "NAME".
            df = pd.read_excel(xls, sheet_name)
            brieann_df = df[df["NAME"] == "Barr, Brieann"]

            # Check that the "GLCODE" column contains one of the expected values.
            incorrect_rows = []
            for index, row in brieann_df.iterrows():
                glcode = str(row["GLCODE"])
                if glcode not in ["007317", "6402", "7317"]:
                    incorrect_rows.append((file, index + 2, glcode))

            # Add errors to the general list
            all_errors.extend(incorrect_rows)

            xls.close()  # Close the file after reading it

        # Display error message with all errors encountered
        if all_errors:
            error_msg = "Errors forBarr, Brieann:\n"
            for file, row, glcode in all_errors:
                error_msg += f"file: {file}, row: {row}, GLCODE: {glcode}\n"
            self.fail(error_msg)

        print("TEST 4.2 DEFAULT CORRECT: FILE TEST 6-11 BRIEANN CORRECT: All GLCODEs for Brieann are valid.")

    def test_DEFAULT_5_1(self):
    # Excel files you wish to validate along with their names
        filenames = [
            ("TestCasesDefault/1667243700213_980358248.xlsx", "1667243700213_980358248.xlsx"),
            ("TestCasesDefault/1667243700213_980358248 minutes.xlsx", "1667243700213_980358248 minutes.xlsx")
        ]

        # Values you want to search for in each file
        name_value = "Tr-Freeman, Alexander"
        glcode_value = "1110.2115.1057"

        # List to store the details of the rows that do not meet the criteria.
        failed_rows = []

        for filename, excel_name in filenames:
            # Read the Excel file
            df = pd.read_excel(filename)

            # Filter by the value in the "NAME" column
            filtered_df = df[df["NAME"] == name_value]

            # Get the rows that do not meet the validation criterion
            incorrect_rows = filtered_df[filtered_df["GLCODE"] != glcode_value]

            # If there are incorrect rows, add the details to the list of failed_rows
            if not incorrect_rows.empty:
                for index, row in incorrect_rows.iterrows():
                    failed_rows.append((excel_name, index + 2, row["GLCODE"]))

        # Check if any row did not meet the criterion
        if failed_rows:
            # Display the message with the details of the incorrect rows
            message = "Problems were found in the following records:\n"
            for excel_name, row_num, glcode in failed_rows:
                message += f"File: {excel_name}, Row {row_num}: GLCODE={glcode} does not match the expected value.\n"
            self.fail(message)
        
        print(".TEST 5.1 DEFAULT CORRECT: Alexander's GLCODE contains . and is 1110.2115.1057")

    def test_DEFAULT_5_2(self):
        # Excel files you wish to validate along with their names
            filenames = [
                ("TestCasesDefault/1667243700213_980358248.xlsx", "1667243700213_980358248.xlsx"),
                ("TestCasesDefault/1667243700213_980358248 minutes.xlsx", "1667243700213_980358248 minutes.xlsx")
            ]

            # Values you want to search for in each file
            name_value = "Tr-Belcher, Hanna"
            glcode_value = "1130.2305.1474"

            # List to store the details of the rows that do not meet the criteria.
            failed_rows = []

            for filename, excel_name in filenames:
                # Read the Excel file
                df = pd.read_excel(filename)

                # Filter by the value in the "NAME" column
                filtered_df = df[df["NAME"] == name_value]

                # Get the rows that do not meet the validation criterion
                incorrect_rows = filtered_df[filtered_df["GLCODE"] != glcode_value]

                # If there are incorrect rows, add the details to the list of failed_rows
                if not incorrect_rows.empty:
                    for index, row in incorrect_rows.iterrows():
                        failed_rows.append((excel_name, index + 2, row["GLCODE"]))

            # Check if any row did not meet the criterion
            if failed_rows:
                # Display the message with the details of the incorrect rows
                message = "Problems were found in the following records:\n"
                for excel_name, row_num, glcode in failed_rows:
                    message += f"File: {excel_name}, Row {row_num}: GLCODE={glcode} does not match the expected value.\n"
                self.fail(message)
            
            print(".TEST 5.2 DEFAULT CORRECT: Hannas's GLCODE contains . and is 1110.2115.1057")

    def test_DEFAULT_6(self):
        files = ["TestCasesDefault/Kronos Timecards TC 07-30-22.xlsx", "TestCasesDefault/Kronos Timecards TC 07-30-22 minutes.xlsx"]

        all_errors = []  # List to store all the errors found

        for file in files:
            try:
                xls = pd.ExcelFile(file)
                sheet_name = xls.sheet_names[0]  # We assume that the sheet of interest is the first one.

                # Load the file and filter by "AMBURN, SARAH" and "ATKINS, CARA" in the column "NAME".
                df = pd.read_excel(xls, sheet_name)
                filtered_df = df[df["NAME"].isin(["AMBURN, SARAH", "ATKINS, CARA"])]

                # Check that the "GLCODE" column contains the expected value "95221046530001".
                incorrect_rows = []
                for index, row in filtered_df.iterrows():
                    glcode = str(row["GLCODE"])
                    if glcode != "95221046530001":
                        incorrect_rows.append((file, index + 2, glcode))

                # Add errors to the general list
                all_errors.extend(incorrect_rows)

                xls.close()  # Close the file after reading it
            except Exception as e:
                self.fail(f"Error reading {file}: {str(e)}")

        # Display error message with all errors encountered
        if all_errors:
            error_msg = "Errors for AMBURN, SARAH and ATKINS, CARA:\n"
            for file, row, glcode in all_errors:
                error_msg += f"file: {file}, row: {row}, GLCODE: {glcode}\n"
            self.fail(error_msg)

        print("TEST 6 DEFAULT CORRECT: The GLCODE of AMBURN, SARAH ; ATKINS, CARA match the expected value and have 14 digits.")

    def test_DEFAULT_7(self):
        file1 = "TestCasesDefault/Time Detail_July152022 minutes.xlsx"
        file2 = "TestCasesDefault/Time Detail_July152022.xlsx"
        name_to_find = "Anderson, Kasey"
        expected_glcode = ["34006510", "4900-20-40", "4900"]

        # Leer los archivos Excel
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)

        # Filtrar por el valor de "NAME"
        filtered_df1 = df1[df1["NAME"] == name_to_find]
        filtered_df2 = df2[df2["NAME"] == name_to_find]

        # Almacenar los errores encontrados
        errors = []

        # Verificar que los valores de "GLCODE" coincidan con los esperados
        for index, row in filtered_df1.iterrows():
            if row["GLCODE"] not in expected_glcode:
                errors.append(f"File: {file1}, Row: {index + 2}")

        for index, row in filtered_df2.iterrows():
            if row["GLCODE"] not in expected_glcode:
                errors.append(f"File: {file2}, Row: {index + 2}")

        # Si hay errores, imprimirlos; de lo contrario, imprimir mensaje de éxito
        if errors:
            for error in errors:
                print("TEST 7 DEFAULT ERROR WITH GL CODE for Anderson, Kasey:", error)
        else:
            print("TEST 7 DEFAULT CORRECT: The GLCODE of Anderson, Kasey match the expected value")

    def test_default_14(self):
        # File path and name of the Excel file
        excel_file = 'TestCasesDefault/6-11.xlsx'
        
        # Sheet name in the Excel file
        excel_sheet = 'Sheet1'
        
        # Names to search in the NAME column
        names_to_search = ['Aguilar, Isabelle', 'Aguilar, Marissa']
        
        # Columns to check for empty values
        columns_to_check = ['DATE', 'GLCODE', 'PAYCODE', 'STARTDTM', 'ENDDTM', 'HOURS']
        
        # Read the Excel file into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=excel_sheet)
        
        # Filter by names in the NAME column
        filtered_df = df[df['NAME'].isin(names_to_search)]
        
        # Check for empty columns in the specified columns
        empty_columns = filtered_df[filtered_df[columns_to_check].isnull().any(axis=1)]
        
        # Generate the error message
        error_msg = "The following rows and columns have empty data:\n"
        for idx, row in empty_columns.iterrows():
            for col in columns_to_check:
                if pd.isnull(row[col]):
                    error_msg += f"Column: {col}, Row: {idx+2}\n"
        
        # Assert that there are no empty columns
        self.assertTrue(empty_columns.empty, error_msg)
        print(".TEST 11 DEFAULT CORRECT: All the information of the nurses are in the file.")
    
    def test_Default_15(self):
        # File path and name of the Excel file
        excel_file = 'TestCasesDefault/6-11.xlsx'
        
        # Sheet name in the Excel file
        excel_sheet = 'Sheet1'
        
        # Name to search in the NAME column
        name_to_search = 'Anderson, Jennifer'
        
        # Read the Excel file into a DataFrame
        df = pd.read_excel(excel_file, sheet_name=excel_sheet)
        
        # Count the occurrences of the name in the NAME column
        name_count = df['NAME'].value_counts().get(name_to_search, 0)
        
        # Check if the name appears exactly three times
        self.assertEqual(name_count, 3, f"The name '{name_to_search}' registered {name_count} shifts, but it should registered 3 shifts.")
        
        # Print a message if the test passes
        print(".TEST 12 DEFAULT CORRECT: The nurse registered in the file three shifts.")

    def test_default_16(self): 
        #Files: TestCasesDefault\6-11 Minutes.xlsx , TestCasesDefault\6-11.xlsx
        # Descriotion: Check if the nurse has her last comment that is located in the next page
        file_paths = ['TestCasesDefault\\6-11.xlsx', 'TestCasesDefault\\6-11 Minutes.xlsx']

        # Name to search and data to verify in the 'Comments' column
        name_to_find = 'Casey, Quentasha'
        expected_comment = "LV"

        for file_path in file_paths:
            try:
                # Read the Excel file and the 'Sheet1' sheet
                df = pd.read_excel(file_path, sheet_name='Sheet1')

                # Search for the name in the 'NAME' column
                name_row = df[df['NAME'] == name_to_find]
                if not name_row.empty:
                    row_index = name_row.index[0+2]

                    # Verify if the comment matches the expected value
                    comment_value = df.loc[row_index, 'Comments']
                    cleaned_comment = comment_value.strip()  # Remove leading/trailing whitespaces

                    if cleaned_comment == expected_comment:
                        print(f"TEST 16 DEFAULT CORRECT: Name and Comments are matched in file '{file_path}'.")
                    else:
                        print(f"TEST 16 DEFAULT INCORRECT: The comment found was '{cleaned_comment}' in file '{file_path}'.")
                else:
                    print(f"TEST 16 DEFAULT INCORRECT: The name '{name_to_find}' was not found in the file '{file_path}'.")
            except pd.errors.ParserError as pe:
                print(f"Error while parsing the file '{file_path}': {str(pe)}")
            except FileNotFoundError as fnf:
                print(f"Error: File '{file_path}' not found.")
            except Exception as e:
                print(f"Unexpected error while processing the file '{file_path}': {str(e)}")

    def test_Default_17(self): 
        # List of files to validate
        file_paths = ['TestCasesDefault\\6-11.xlsx', 'TestCasesDefault\\6-11 Minutes.xlsx']

        # Word to search for in the 'Comments' column
        word_to_find = 'UPO'

        for file_path in file_paths:
            try:
                # Read the Excel file and the 'Sheet1' sheet
                df = pd.read_excel(file_path, sheet_name='Sheet1')

                # Search for the word in the 'Comments' column
                rows_with_word = df[df['Comments'].str.contains(word_to_find, case=False, na=False)]

                if not rows_with_word.empty:
                    for index, row in rows_with_word.iterrows():
                        row_number = index + 2  # Add 2 to index to account for 0-based indexing and header row
                        column_name = df.columns.get_loc('Comments') + 1  # Get the column number for 'Comments'
                        print(f"TEST 17 DEFAULT INCORRECT: Word '{word_to_find}' found in row {row_number}, column Comments in file '{file_path}'.")
                else:
                    print(f"TEST 17 DEFAULT CORRECT: Word is not present in the Comments column in file '{file_path}'.")
            except pd.errors.ParserError as pe:
                print(f"Error while parsing the file '{file_path}': {str(pe)}")
            except FileNotFoundError as fnf:
                print(f"Error: File '{file_path}' not found.")
            except Exception as e:
                print(f"Unexpected error while processing the file '{file_path}': {str(e)}")

if __name__ == '__main__':

    unittest.main()
