
#TASK 1: Python File Handling & Automation


import os
import shutil
import csv
from pathlib import Path
from datetime import datetime

# ============================================================================
# SECTION 1: CREATE SAMPLE DATA
# ============================================================================

def create_sample_files():
    """
    Creates sample input files for demonstration:
    - students.txt: Simple text file with student data
    - grades.csv: CSV file with student grades
    """
    try:
        # Create data directory if it doesn't exist
        data_dir = "sample_data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"✓ Created directory: {data_dir}")
        
        # Create a simple text file
        txt_file = os.path.join(data_dir, "students.txt")
        with open(txt_file, 'w') as f:
            f.write("STUDENT RECORDS\n")
            f.write("=" * 50 + "\n")
            f.write("Alice Johnson | Roll: 001 | Class: A\n")
            f.write("Bob Smith | Roll: 002 | Class: B\n")
            f.write("Charlie Davis | Roll: 003 | Class: A\n")
            f.write("Diana Wilson | Roll: 004 | Class: C\n")
        print(f"✓ Created text file: {txt_file}")
        
        # Create a CSV file with grades
        csv_file = os.path.join(data_dir, "grades.csv")
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Student Name', 'Math', 'English', 'Science', 'Average'])
            writer.writerow(['Alice Johnson', '95', '88', '92', '91.67'])
            writer.writerow(['Bob Smith', '78', '82', '85', '81.67'])
            writer.writerow(['Charlie Davis', '88', '90', '87', '88.33'])
            writer.writerow(['Diana Wilson', '92', '85', '88', '88.33'])
        print(f"✓ Created CSV file: {csv_file}")
        
        return data_dir
    
    except IOError as e:
        # Handle file I/O errors (permission denied, disk full, etc.)
        print(f"✗ Error creating files: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"✗ Unexpected error: {e}")
        return None


# ============================================================================
# SECTION 2: FILE READING OPERATIONS
# ============================================================================

def read_text_file(file_path):
    """
    Reads and displays content from a text file.
    Handles cases where file doesn't exist or can't be read.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n✓ Successfully read: {file_path}")
        print("-" * 50)
        print(content)
        print("-" * 50)
        return content
    
    except FileNotFoundError:
        # File doesn't exist
        print(f"✗ Error: File not found - {file_path}")
        return None
    
    except PermissionError:
        # Don't have permission to read the file
        print(f"✗ Error: Permission denied - {file_path}")
        return None
    
    except Exception as e:
        # Any other error during file reading
        print(f"✗ Error reading file: {e}")
        return None


def read_csv_file(file_path):
    """
    Reads CSV file and displays data in a formatted table.
    Useful for processing structured data.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Get column headers
            rows = list(reader)      # Get all data rows
        
        print(f"\n✓ Successfully read CSV: {file_path}")
        print("-" * 80)
        
        # Display headers
        print(" | ".join(f"{h:^20}" for h in headers))
        print("-" * 80)
        
        # Display rows
        for row in rows:
            print(" | ".join(f"{cell:^20}" for cell in row))
        
        print("-" * 80)
        return headers, rows
    
    except FileNotFoundError:
        print(f"✗ Error: CSV file not found - {file_path}")
        return None, None
    
    except csv.Error as e:
        # Error parsing CSV format
        print(f"✗ Error parsing CSV: {e}")
        return None, None
    
    except Exception as e:
        print(f"✗ Error reading CSV: {e}")
        return None, None


# ============================================================================
# SECTION 3: FILE WRITING OPERATIONS
# ============================================================================

def write_processed_data(input_file, output_file):
    """
    Reads input CSV, processes data (calculates statistics),
    and writes results to a new file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
        
        # Process data: Add a new column with grade letters
        processed_rows = [headers + ['Grade']]
        
        for row in rows:
            if len(row) >= 5:  # Has average score
                average = float(row[4])
                # Assign letter grade based on average
                if average >= 90:
                    grade = 'A'
                elif average >= 80:
                    grade = 'B'
                elif average >= 70:
                    grade = 'C'
                else:
                    grade = 'D'
                
                processed_rows.append(row + [grade])
        
        # Write processed data to output file
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(processed_rows)
        
        print(f"\n✓ Processed data written to: {output_file}")
        return True
    
    except FileNotFoundError:
        print(f"✗ Error: Input file not found - {input_file}")
        return False
    
    except ValueError as e:
        # Error converting data to float/int
        print(f"✗ Error processing data: {e}")
        return False
    
    except IOError as e:
        print(f"✗ Error writing file: {e}")
        return False


# ============================================================================
# SECTION 4: FILE AUTOMATION (RENAME, MOVE, DELETE)
# ============================================================================

def rename_file(old_path, new_path):
    """
    Renames a file from old_path to new_path.
    """
    try:
        # Check if source file exists
        if not os.path.exists(old_path):
            print(f"✗ Error: Source file not found - {old_path}")
            return False
        
        # Check if destination already exists
        if os.path.exists(new_path):
            print(f"✗ Error: Destination file already exists - {new_path}")
            return False
        
        # Perform rename operation
        os.rename(old_path, new_path)
        print(f"✓ Renamed: {old_path} → {new_path}")
        return True
    
    except PermissionError:
        print(f"✗ Error: Permission denied for rename operation")
        return False
    
    except Exception as e:
        print(f"✗ Error renaming file: {e}")
        return False


def move_file(source_path, destination_dir):
    """
    Moves a file to a different directory.
    Creates destination directory if it doesn't exist.
    """
    try:
        # Check if source file exists
        if not os.path.exists(source_path):
            print(f"✗ Error: Source file not found - {source_path}")
            return False
        
        # Create destination directory if needed
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f"✓ Created destination directory: {destination_dir}")
        
        # Move file using shutil.move (works across file systems)
        filename = os.path.basename(source_path)
        destination_path = os.path.join(destination_dir, filename)
        shutil.move(source_path, destination_path)
        
        print(f"✓ Moved: {source_path} → {destination_path}")
        return True
    
    except PermissionError:
        print(f"✗ Error: Permission denied for move operation")
        return False
    
    except Exception as e:
        print(f"✗ Error moving file: {e}")
        return False


def delete_file(file_path):
    """
    Deletes a file after confirming it exists.
    """
    try:
        if not os.path.exists(file_path):
            print(f"✗ Error: File not found - {file_path}")
            return False
        
        os.remove(file_path)
        print(f"✓ Deleted: {file_path}")
        return True
    
    except PermissionError:
        print(f"✗ Error: Permission denied - cannot delete {file_path}")
        return False
    
    except Exception as e:
        print(f"✗ Error deleting file: {e}")
        return False


def delete_directory(dir_path):
    """
    Deletes an entire directory and all its contents.
    Use with caution!
    """
    try:
        if not os.path.exists(dir_path):
            print(f"✗ Error: Directory not found - {dir_path}")
            return False
        
        # shutil.rmtree removes directory and all contents recursively
        shutil.rmtree(dir_path)
        print(f"✓ Deleted directory and contents: {dir_path}")
        return True
    
    except PermissionError:
        print(f"✗ Error: Permission denied - cannot delete {dir_path}")
        return False
    
    except Exception as e:
        print(f"✗ Error deleting directory: {e}")
        return False


# ============================================================================
# SECTION 5: FILE OPERATIONS WITH BACKUPS
# ============================================================================

def backup_file(file_path):
    """
    Creates a backup copy of a file with timestamp.
    Useful for preserving original files before modification.
    """
    try:
        if not os.path.exists(file_path):
            print(f"✗ Error: File not found - {file_path}")
            return None
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.splitext(file_path)[0]
        extension = os.path.splitext(file_path)[1]
        backup_path = f"{base_name}_backup_{timestamp}{extension}"
        
        # Copy file to backup location
        shutil.copy2(file_path, backup_path)  # copy2 preserves metadata
        print(f"✓ Backup created: {backup_path}")
        return backup_path
    
    except shutil.Error as e:
        print(f"✗ Error creating backup: {e}")
        return None
    
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return None


# ============================================================================
# SECTION 6: MAIN DEMONSTRATION
# ============================================================================

def main():
    """
    Main function that demonstrates all file handling operations.
    """
    print("=" * 70)
    print("TASK 1: PYTHON FILE HANDLING & AUTOMATION")
    print("=" * 70)
    
    # Step 1: Create sample files
    print("\n[STEP 1] Creating sample data files...")
    data_dir = create_sample_files()
    
    if data_dir is None:
        print("✗ Failed to create sample files. Exiting.")
        return
    
    # Step 2: Read and display files
    print("\n[STEP 2] Reading files...")
    txt_file = os.path.join(data_dir, "students.txt")
    csv_file = os.path.join(data_dir, "grades.csv")
    
    read_text_file(txt_file)
    read_csv_file(csv_file)
    
    # Step 3: Create backup before processing
    print("\n[STEP 3] Creating backup...")
    backup_file(csv_file)
    
    # Step 4: Process and write data
    print("\n[STEP 4] Processing and writing data...")
    processed_file = os.path.join(data_dir, "grades_processed.csv")
    write_processed_data(csv_file, processed_file)
    
    # Display processed file
    read_csv_file(processed_file)
    
    # Step 5: Rename file
    print("\n[STEP 5] File renaming operations...")
    renamed_file = os.path.join(data_dir, "final_grades.csv")
    rename_file(processed_file, renamed_file)
    
    # Step 6: Create archive directory and move file
    print("\n[STEP 6] Moving files to archive...")
    archive_dir = "archive_data"
    move_file(renamed_file, archive_dir)
    
    # Step 7: Demonstrate file deletion
    print("\n[STEP 7] Cleanup operations...")
    print("\nFiles and directories created during this demo:")
    print(f"- {data_dir}/")
    print(f"- {archive_dir}/")
    print("\nThese will remain on disk for your inspection.")
    print("Delete them manually when done reviewing.")
    
    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()