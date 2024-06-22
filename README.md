# Budget Prediction Model
This project focuses on developing a budget prediction model using web scraping, API validation, and machine learning techniques. The primary tools and technologies used in this project include Selenium for web scraping, Postman for REST API validation, and Azure Machine Learning for building and deploying the prediction model.

## Project Overview

The goal of this project is to predict the overall budget and duration required for new projects. The model leverages data from the World Bank website, and the workflow involves:

1. **Web Scraping with Selenium**: Extracting relevant data from the World Bank website.
2. **API Validation with Postman**: Ensuring the accuracy and reliability of APIs used in the data pipeline.
3. **Machine Learning with Azure ML**: Building and deploying a predictive model for budget and duration estimation.

## Beneficiaries

- **Government Agencies and Organizations**: Responsible for project planning and funding.
- **Financial Institutions and Investors**: Gain a better understanding of potential project risks and returns.
- **Project Managers and Teams**: Benefit from more realistic expectations, proactive funding shortfall identification, and improved risk management with this tool.

## Machine Learning Model

We employed a decision forest regression model for our analysis. This model was chosen to predict the allocated amount for a particular project in a particular sector by identifying hidden patterns in the data.

### Evaluation Metrics

The following table summarizes the evaluation metrics for the different ML algorithms tried:

| S.No | Algo Name                   | Coeff of determination | Relative MAE | MAE       | R2       | RMSE     |
|------|-----------------------------|------------------------|--------------|-----------|----------|----------|
| 1    | Decision Forest Regression  | 0.4171                 | 0.7301       | 85.3694   | 0.5828   | 108.5929 |
| 2    | Neural Network Regression   | -0.00004               | 0.9995       | 116.8668  | 1.0004   | 142.2454 |
| 3    | Linear Regression           | 0.2801                 | 0.7794       | 91.1346   | 0.7198   | 120.6881 |
| 4    | Poisson Regression          | 0.2205                 | 0.7103       | 83.0567   | 0.7794   | 125.5834 |

## Model Accuracies and Fine-Tuning

To enhance model accuracy, we incorporated additional features such as India's GDP and per capita income, enriching the dataset. Simultaneously, rigorous data cleaning procedures were implemented to ensure the quality and reliability of the input data.

Initially, the coefficient of determination was 0.21%, which increased to 0.41%, indicating enhanced explanatory power and a better fit to the underlying data. However, with a coefficient of determination (R-squared) of 0.41%, the model still indicates substantial underfitting, suggesting that it does not accurately capture the variability in the data, leading to approximate performance but not 100% accuracy.

### Azure ML Pipeline

The model was trained, scored, and evaluated using Azure Machine Learning. Below is the pipeline used for real-time inference:

![Azure ML Pipeline](https://path-to-your-image/screenshot.png)

1. **Data Preparation**: Data was manually entered and processed through the training module.
2. **Model Training**: The model was trained using the training dataset.
3. **Model Scoring**: The trained model was scored using the scoring dataset.
4. **Model Evaluation**: The scored model was evaluated to assess its performance.
5. **Web Service**: The model was deployed as a web service for real-time inference.

## Data Collection

### Source
We selected [World Bank Data](https://data.worldbank.org/) as the target site for automation.

### Data Scraping Details
We scraped 187 pages and extracted data from the following web elements on each page:
- Project titles
- Project IDs
- Project status
- Commitment amounts
- Approval dates
- Closing dates (collected from individual project detail pages)

### Selenium Techniques Used
- **Navigation**: `driver.get()`, `driver.switch_to.window()`, `WebDriverWait`
- **Element Interaction**: `find_element` and `find_elements`, `click()`, `send_keys()`
- **Scrolling**: `execute_script("window.scrollTo(0, document.body.scrollHeight);")`
- **Data Extraction**: Text

### Problem Encountered
We encountered a stale element exception while attempting to access an element when the WebDriver was on one page. This was resolved by revisiting the target page to refresh the DOM before interacting with the desired element.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Jaswanthi220/Project-Budget-Prediction-model.git
    cd Project-Budget-Prediction
    ```

2. **Install the required packages**:
    ```bash
    pip install Selenium
    ```

3. **Set up Selenium**:
    - Download the appropriate WebDriver for your browser (e.g., ChromeDriver for Google Chrome).
    - Ensure the WebDriver is accessible in your system PATH.

4. **Configure Azure ML**:
    - Set up an Azure account and configure your workspace.
    - Update the `config.json` file with your Azure ML workspace details.

## Usage

1. **Web Scraping**:
    - Run the Selenium script to scrape data from the World Bank website:
        ```bash
        python web_scraping.py
        ```

2. **API Validation**:
    - Use the Postman collection provided in the repository to validate the REST APIs.
    - Import the collection into Postman and run the tests.

3. **Model Training and Prediction**:
    - Use the Azure ML scripts to train and deploy the model:
        ```bash
        python train_model.py
        python deploy_model.py
        ```
    - Make predictions using the deployed model:
        ```bash
        python predict.py
        ```
