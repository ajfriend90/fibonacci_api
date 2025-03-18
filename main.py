from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import sqlite3
import sys
sys.set_int_max_str_digits(1000000)  # Increase limit to 1 million digits

app = FastAPI()

# Serve static files (Frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database setup
conn = sqlite3.connect("fibonacci.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS fib_cache (n INTEGER PRIMARY KEY, result TEXT)")
conn.commit()

# Fibonacci function with database caching
def calculate_fibonacci(n):
    if n > 100000:
        raise HTTPException(status_code=400, detail="Number too large! Please enter a number ≤ 100,000.")
    
    cursor.execute("SELECT result FROM fib_cache WHERE n=?", (n,))
    result = cursor.fetchone()
    if result:
        return int(result[0])  # Return cached result as int

    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Constant space dynamic programming approach
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr  # Only keep last two values

    result = curr

    # Store the result in the database
    cursor.execute("INSERT INTO fib_cache (n, result) VALUES (?, ?)", (n, str(result)))
    conn.commit()
    return result

@app.get("/fibonacci/{n}")
def get_fibonacci(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative.")
    return {"n": n, "fibonacci": calculate_fibonacci(n)}
