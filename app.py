import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_ollama import ChatOllama
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import chain
from sqlalchemy import inspect
from langchain_community.utilities.sql_database import SQLDatabase

# ✅ Correct SQLAlchemy Connection for SQL Server with PyODBC
def get_db_connection():
    try:
        connection_string = "mssql+pyodbc://sa:bebo@123@SURFACELAPPY:1433/mydb?driver=ODBC+Driver+17+for+SQL+Server"
        
        # ✅ Create SQLAlchemy Engine
        engine = create_engine(connection_string, pool_size=10, max_overflow=20)

        # ✅ Create Session
        Session = sessionmaker(bind=engine)
        session = Session()

        return engine  # ✅ Return engine instead of raw connection

    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

# ✅ Initialize LLM (Llama3)
@st.cache_resource
def init_llm():
    return ChatOllama(
        model='llama3:latest',
        base_url='http://localhost:11434',
        temperature=0.7
    )

# ✅ Function to Fetch Dynamic Database Schema
def get_dynamic_schema_context(db):
    """Fetch schema info dynamically using SQLAlchemy"""
    try:
        inspector = inspect(db)
        tables = inspector.get_table_names()
        
        schema_context = f"Database Schema Information:\n"
        for table in tables:
            schema_context += f"- `{table}`\n"
            columns = inspector.get_columns(table)
            column_info = [f"{col['name']} ({col['type']}){' PRIMARY KEY' if col.get('primary_key', False) else ''}" for col in columns]
            schema_context += "  - " + "\n  - ".join(column_info) + "\n"
        return schema_context
    except Exception as e:
        st.error(f"Error fetching schema: {str(e)}")
        return "Could not fetch schema information"

# ✅ Chain to Generate SQL Queries Based on User Input
@st.cache_resource
def get_sql_chain(_llm, _db):
    CUSTOM_CONTEXT = f"""You are an expert SQL query generator. Follow these rules:
1. **Schema Awareness**: {get_dynamic_schema_context(_db)}
2. **Query Optimization**: Select only needed columns, use proper filters
3. **JOINs**: Use INNER JOIN for required relationships
4. **Aggregation**: Include GROUP BY with aggregate functions
5. **Filtering**: Always add LIMIT 5 unless specified
6. **Format**: Return ONLY SQL query, no explanations"""

    return create_sql_query_chain(_llm, _db) | (lambda query: {
        "context": CUSTOM_CONTEXT + "\nSchema:\n" + _db.get_table_info(),
        "question": query
    })

# ✅ LLM Query Execution Chain
@chain
def get_correct_sql_query(input):
    context = input['context']
    question = input['question']

    instruction = f"""Use above context to fetch the correct SQL query for following question:
    {question}

    Do not enclose query in ```sql and do not write preamble and explanation.
    You MUST return only a single SQL query."""

    return ask_llm(context=context, question=instruction)

# ✅ Streamlit UI
st.title("AD-HOC-QL")

# ✅ Sidebar UI for Database Connection
with st.sidebar:
    st.header("Database Connection")
    db_host = st.text_input("Host", value="SURFACELAPPY")
    db_port = st.number_input("Port", value=1433)
    db_name = st.text_input("Database Name", value="mydb")

    if st.button("Connect"):
        # Store credentials in session state
        st.session_state.db_config = {
            'host': db_host,
            'port': db_port,
            'name': db_name
        }
        conn = get_db_connection()
        if conn:
            st.success("✅ Successfully connected to SQL Server!")
        else:
            st.error("❌ Failed to connect to SQL Server.")

# ✅ User Input for Ad-Hoc Queries
question = st.text_input("Enter your question about the data:", 
                        placeholder="What's your ad-hoc?")

if st.button("Generate Ad-Hoc Results"):
    st.cache_resource.clear()
    if not question:
        st.warning("Please enter a question first!")
        st.stop()
        
    with st.spinner("Processing your query..."):
        try:
            # Initialize Components
            llm = init_llm()
            db_engine = get_db_connection()
            if not db_engine:
                st.error("Database connection failed! Check your credentials.")
                st.stop()

            db = SQLDatabase(db_engine)  # ✅ Fixed: Use SQLDatabase(db_engine) instead of from_engine()
            sql_chain = get_sql_chain(llm, db)
            
            # Generate Initial Query
            raw_query = sql_chain.invoke({'question': question})
            
            # Get Corrected Query
            corrected_query = get_correct_sql_query.invoke({
                'context': raw_query,
                'question': question
            })
            
            # Execute and Display Results
            result = db.run(corrected_query)
            
            # Improved result handling for multiple rows
            st.write("Query Results:")
            try:
                if result.startswith("[(") and result.endswith(")]"):
                    rows = eval(result)
                    for row in rows:
                        if len(row) == 1:  # Single column
                            st.write(f"- {row[0]}")
                        else:  # Multiple columns
                            st.write(" | ".join(str(x) for x in row))
                else:
                    st.write(result)
            except:
                st.write(result)
            
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
