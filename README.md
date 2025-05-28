# Candidate Elimination Algorithm Tool

A professional GUI application for the Candidate Elimination Algorithm, designed to process CSV data and visualize machine learning results.

## Features

- **Professional GUI Interface**: Clean, tabbed interface built with tkinter
- **CSV File Import**: Easy file selection with drag-and-drop support
- **Flexible Configuration**: Customizable positive/negative class indicators
- **Data Preview**: Interactive table showing your CSV data
- **Results Display**: Formatted output showing Final S and Final G hypotheses
- **History Management**: Keep track of all processing sessions
- **Export Results**: Save results to text files for later reference

## System Requirements

- Windows 7/8/10/11 (64-bit)
- Python 3.7 or later
- Minimum 4GB RAM
- 100MB free disk space

## Quick Start

1. **Launch the Application**: Double-click the desktop icon or use the Start Menu
2. **Load Data**: Click "Browse CSV File" and select your data file
3. **Configure Settings**: Set your positive/negative indicators (default: Yes/No)
4. **Process**: Click "🚀 Process Data" to run the algorithm
5. **View Results**: See the Final S and Final G hypotheses in the Results tab

## Data Format

Your CSV file should:
- Have headers in the first row
- Include all feature columns followed by the target column (last column)
- Use consistent values for positive/negative cases (e.g., "Yes"/"No", "True"/"False")

## Sample Data

The application includes sample CSV files in the `sample_data` folder:
- `data.csv` - Basic example dataset
- `driving_behavior.csv` - Driving behavior classification
- `test_data.csv` - Additional test data

## Troubleshooting

**Python Not Found**: Ensure Python 3.7+ is installed and added to your system PATH.

**Missing Dependencies**: The application will automatically install required packages (pandas, tkinter).

**CSV Import Issues**: Verify your CSV file has proper formatting and encoding (UTF-8 recommended).

## Version History

- **v1.0.0** - Initial release with full GUI functionality

## Support

For issues or questions, please check the documentation or contact support.