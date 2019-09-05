import os, datetime, shutil

"""
Description: This program is meant to recursively copy one directory into another.

How to use: Replace "YourPathHere" with the absolute path of the directory you
expect to be updating. ie. C:\Bob\Documents\Folder3 and replace
"YourPathThatYouWantToStayUpdatedHere" with the one you want to
 keep updated.

"""


pathNew = r"YourPathHere"
pathOld = r"YourPathThatYouWantToStayUpdatedHere"
start_Time = datetime.datetime.now()  # used to calculate run time of program


def list_Files(path_To_Compare, path_To_Update):
    # Creates list of directories/files
    # files/Dirs in pathNew
    new_File_List = []  # list of files
    new_Dir_List = []  # list of Dirs
    new_Dir_Basename = []  # list of basename  of directories
    new_File_Basename = []  # basename of files in newDir

    new_Dir_Files = []  # list of files and dirs in new Files

    # files/Dirs in pathOld
    old_File_List = []  # list of files
    old_Dir_List = []  # list of directories
    old_Dir_Basename = []  # basename of directories
    old_File_Basename = []  # basename of files

    old_Dir_Files = [] # list of files and dirs in pathOld

    for root, dirs, files in os.walk(path_To_Compare):

        for d in dirs:
            new_Dir_List.append(os.path.abspath(os.path.join(root, d)))
            new_Dir_Basename.append(os.path.basename(d))
            new_Dir_Files.append(os.path.join(root, d))

        for f in files:
            new_File_List.append(str(os.path.abspath(os.path.join(root, f))))
            new_File_Basename.append(str(os.path.basename(os.path.join(root, f))))
            new_Dir_Files.append(os.path.join(root, f))

    for root, dirs, files in os.walk(path_To_Update):
        for d in dirs:
            old_Dir_List.append(str(os.path.abspath(os.path.join(root, d))))
            old_Dir_Basename.append(os.path.basename(d))
            old_Dir_Files.append(os.path.join(root, d))

        for f in files:
            old_File_List.append(str(os.path.abspath(os.path.join(root, f))))
            old_File_Basename.append(str(os.path.basename(os.path.join(root, f))))
            old_Dir_Files.append(os.path.join(root, f))

    # This is for testing
    # print("new files ", *new_File_List)
    # print("new direction ", *new_Dir_List)
    # print("new Dir BaseName", *new_Dir_Basename)
    # print("new file basename", *new_File_Basename)
    # print("new dirs and files", *new_Dir_Files)
    # print("\n")
    # print("old files ", *old_File_List)
    # print("old directory ", *old_Dir_List)
    # print("old Dir BaseName", *old_Dir_Basename)
    # print("old file basename", *old_File_Basename)

    # For testing
    # print("Difference in lists", set(new_Dir_List) - set(old_Dir_List))

    # For the range of items in the directory list
    for item in range(len(new_Dir_Files)):

        # if basename is not in old directory list and it is a directory, create the directory.
        # will also create all subdirectories
        if os.path.isdir(new_Dir_Files[item]):

            if os.path.basename(new_Dir_Files[item]) not in old_Dir_Basename:
                # print("mkdir", os.path.join(pathOld, os.path.relpath(new_Dir_List[item], pathNew)))
                os.mkdir(os.path.join(pathOld, os.path.relpath(new_Dir_List[item], pathNew)))

        # else if entry is in new_directory
        elif os.path.isfile(new_Dir_Files[item]):

            # and if basename of new_Directory is not in old directory
            # copy the file to old directory
            if os.path.basename(new_Dir_Files[item]) not in old_File_Basename:
                # print("copy files src", new_Dir_Files[item],"dst ", os.path.join(pathOld, os.path.relpath(new_Dir_Files[item], pathNew)))
                shutil.copy2(new_Dir_Files[item], os.path.join(pathOld, os.path.relpath(new_Dir_Files[item], pathNew)))

            # if basename of file is in old_File_Basename directory and getmtime of new_file is greater than old file
            # "update" the file
            elif os.path.basename(new_Dir_Files[item]) in old_File_Basename:
                if os.path.getmtime(new_Dir_Files[item]) > os.path.getmtime(old_File_List[old_File_Basename.index(os.path.basename(new_Dir_Files[item]))]):
                    # print("newly modified files", os.path.join(pathOld, os.path.relpath(new_Dir_Files[item], pathNew)))
                    shutil.copy2(new_Dir_Files[item], os.path.join(pathOld, os.path.relpath(new_Dir_Files[item], pathNew)))

    # for range of files in Old directory
    for item in range(len(old_Dir_Files)):

        # if the item is a directory
        if os.path.isdir(old_Dir_Files[item]):

            # if the directory does not exist in the new Directory
            # delete directory tree
            if os.path.basename(old_Dir_Files[item]) not in new_Dir_Basename:
                # print("Removing this directory: ", old_Dir_Files[item])
                shutil.rmtree(old_Dir_Files[item])

        # else if the item is a file
        elif os.path.isfile(old_Dir_Files[item]):

            # and the item does not exist in the new Directory
            # delete the file
            if os.path.basename(old_Dir_Files[item]) not in new_File_Basename:
                # print("Deleting this file: ", old_Dir_Files[item])
                os.remove(old_Dir_Files[item])

# add ability to delete trees and stuff if not in new_ but is in old_


list_Files(pathNew, pathOld)

# calculates amount of time between program start and program end
print("Finished running in:", datetime.datetime.now() - start_Time)
