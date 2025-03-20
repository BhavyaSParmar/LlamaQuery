# LlamaQuery

## 🚀 Architecture Breakdown of LlamaQuery: Natural Language to SQL Conversion

This section provides a detailed explanation of the architecture shown in the image. The architecture follows a structured pipeline where user queries in natural language are processed, converted into SQL, executed against a database, and the results are returned.

---

### 1️⃣ Context Feeding: User Input (LLM Prompt)

The user enters a natural language question that needs to be converted into an SQL query.

**Example:** _"Show me all Nike t-shirts in black color with size XL."_

**Metadata Processing (SQLAlchemy & Database Schema):**
- The system retrieves relevant schema information (tables, columns, relationships) using SQLAlchemy.
- The schema metadata helps the model understand the database structure for query generation.

**LLM Model (Llama 3.2 3B):**
- The Ollama-hosted Llama 3.2 3B model is used for natural language processing.
- The model takes the user query along with the schema metadata to generate SQL statements.

---

### 2️⃣ SQL Query Process

**Query Input:**
- The user’s natural language query and the metadata are passed to the query generation module.

**Query Generation:**
- The LLM converts the structured input into a valid SQL query.
- The generated query is optimized using proper joins, filters, and conditions.
- The system ensures syntactic correctness and aligns the SQL format with the database type (MySQL in this case).

---

### 3️⃣ Execution

**Database Execution:**
- The generated SQL query is executed against the connected MySQL database.
- The system supports various MySQL databases as per the user's configuration.

**Result Generation:**
- The executed query retrieves the results from the database.
- The results are then formatted and displayed in a structured manner using Streamlit.

---

## 🔹 Key Technologies Used

- **Language Model:** Ollama-hosted Llama 3.2 3B for NL to SQL conversion.
- **Database Connectivity:** SQLAlchemy for schema retrieval and MySQL query execution.
- **Query Optimization:** Ensures valid SQL queries with optimized performance.
- **Frontend & Execution:** Streamlit for user interaction and result visualization.

---

## 📌 Summary

This architecture enables users to seamlessly translate natural language queries into SQL queries using an LLM-powered workflow. The system automates query generation, optimization, and execution while ensuring metadata-driven accuracy.
