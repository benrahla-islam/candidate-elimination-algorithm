# Candidate Elimination Algorithm Tool

A GUI implementation of the Candidate Elimination Algorithm for processing CSV datasets and visualizing learning hypothesis evolution.

## Core Features

- **Tkinter GUI**: Professional tabbed interface with data preview
- **Flexible CSV Processing**: Configurable positive/negative class indicators
- **Algorithm Visualization**: Real-time display of Final S and Final G hypotheses
- **Session Management**: History tracking and result export

## Technical Requirements

- Python 3.7+
- Dependencies: `pandas`, `tkinter`
- Target column must be last column in CSV
- Binary classification format (customizable labels)

## Quick Start

```bash
python app.py
```

1. Load CSV file via GUI
2. Configure class indicators (default: "Yes"/"No")
3. Process data to get Final S/G hypotheses
4. Export results or view history

## Data Format

CSV structure:

```
feature1,feature2,...,featureN,target
value1,value2,...,valueN,Yes/No
```

- Last column = target variable
- Binary classification labels (configurable)
- Headers required

## Architecture

- `main.py`: Core Candidate Elimination algorithm implementation
- `app.py`: GUI wrapper with result management
- `results/`: Output directory for processed results and history

## Sample Data Included

- `data.csv`, `driving_behavior.csv`, `test_data.csv`