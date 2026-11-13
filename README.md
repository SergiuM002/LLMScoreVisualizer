# LLMScoreVisualizer
A graphical user interface for plotting scores sourced from DNA language models using customtkinter. This project is for easily visualizing DNA LLM results.

## Quickstart

### Download
You can find the downloads on the [Release Page](https://github.com/SergiuM002/LLMScoreVisualizer/releases/latest).

## Building

### Creating the environment
Create the venv environment in the project root using `python3 -m venv .venv` and activate it.

### Building via Briefcase
Install briefcase with `pip install briefcase` and package the project with `briefcase package`. The built package should be in "dist/".

### Building via Pyinstaller
Install the requirements with `pip install -r requirements.txt` and pyinstaller with `pip install pyinstaller`. Then, package the program with `pyinstaller spec/main.spec`. The executable should be in "dist/LLMScoreVisualizer/".

## Usage
Select a plot type, import the CSVs with the scores and use the various plot options to get your desired plot.
You may also use the navigation toolbar below the plot the navigate within the plot itself.