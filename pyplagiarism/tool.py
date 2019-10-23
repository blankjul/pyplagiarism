import os
import webbrowser

from pyplagiarism.comparator import PycodeComparison
from pyplagiarism.util import get_files, files_to_dict, sort_by_plag, diff, check_similarities, check_groups, visualize, \
    create_folder


def plagiarism(data,
               output_folder=None,
               comparator=PycodeComparison(),
               find_groups=True,
               visualize_as_html=True,
               sort_by_plagiarism=True,
               diff_of_files=True,
               verbose=True
               ):
    """

    Function that does the job of plagiarism check.

    Parameters
    ----------

    data
        A dictionary where each entry is a source code file.

    output_folder
        The output folder where the results should be stored

    find_groups
        Whether groups of similarities should be detected.

    visualize_as_html
        Whether the output should be written to file file that visualizes the plagiarism in a
        matrix.

    sort_by_plagiarism
        Whether the files should be sorted by corresponding amount of plagiarism when visualized in html.
        Otherwise, the files are sorted by alphabet.

    diff_of_files
        Whether for each pair of files a diff should be created.

    comparator
        The comparator which returns compares two lists of strings (the lines of each file) and
        returns the corresponding plagiarism value. New comparators can be written and provided.

    verbose
        Whether output should be printed or not.

    """

    if output_folder is None:
        if visualize_as_html or diff_of_files:
            raise Exception("Please define output_folder if the results should be visualized or diff files written.")
    else:
        create_folder(output_folder)

    # actually run the comparisons
    labels, M = check_similarities(data, comparator, verbose=verbose)

    groups = None
    path_to_diff = None

    if find_groups:
        groups = check_groups(labels, M)

    if diff_of_files:
        diff_path = os.path.join(output_folder, "diff")
        create_folder(diff_path)
        path_to_diff = diff(diff_path, data)

    if sort_by_plagiarism:
        I = sort_by_plag(M, groups=groups)
        M = M[I][:, I]
        labels = labels[I]
        if path_to_diff is not None:
            path_to_diff = path_to_diff[I][:, I]

    if visualize_as_html:
        out_index = os.path.join(output_folder, "index.html")
        visualize(out_index, M, labels, P=path_to_diff)
        webbrowser.open('file://' + out_index)


def plagiarism_from_files(*files):
    # if just one entry we assume it is the folder
    if len(files) == 1:
        files = get_files(files[0])

    # parse all the data into an array
    return files_to_dict(*files)
