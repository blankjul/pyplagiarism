import os
from collections import namedtuple

import numpy as np
import plotly.graph_objects as go

from pyplagiarism.vendor.diff2html.diff2html import main as diff2html


def parse(path_to_file, sourround_with_method=True):
    with open(path_to_file, "r") as f:
        code = f.readlines()

    if sourround_with_method:
        code = ["   " + line for line in code]
        code.insert(0, "def run():")

    return code


def create_folder(p):
    if not os.path.exists(p):
        os.makedirs(p)

def get_files(path_to_folder):
    ret = []
    for root, dirs, files in os.walk(os.path.abspath(path_to_folder)):
        for f in files:
            ret.append(os.path.join(root, f))
    return sorted(ret)


def get_unique_key(data, f):
    name = os.path.basename(f)

    # remove the extension of necessary
    if '.' in name:
        name = '.'.join(name.split('.')[:-1])

    while name in data:
        name = "_" + name

    return name


def files_to_dict(*path_to_files):
    data = {}
    for f in path_to_files:
        key = get_unique_key(data, f)
        data[key] = parse(f)
    return data


def find_groups(labels, M, perc=0.95):
    b = np.full(len(labels), False)

    groups = []

    # a simple expand function which allows recursion
    def expand(i, b, g):
        if not b[i]:
            b[i] = True

            I = np.where(~b)[0]
            others = I[np.where(M[k, I] >= perc)[0]].tolist()

            for o in others:
                if not b[o]:
                    expand(o, b, g)
                    g.append(o)

    # until all students are considered
    while b.sum() < len(labels):

        I = np.where(~b)[0]
        k = int(I.min())

        val = [k]
        expand(k, b, val)

        if len(val) > 1:
            groups.append(val)

    groups = [sorted(group) for group in groups]

    return groups


def sort_by_plag(M, groups=None):
    S = []

    if groups is not None:
        for group in groups:
            S.extend(group)

    I = M.max(axis=1).argsort()[::-1]
    for i in I:
        if i not in S:
            S.append(int(i))

    return S


def plot(M, labels, **kwargs):
    val = np.copy(M)

    val = val ** 6
    val = 0.5 + (val / 2)

    np.fill_diagonal(val, np.inf)
    val[np.isinf(val)] = 0

    fig = go.FigureWidget(
        data=go.Heatmap(
            z=val,
            text=kwargs.get("P"),
            hovertext=M,
            x=labels,
            y=labels,
            colorscale=[
                [0, "grey"],
                [0.5, "white"],
                [1, "red"]],
            hoverinfo="x+y+z+text",
            zmin=0,
            zmax=1
        ))

    return fig


def visualize(out, M, labels, **kwargs):
    fig = plot(M, labels, **kwargs)

    html = fig.to_html()

    script = """
        <script>
            var myPlot =  document.getElementsByClassName("plotly-graph-div")[0];
            myPlot.on('plotly_click', function(data){
                var obj = data.points[0].text;
                if (obj.length > 0) {
                    window.open('diff/' + obj);
                }   
            });
        </script>
        """
    html += script

    with open(out, "w") as f:
        f.write(html)


def diff(out, files):
    P = [["" for _ in range(len(files))] for _ in range(len(files))]

    for i in range(len(files)):

        for j in range(i + 1, len(files)):
            file_a, file_b = files[i], files[j]
            Option = namedtuple("Options", "file1 file2 print_width show syntax_css verbose")
            options = Option(file1=file_a, file2=file_b, print_width=True, show=False, syntax_css="vs", verbose=False)

            name_a = os.path.basename(file_a)
            name_b = os.path.basename(file_b)

            fname = f"{name_a}_vs_{name_b}".replace(".py", "") + ".html"
            path = os.path.join(out, fname)

            diff2html(file_a, file_b, path, options)

            P[i][j], P[j][i] = fname, fname

    return np.array(P)


def check_similarities(data, cmp, verbose=False):
    label = np.array(list(data.keys()), dtype=np.str)

    M = np.full((len(label), len(label)), np.inf)

    # now compare the input for each pair of label
    for i in range(len(label)):
        for j in range(i + 1, len(label)):
            path_a, path_b = label[i], label[j]

            a, b = data[path_a], data[path_b]

            try:
                val = cmp.compare(a, b)
            except:
                val = 0.0
                if verbose:
                    print(f"Error while comparing {path_a} with {path_b}")

            M[i, j], M[j, i] = val, val

    return label, M


def check_groups(labels, M, verbose=True):
    groups = find_groups(labels, M)
    for i in range(len(groups)):
        g = groups[i]
        val = np.round(M[g][:, g].min(), 2)
        s = ", ".join(labels[g])

        if verbose:
            print(f"Group {i + 1} ({val}): {s}")

    return groups

