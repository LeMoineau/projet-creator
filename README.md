# projet-creator

## Installation

- add to your terminal Path the location of the current `dist/` folder
- to create your own `dist/` directory, run the command `pyinstaller --onefile main.py` (require `pip install pyinstaller`)

## Usage

After add to your terminal path the `dist/` directory, run the following commands
- `projet-creator <path-to-your-project>` (if no path specified, will create the project file in the current path where is running the command)
- `projet-creator check <task>` to check a project task

## Settings

To change and/or add tasks to your current project, you have 2 options

### For local change to the tasks

To change/add specific task to the current project, you can run the following commands
- `projet-creator rm <task>`
- `projet-creator add <task>`

### For global change to the tasks

To change/add task for all of the project currently created, you can run the following commands
- `projet-creator global rm <task>`
- `projet-creator global add <task>`

## Requirement

library need to run the projet
- os
- colorama