import shutil
import streamlit as st
import os


def copy_md_files_from_to(source_directory, target_directory):
    """
    Copies all markdown files from root_directory and all inside folders
    to target_directory.
    :param source_directory:
    :param target_directory:
    :return: None
    """
    st.write("Copying files from `{}` to `{}`".format(source_directory, target_directory))

    md_files = []

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.endswith(".md"):
                md_files.append(os.path.join(root, filename))
                shutil.copy(os.path.join(root, filename), target_directory)

    st.write("Files copied:")
    st.write(md_files)


