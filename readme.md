# Auto Deletion Script

This Python script helps you clean up your Linux system by deleting temporary files, unwanted data, and even entire folders based on configurable criteria. It also removes any empty folders and subfolders after the deletion process.

## Features

- **File Deletion:** Delete files based on name patterns, extensions, content, size, and relative age (in days).
- **Folder Deletion:** Delete entire folders if they are older than a specified number of days.
- **Recursive Scanning:** Option to scan folders and all their subdirectories.
- **Empty Folder Cleanup:** Automatically remove empty folders after file deletion.
- **Easy Configuration:** Simply update the `Config.json` file to change which files or folders to target.

## Prerequisites

- Python 3.x installed on your Linux system.
- Basic understanding of terminal commands.

## Files Included

- **app.py:** The main Python script that performs the deletion operations.
- **config.json:** A JSON configuration file where you specify folders, deletion criteria, and other settings.
- **readme.md:** This file, which explains how to use the script.

## How to Use

### 1. Update the Configuration File

Open the `Config.json` file in your favorite text editor and update it with your desired settings. Below is a sample configuration:

```json
{
  "folders": [
    {
      "path": "/path/to/folder1",
      "deleteEntireFolder": false,
      "recursive": true,
      "criteria": {
        "fileNamePattern": "temp_*",      
        "fileExtensions": [".tmp", ".bak"],
        "containsString": "delete me",      
        "fileSizeLessThan": 102400,
        "createdAgeDays": 180,
        "modifiedAgeDays": 90
      }
    },
    {
      "path": "/path/to/folder2",
      "deleteEntireFolder": false,
      "recursive": false,
      "criteria": {
        "fileNameContains": "old",         
        "fileExtensions": [".log"],
        "containsString": "error",         
        "fileSizeGreaterThan": 1048576,
        "createdAgeDays": 365,
        "modifiedAgeDays": 180
      }
    },
    {
      "path": "/path/to/folder3",
      "deleteEntireFolder": true,
      "criteria": {
        "folderAgeDays": 30
      }
    },
    {
      "path": "/path/to/folder4",
      "deleteEntireFolder": false,
      "recursive": true,
      "criteria": {
        "fileNameEndsWith": ".cache",
        "fileSizeBetween": {
          "min": 2048,
          "max": 5120
        },
        "modifiedBetweenDays": {
          "start": 30,
          "end": 365
        }
      }
    }
  ]
}
```

- **path:** Absolute path to the folder.
- **deleteEntireFolder:** Set to `true` to delete the entire folder (with an optional age check).
- **recursive:** Set to `true` to include subdirectories when scanning files.
- **criteria:** Conditions to match files or folders. You can specify file name patterns, content checks, file sizes, and relative age (in days).

### 2. Run the Script

1. Open a terminal.
2. Navigate to the directory containing `script.py` and `Config.json`.
3. Run the script with Python:

   ```bash
   python3 script.py
   ```

### 3. Review the Output

The script will print messages to the terminal showing which files or folders were deleted. It will also notify you if any errors occur or if folders are not old enough (based on the configured age) to be deleted.

## Important Notes

- **Test First:** Always run the script on a test folder or with sample data to ensure it behaves as expected before running it on important directories.
- **Backup:** Make sure to back up any critical data. The script permanently deletes files and folders.
- **Permissions:** You might need to run the script with elevated permissions (using `sudo`) if some directories require administrative access.

## Troubleshooting

- **File Access Errors:** If the script cannot access a file, ensure you have the necessary permissions.
- **Incorrect Deletion:** Double-check your `Config.json` criteria if files or folders are not being deleted as expected.
- **Python Errors:** Ensure you are using Python 3 and that all dependencies (standard libraries) are available.

## Customization

You can customize the script further to add more criteria or modify the deletion process as needed. The code is well-commented, making it easier to understand and modify.

##### Below is a table that explains all the keys you can use in the `Config.json` file:

| **Key**               | **Applies To**                                          | **Explanation**                                                                                                                                       | **Expected Value/Type**                          |
|-----------------------|---------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| **path**              | Folder entry                                            | The absolute path to the folder you want to process.                                                                                                  | String                                           |
| **deleteEntireFolder**| Folder entry                                            | If set to `true`, the script will delete the entire folder instead of scanning for individual files.                                                 | Boolean (`true`/`false`)                         |
| **recursive**         | Folder entry (when deleting files)                      | Indicates whether to search the folder recursively (including all subdirectories) for files that meet the criteria.                                    | Boolean (`true`/`false`)                         |
| **criteria**          | Folder entry                                            | A dictionary containing the conditions to match files or folders for deletion.                                                                        | Dictionary                                       |
| **fileNamePattern**   | File deletion criteria                                  | A glob-style pattern to match file names (e.g., `"temp_*"`).                                                                                          | String                                           |
| **fileNameContains**  | File deletion criteria                                  | A substring that must be present in the file name.                                                                                                    | String                                           |
| **fileNameEndsWith**  | File deletion criteria                                  | Specifies that the file name should end with the provided string.                                                                                     | String                                           |
| **fileExtensions**    | File deletion criteria                                  | A list of file extensions to target (e.g., `[ ".tmp", ".bak" ]`).                                                                                      | List of strings                                  |
| **containsString**    | File deletion criteria                                  | Checks whether the file's content includes a specific string.                                                                                        | String                                           |
| **fileSizeLessThan**  | File deletion criteria                                  | Deletes the file if its size is less than this value (in bytes).                                                                                       | Integer (bytes)                                  |
| **fileSizeGreaterThan** | File deletion criteria                                | Deletes the file if its size is greater than this value (in bytes).                                                                                     | Integer (bytes)                                  |
| **fileSizeBetween**   | File deletion criteria                                  | A dictionary defining a range for file size with `min` and `max` keys (in bytes).                                                                       | Dictionary with keys `"min"` and `"max"`         |
| **createdAgeDays**    | File deletion criteria                                  | Targets files that were created at least this many days ago (relative age).                                                                            | Integer (days)                                   |
| **modifiedAgeDays**   | File deletion criteria                                  | Targets files that were last modified at least this many days ago (relative age).                                                                       | Integer (days)                                   |
| **modifiedBetweenDays** | File deletion criteria                                | A dictionary specifying a range (with `start` and `end` in days) for file modification age.                                                            | Dictionary with keys `"start"` and `"end"`       |
| **folderAgeDays**     | Folder deletion criteria (when `deleteEntireFolder` is true) | When deleting an entire folder, this key specifies that the folder must be older than the given number of days (relative age) to be deleted.            | Integer (days)                                   |

This table should help you understand the purpose of each key and how to configure your JSON file for the auto deletion script.
