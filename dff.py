import hashlib
import os
import stat
import sys
import time

# Flags
verbose_output = None
output_immediately = None
trial_delete = None
delete_shorter = None

# Globals
stdout = ""
megabytes_scanned = 0
failed_delete_count = 0

# Constants
BYTES_IN_A_MEGABYTE = 1048576
BYTES_TO_SCAN = 4096
SCAN_SIZE_MB = BYTES_TO_SCAN / BYTES_IN_A_MEGABYTE

# Progress
SHOW_PROGRESS = lambda t, d: ...


class FileFullHash:
    full: dict = {}

    def __init__(self):
        self.full.clear()

    def search_duplicate(self, snip_file_path, current_file_path):
        current_file_hash = self.hash_full(current_file_path)
        if current_file_hash in self.full:
            return self.full[current_file_hash]

        snip_file_hash = self.hash_full(snip_file_path)
        self.full[snip_file_hash] = snip_file_path
        if current_file_hash in self.full:
            return self.full[current_file_hash]

        self.full[current_file_hash] = current_file_path
        return False

    def hash_full(self, file_path):
        global megabytes_scanned
        SHOW_PROGRESS("...calculating full hash of " + file_path, True)
        file_hash = hashlib.blake2b()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(BYTES_TO_SCAN), b""):
                file_hash.update(chunk)
                megabytes_scanned += SCAN_SIZE_MB
        return file_hash.hexdigest()


def unicode_output(out):
    # when printing directly to the windows console stdout, unicode errors tend to be ignored automatically
    # if the user redirects stdout to a file, unicode errors can occur
    # this code outputs the best it can and flags errors in the output
    try:
        print(out, flush=True)
    except UnicodeEncodeError:
        try:
            print(out.encode("utf8").decode(sys.stdout.encoding))
        except UnicodeDecodeError:
            print(out.encode("utf8").decode(sys.stdout.encoding, errors="ignore") + " <-- UnicodeDecodeError")


class DFF:
    def find_file_duplicates(self, path, show_progress):
        global SHOW_PROGRESS
        SHOW_PROGRESS = show_progress

        start_time = time.time()
        SHOW_PROGRESS(time.strftime("%X : "), False)

        sizes = FileSizes()
        sizes.find_files_with_duplicate_file_size(path)

        snip = dict()
        full_hash = FileFullHash()

        duplicate_count = 0
        file_count = 0

        for current_file_path in sizes.files_list:
            file_count += 1
            SHOW_PROGRESS("Processing file " + current_file_path, True)
            current_file_snip_hash = self.hash_snip(current_file_path)
            if current_file_snip_hash in snip:
                dupe_file_path = full_hash.search_duplicate(snip[current_file_snip_hash], current_file_path)
                if dupe_file_path:
                    display_duplicate(dupe_file_path, current_file_path)
                    duplicate_count += 1
                else:
                    SHOW_PROGRESS("...first 4096 bytes are the same, but files are different", True)
            else:
                snip[current_file_snip_hash] = current_file_path

        SHOW_PROGRESS(
            "\n"
            + time.strftime("%X : ")
            + str(duplicate_count)
            + " duplicate files found, "
            + str(file_count)
            + " files and "
            + str(megabytes_scanned)
            + " megabytes scanned in "
            + str(round(time.time() - start_time, 3))
            + " seconds, "
            + str(sizes.file_count)
            + " files assessed",
            False
        )

        if failed_delete_count:
            SHOW_PROGRESS("\n" + "failed to delete " + str(failed_delete_count) + " duplicates - rerun script", False)

        return stdout

    @staticmethod
    def hash_snip(file_path):
        global megabytes_scanned
        SHOW_PROGRESS("...calculating hash snippet of " + file_path, True)
        snip_hash = hashlib.blake2b()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(BYTES_TO_SCAN), b""):
                    snip_hash.update(chunk)
                    f.close()
                    megabytes_scanned += SCAN_SIZE_MB
                    return snip_hash.hexdigest()
                return "UnexpectedError:" + file_path
        except PermissionError:
            SHOW_PROGRESS("PermissionError: " + file_path + "\n", False)
            return "PermissionError:" + file_path


class FileSizes:
    sizes: dict = {}
    files_to_process: dict = {}
    files_list: list = []  # want to process files in os.walk order, not some unknown order
    file_count = 0

    def __init__(self):
        self.sizes.clear()
        self.files_to_process.clear()
        self.files_list.clear()

    def find_files_with_duplicate_file_size(self, path):
        self.file_count = 0
        for root, _, files in sorted(os.walk(path)):
            files.sort()
            for file_name in files:
                self.file_count += 1
                current_file_path = os.path.join(root, file_name)
                SHOW_PROGRESS("Checking size of file " + current_file_path, True)
                try:
                    file_size = os.path.getsize(current_file_path)
                except FileNotFoundError:  # in case of symlink to nowhere
                    continue
                if file_size > 0:
                    self.add_file(current_file_path, file_size)

    def add_file(self, current_file_path, size):
        if size in self.sizes:
            SHOW_PROGRESS(current_file_path + " has non unique file size [" + str(size) + " bytes]", False)
            self.add_original_file_to_process_list(self.sizes[size])
            self.add_file_to_process_list(current_file_path)
        else:
            self.sizes[size] = current_file_path

    def add_original_file_to_process_list(self, original_file_path):
        if original_file_path in self.files_to_process:
            SHOW_PROGRESS(original_file_path + " is a known size duplicate", True)
            return
        self.add_file_to_process_list(original_file_path)

    def add_file_to_process_list(self, file_path):
        self.files_to_process[file_path] = True
        self.files_list.append(file_path)
        SHOW_PROGRESS(file_path + " added to process list", True)


def display_duplicate(previously_hashed_file_path, current_file_path):
    current_file_message = "            "
    previously_hashed_file_message = ""

    SHOW_PROGRESS(
        current_file_message
        + current_file_path
        + "\n is dupe of "
        + previously_hashed_file_path
        + previously_hashed_file_message
        + "\n", False
    )


def delete_duplicate_and_get_message(previously_hashed_file_path, current_file_path):
    delete_file_path = current_file_path
    previously_hashed_file_message = ""
    current_file_message = "deleted ... "

    if delete_shorter:
        if len(os.path.basename(previously_hashed_file_path)) < len(os.path.basename(current_file_path)):
            delete_file_path = previously_hashed_file_path
            previously_hashed_file_message = " ... deleted"
            current_file_message = "            "

    if not trial_delete:
        try:
            os.chmod(delete_file_path, stat.S_IWRITE)
            os.remove(delete_file_path)
        except FileNotFoundError:
            # only the previously hashed file could have been deleted and
            # not the current file (unless user is deleting files outside of this script!)
            previously_hashed_file_message = " ... already deleted"
            global failed_delete_count
            failed_delete_count += 1

    return previously_hashed_file_message, current_file_message
