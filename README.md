# DNA_sequencing
This web app allows users to upload sequence data and visualize various sequence-related metrics, including sequence length and GC content analysis.


## Prerequisites

Before running the web app, ensure you have the following Python libraries installed:

- `dash`
- `dash_core_components`
- `dash_html_components`
- `dash_table`
- `pandas`
- `plotly`
- `base64`

You can install these libraries using `pip`:

```
pip install dash dash-core-components dash-html-components dash-table pandas plotly
```

## Running the Web App

1. Clone or download the repository to your local machine.
2. Navigate to the directory containing the `.py` file for the web app.
3. Run the following command:

```
python your_filename.py
```

Replace `your_filename.py` with the name of the Python file containing the web app code.

4. Once the app is running, open a web browser and navigate to `http://127.0.0.1:8070` to access the web app.

## Usage

1. Use the file upload interface to upload your sequence data.
2. Once uploaded, the data will be displayed in a table format.
3. Use the dropdown menu to select a specific sequence.
4. Visualize the sequence length in the provided plot.
5. Below the plot, view the GC content analysis for the selected sequence.

---
