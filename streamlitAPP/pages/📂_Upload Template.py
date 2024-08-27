import streamlit as st
import pandas as pd
import numpy as np

st.logo('cropped-radem.png')
st.title('Prediction DataFrame Format Required')


df = pd.DataFrame({
    'client_id': np.random.randint(1000, 9999, size=10),  # Random client IDs
    'district':np.random.randint(100, 999, size=10),  # Example districts
    'client_catg':np.random.randint(100, 999, size=10),  # Client categories
    'region': np.random.randint(100, 999, size=10),  # Example regions
    'creation_date': pd.date_range(start='2020-01-01', periods=10, freq='ME').strftime('%Y-%m-%d'),  # Random dates
    'invoice_date': pd.date_range(start='2021-01-01', periods=10, freq='ME').strftime('%Y-%m-%d'),  # Random invoice dates
    'tarif_type': np.random.randint(10, 999, size=10),  # Tariff types
    'counter_number': np.random.randint(100, 999, size=10),  # Random counter numbers
    'counter_statue': np.random.randint(100, 999, size=10),  # Counter status
    'counter_code':np.random.randint(100, 999, size=10),  # Counter codes
    'reading_remarque': np.random.randint(100, 999, size=10),  # Remarks on readings
    'counter_coefficient': np.random.rand(10),  # Random coefficients
    'consommation_level_1': np.random.randint(50, 2000, size=10),  # Consumption levels
    'consommation_level_2': np.random.randint(50, 2000, size=10),
    'consommation_level_3': np.random.randint(0, 2000, size=10),
    'consommation_level_4': np.random.randint(0, 2000, size=10),
    'old_index':np.random.randint(100, 999, size=10),  # Old meter index
    'new_index': np.random.randint(100, 999, size=10),  # New meter index
    'months_number': np.random.randint(1, 12, size=10),  # Number of months
    'counter_type': np.random.choice(['ELEC', 'GAZ'], size=10),  # Counter types
    'target': np.random.choice([0, 1], size=10)
})

st.table(df)