# Finance Data API
Python API that collects, stores and provides data on various financial data sets. Also can create graph visualisations of data sets.

### Data Sets:
#### Global:
- Food Index
- Energy Index
- All Commodities Index

#### Per Country
- Policy Interest Rate

#### Countires
- United Kingdom
- United States

## Install
> pip install -r requirements.txt

## Usage
Setup database and collect data
> python -m src.run

Create graph of data

> python -m src.analysis

Run API

> uvicorn src.api:app --reload