# LLMScoreVisualizer
A graphical user interface for plotting scores sourced from DNA language models using customtkinter. This project is for easily visualizing DNA LLM results.

## Quickstart

### Cloning the repository
Clone the repository to your system using `git clone <repository-link>`.

### Creating the environment
Create the venv environment using `python -m venv .venv`, activate it and install the required packages from the requirements.txt with `pip install -r requirements.txt`.

### Use the GUI
Now you can launch the GUI from "src/main.py" and import csv files with the scores to be plotted.

## Building the program
If you want to not have to launch the script from within the environment in the terminal, follow these steps to create an executable.

### Installing Pyinstaller
You will have to manually install the pyinstaller package using `pip install pyinstaller`, since it is not included in the requirements.

### Using the spec files
To build the GUI program, run `pyinstaller spec/main.spec`. The executable will be in "dist/main".