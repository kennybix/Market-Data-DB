# Automated Market Data Onboarding Project

## Overview

This project is designed to automate the collection, processing, and storage of market data and macroeconomic data for various countries and regions. The goal is to provide a completely free and highly efficient solution for accessing reliable market data. Unlike traditional data onboarding processes, this project utilizes advanced automation techniques to solve common challenges, including CAPTCHA verifications. A machine learning-based text recognition model is seamlessly integrated to handle these obstacles, ensuring uninterrupted data collection. 

Once the data is fetched, it undergoes rigorous cleaning and organization to make it ready for analysis. Additionally, the project employs Large Language Models (LLMs), specifically Groq, to generate detailed data dictionaries. These dictionaries enhance the usability of the data by providing comprehensive metadata and insights into its structure. This project supports a wide range of markets, including equities, ETFs, indices, cryptocurrencies, and macroeconomic indicators.

---

## Features

- **Automated Data Collection**: Implements web scraping techniques combined with Selenium and undetected ChromeDriver to fetch data from multiple sources, including regional markets such as the US, UK, and Hong Kong.
- **CAPTCHA Solving**: Utilizes the Alibaba DAMO Text Recognition model to automatically solve CAPTCHA challenges, ensuring a smooth and continuous data extraction process.
- **Comprehensive Market Coverage**: Supports the onboarding of data from diverse markets, including equities, ETFs, cryptocurrencies, and indices, as well as macroeconomic indicators.
- **Data Cleaning and Standardization**: Employs custom utilities to clean raw data files, remove inconsistencies, and standardize formats for analysis.
- **Data Dictionary Creation**: Leverages Groq LLMs to generate detailed metadata dictionaries for onboarded datasets, improving data discoverability and usability.
- **Structured Data Storage**: Stores processed data in an organized directory structure, categorized by region and data type (e.g., stocks, ETFs, macroeconomic indicators).
- **Global Reach**: Includes support for multiple regions and currencies, ensuring comprehensive global data coverage.

---

## Usage

1. **Automated Data Onboarding**:
   - The project scripts automate the process of fetching data from online sources.
   - CAPTCHAs encountered during the data extraction process are solved programmatically using an ML-based model.
   - The onboarded data is categorized by region and market type, cleaned, and saved in a structured format.

2. **Data Dictionary Exploration**:
   - Use the `data_dictionary.ipynb` notebook to create and explore metadata for the onboarded datasets.
   - The generated data dictionaries include detailed descriptions of each dataset's columns and values, enhancing their interpretability and usage.

3. **Market-Specific Data Management**:
   - The project supports separate pipelines for US, UK, and Hong Kong market data, as well as macroeconomic indicators for other regions.
   - Users can easily customize these pipelines to include additional regions or data sources.

---

## Project Structure

```plaintext
.
├── data_preprocessor.ipynb       # Notebook for preprocessing and cleaning
├── dp_utils.py                   # Utilities for data download, CAPTCHA handling, and cleaning
├── market_dp.py                  # Main script for orchestrating the data onboarding
├── data_dictionary.ipynb         # Data dictionary generation using LLM
├── raw/                          # Folder for storing raw data files
├── extracted_data/               # Folder for storing processed data
├── README.md                     # Project documentation
```

---

## Future Enhancements

- **Expanded Regional Support**: Add pipelines for additional regions, such as emerging markets and smaller economies.
- **Enhanced Data Quality Checks**: Integrate more advanced validation techniques to ensure the accuracy and completeness of the onboarded data.
- **Visualization Tools**: Develop interactive dashboards and visualizations for quick insights into market and macroeconomic data.
- **User-Friendly Interface**: Create a web-based interface for easier access and management of onboarded data.
- **Real-Time Updates**: Implement features to fetch and update market data in real-time.

---

## Contributing

Contributions are welcome! If you have suggestions for improving the project or adding new features, feel free to submit issues or pull requests.

---

## License

This project is licensed under the [MIT License](LICENSE).
