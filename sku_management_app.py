import sqlite3
import streamlit as st
import pandas as pd

# Connect to the database
def get_database_connection():
    conn = sqlite3.connect("sku.db")
    return conn

# Assign SKUs
def assign_skus(quantity):
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT base_number, suffix FROM skus WHERE used = 0 LIMIT ?", (quantity,))
    rows = c.fetchall()
    if not rows or len(rows) < quantity:
        return None
    assigned_skus = [f"{base}-{suffix}" for base, suffix in rows]
    for base, suffix in rows:
        c.execute("UPDATE skus SET used = 1 WHERE base_number = ? AND suffix = ?", (base, suffix))
    conn.commit()
    conn.close()
    return assigned_skus

# Get used SKUs
def get_used_skus():
    conn = get_database_connection()
    c = conn.cursor()
    c.execute("SELECT base_number, suffix FROM skus WHERE used = 1")
    rows = c.fetchall()
    conn.close()
    return [f"{base}-{suffix}" for base, suffix in rows]

# Streamlit app
st.title("SKU Generator App")
st.write("Generate unique SKUs with ease.")

# Input for the number of SKUs to assign
quantity = st.number_input("How many SKUs do you need?", min_value=1, step=1, key="unique_sku_quantity")

if st.button("Generate SKUs"):
    skus = assign_skus(quantity)
    if skus:
        st.success(f"Generated {quantity} SKUs:")
        st.write(skus)
    else:
        st.error("Not enough SKUs available.")

# Admin Section to View Used SKUs
st.header("Admin View: Used SKUs")
if st.button("View Used SKUs"):
    used_skus = get_used_skus()
    if used_skus:
        st.write("The following SKUs have been used:")
        st.write(used_skus)

        # Create a DataFrame for download
        used_df = pd.DataFrame({"Used SKUs": used_skus})

        # Create an in-memory buffer
        import io
        excel_buffer = io.BytesIO()
        used_df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)

        # Add a download button for the Excel file
        st.download_button(
            label="Download Used SKUs as Excel",
            data=excel_buffer,
            file_name="used_skus.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    else:
        st.info("No SKUs have been used yet.")

