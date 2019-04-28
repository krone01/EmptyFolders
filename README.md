
## Usage 
Due to my own laziness, I've made this script to help facilitate the testing of other scripts. Maybe it has some purpose to you, maybe it doesn't, but it's fairly versatile.

## WARNING
- ***If you're running this script with default flags, PUT THIS IN THE DIRECTORY OF THE DIRECTORIES YOU WOULD LIKE TO EMPTY***
- Do not run this script without knowing what it can do to your file system. If misused, this script can be extremely destructive. 
- It is *highly* recommended to look over the flags as they can make the script safer to use and make it do exactly what you want.

## Flags
All flags have some level of explanation through the --help/-h flag, but further explanation and examples are provided below.

***-o or --onlyFiles*** :: This flag can be used if you would like to ***remove*** only certain file extensions from the directory. 
Adding `-o .txt` to the arguments of the script will only remove files that end with .txt, furthermore `-o .txt .mp3 .mp4` will remove .txt, .mp3, and .mp4 files. *If this flag is not set, the script will remove all files it encounters.*

***-n or --notFiles*** :: This flag can be used if you would like to ***ignore*** certain file extensions in the directory. 
Adding `-n .exe` to the arguments of the script will remove all *but* executables, furthermore `-n .exe .js .cpp` will ignore executables, JavaScript files, and C++ source files. *If this flag is not set, the script will default to strictly ignoring Python source files '.py'. This is to prevent the script itself from being moved when the start directory is not set.*

***-r or  --removeEmpty*** :: This is extremely useful for tidying up the empty folders that are left by removing the folders after the directories have emptied. *By default, this flag is set to false.*

***-d or --removeRoot*** :: This is a piggy-back argument for `removeEmpty`, once the directory has emptied into the end directory, the starting directory will delete itself. The reason I say a piggy back argument is because it cannot be ran without the `removeEmpty` flag. This is to prevent any problems that may arise from the directory not actually being empty. Furthermore, this will not do anything unless the `endDir` flag is set to something other than `startDir` *By default, this flag is set to false.*

***-w or --noWarning*** :: This flag can be used to bypass the warning prompt that is ran at the start of the script. This is not recommended if you do not know what you're doing. *By default, this flag is set to false.*
 
 ***-g or --groupTypes*** :: This flag allows you to group files together by their file extensions. This will move the files into their own folder designated by file extension. *By default, this is set to false.*

***-s or --startDir*** :: This flag sets the starting directory that the script will walk through. For example, `-s "C:\Users\Jonathan\Downloads"` will remove the files from the folders contained in the **Downloads** folder. *By default, this is set to the directory the script is ran in.*

***-e or --endDir*** :: This flag sets the ending directory for the files to be moved to. For example, `-e "C:\Users\Jonathan\Documents` will empty the files into the **Documents** folder. *By default, this is set to the directory the script is ran in.*

## HOW TO RUN THE SCRIPT
1) Install Python 3.7+
2) Run the script by typing `python EmptyFolders.py` with your desired flags. 
- ***If you're running this script with default flags, PUT THIS IN THE DIRECTORY OF THE DIRECTORIES YOU WOULD LIKE TO EMPTY***
- Do not run this script without knowing what it can do to your file system. If misused, this script can be extremely destructive. 
3) Make sure the prompt is correct and run.
