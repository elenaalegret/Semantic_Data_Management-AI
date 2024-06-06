#### BDA - GIA
<img src="App-Data_Analysis_pipeline1/images/logo.png" alt="BCN Map4Tourism Logo" width="150">

# Advanced-Databases: Semantic Data Management

### Elena Alegret, Júlia Orteu and Sergi Tomàs
## Authors
- Elena Alegret.
- Sergi Tomàs.
- Júlia Orteu

## Project Description
This project focuses on collecting and formatting data from diverse sources, specifically targeting Airbnb listings and criminal activity datasets. Our goal is to facilitate data analysis and insights by preparing and organizing data efficiently. The repository includes raw data collection scripts, metadata documentation, and a data formatting pipeline.

## BCN Map4Tourism Application
This application was originally developed using PySpark for data processing and filtering. In the new version, **we have migrated the filtering and querying operations to SPARQL to leverage a graph-based RDF approach**.

To run the application, navigate to the directory where the `app.py` file is located (`~/App-Data_Analysis_pipeline1` in this case) and execute the following command in your terminal:

```
streamlit run app.py
```

This command will start the Streamlit application defined in the `app.py` file. You can then access the application through your web browser by following the URL provided in the terminal output (typically `http://localhost:8501`).

> To access the last project interactive interface integrated into your web browser, visit the [BCN Map4Tourism interface](https://bcnmap4tourismin.streamlit.app).

## Directory Structure
```
.
├── REPORT.pdf
├── README.md
├── App-Data_Analysis_pipeline1
│   ├── SPARQL_queries.py
│   ├── app.py
│   └── images
│       └── logo.png
├── Model-Data_Analysis_pipeline2
│   └── model
│       ├── classifier.ipynb
│       ├── objects
│       │   ├── kg_train.pkl
│       │   ├── model.pkl
│       │   ├── test_X.pkl
│       │   ├── test_y.pkl
│       │   └── train.pkl
│       ├── test_X
│       │   ├── batch_0.npy
│       │   ├── batch_1000.npy
│       │   ├── batch_1500.npy
│       │   └── batch_500.npy
│       ├── train_X
│       │   ├── batch_0.npy
│       │   ├── batch_1000.npy
│       │   ├── batch_2000.npy
│       │   ├── batch_3000.npy
│       │   ├── batch_4000.npy
│       │   ├── batch_5000.npy
│       │   ├── batch_6000.npy
│       │   └── batch_7000.npy
│       └── transE.ipynb
├── data
│   ├── Metadata_Airbnb_Lisitings.md
│   ├── Metadata_Criminality_Barcelona.md
│   ├── Metadata_TripAdvisor_Locations.md
│   ├── Metadata_TripAdvisor_Reviews.md
│   ├── explotation_zone
│   │   ├── RDFGraph_Visualitzation.ttl
│   │   ├── barcelona_processed.db
│   │   ├── barcelona_processed.db.wal
│   │   └── barcelona_processed_emb.db
│   ├── formatted_zone
│   │   ├── barcelona.db
│   │   └── barcelona_processed.db
│   ├── landing_zone
│   │   ├── airbnb_listings.parquet
│   │   ├── criminal_dataset.parquet
│   │   ├── tripadvisor_locations.parquet
│   │   └── tripadvisor_reviews.parquet
│   └── trusted_zone
│       ├── Roboto-Light.ttf
│       └── barcelona_processed.db
├── data_collectors
│   ├── Metadata_Airbnb_Lisitings.md
│   ├── Metadata_Criminality_Barcelona.md
│   ├── Metadata_TripAdvisor_Locations.md
│   ├── Metadata_TripAdvisor_Reviews.md
│   ├── airnbnb_dataset.py
│   ├── criminal_dataset.py
│   ├── tripadvisor_places.py
│   └── tripadvisor_reviews.py
├── data_formatting_pipeline
│   ├── DataFormattingPipeline.py
│   └── sanity_check.py
├── data_preparation_pipeline
│   ├── 1-DataExplotationPipeline.ipynb
│   ├── 2-RDF_Visualitzation.ipynb
│   ├── 3-RDF_ModelEmb.ipynb
│   └── embeddedModelExplotation.ipynb
├── data_quality_pipeline
│   ├── 1-CriminalQualityPipeline.ipynb
│   ├── 2-AirbnbQualityPipeline.ipynb
│   ├── 3-TripadvisorQualityPipeline.ipynb
│   ├── DataQualityPipeline.ipynb
│   └── coordinates_dict.pkl
├── lib
│   ├── duckdb.jar
│   └── postgresql.jar
├── requirements.txt
└── utils.py

```
### REPORT
- A technical explanation of the project can be found in the `REPORT.pdf

### data
- **landing_zone**: Contains raw data files as they are collected from the data sources.
  - `airbnb_listings.parquet`: Raw data of Airbnb listings.
  - `criminal_dataset.parquet`: Raw criminal activity data.
  - `tripadvisor_locations.parquet`: Raw data of Tripadvisor locations.
  - `tripadvisor_reviews.parquet`: Raw data of Tripadvisor reviews.
- **formatted_zone**: Stores data after it has been processed and formatted for analysis.
  - `barcelona.db`: Formatted database of Barcelona data.
  - `barcelona_processed.db`: Processed database of Barcelona data.
- **explotation_zone**: Contains data used for analysis and visualization.
  - `RDFGraph_Visualitzation.ttl`: RDF graph visualization file.
  - `RDFGraph_Model_emb.ttl`: RDF graph visualization file.
  - `barcelona_processed.db`: Processed database for analysis.
  - `barcelona_processed_emb.db`: Processed database with embeddings.
- **trusted_zone**: Contains verified and trusted data.
  - `barcelona_processed.db`: Verified database of processed data.
  - `Roboto-Light.ttf`: Font file for visualizations.

### data_collectors
Scripts and metadata for data collection:
- **Metadata_Airbnb_Lisitings.md**: Documentation describing the structure and details of the Airbnb listings data.
- **Metadata_Criminality_Barcelona.md**: Documentation on the criminal dataset's structure and specifics.
- **Metadata_TripAdvisor_Locations.md**: Documentation on the structure and details of the Tripadvisor locations data.
- **Metadata_TripAdvisor_Reviews.md**: Documentation on the structure and details of the Tripadvisor reviews data.
- **airnbnb_dataset.py**: Script to collect Airbnb listings data.
- **criminal_dataset.py**: Script to collect criminal activity data.
- **tripadvisor_places.py**: Script to collect Tripadvisor locations data.
- **tripadvisor_reviews.py**: Script to collect Tripadvisor reviews data.


### data_formatting_pipeline
- **DataFormattingPipeline.py**: A Python script designed to format raw data into a structured form suitable for relational analysis. It includes functions to clean, transform, and standardize data, preparing it for analysis.
- **sanity_check.py**: Script used to perform initial checks on data to ensure its integrity before it enters the formatting pipeline.

### data_quality_pipeline
### data_quality_pipeline
Scripts and utilities designed to assess and improve the quality of data:
- **1-CriminalQualityPipeline.ipynb**: Jupyter Notebook for assessing and improving the quality of criminal activity data.
- **2-AirbnbQualityPipeline.ipynb**: Jupyter Notebook for assessing and improving the quality of Airbnb listings data.
- **3-TripadvisorQualityPipeline.ipynb**: Jupyter Notebook for assessing and improving the quality of Tripadvisor data.
- **DataQualityPipeline.ipynb**: Python script that implements checks and balances on the data, ensuring that data quality is maintained throughout processing.
- **coordinates_dict.pkl**: A pickle file containing pre-computed coordinates for use in validation or transformation processes.

### data_preparation_pipeline
- **1-DataExplotationPipeline.ipynb**: Jupyter Notebook for initial data exploration.
- **2-RDF_Visualitzation.ipynb**: Jupyter Notebook for visualizing RDF graphs.
- **3-RDF_ModelEmb.ipynb**: Jupyter Notebook for creating RDF model embeddings.
- **embeddedModelExplotation.ipynb**: Jupyter Notebook for exploring embedded models.

### App-Data_Analysis_pipeline1
- **SPARQL_queries.py**: Python script for executing SPARQL queries.
- **app.py**: Main application script.
- **images/logo.png**: Logo image for the application.

### Model-Data_Analysis_pipeline2
- **model/classifier.ipynb**: Jupyter Notebook for training and evaluating the classifier model.
- **model/objects**: Directory containing pickled model objects and training data.
  - `kg_train.pkl`: Knowledge graph training data.
  - `model.pkl`: Trained model.
  - `test_X.pkl`: Test features.
  - `test_y.pkl`: Test labels.
  - `train.pkl`: Training data.
- **model/test_X**: Directory containing test feature batches.
  - `batch_0.npy`, `batch_1000.npy`, `batch_1500.npy`, `batch_500.npy`: Test feature batches.
- **model/train_X**: Directory containing training feature batches.
  - `batch_0.npy`, `batch_1000.npy`, `batch_2000.npy`, `batch_3000.npy`, `batch_4000.npy`, `batch_5000.npy`, `batch_6000.npy`, `batch_7000.npy`: Training feature batches.
- **model/transE.ipynb**: Jupyter Notebook for training the TransE model.

### lib
- **duckdb.jar**: JDBC driver for DuckDB.
- **postgresql.jar**: JDBC driver for PostgreSQL.

### requirements.txt
- Contains all Python library dependencies required by the project, ensuring all data scripts run without issues. Use `pip install -r requirements.txt` to install these dependencies.

---


