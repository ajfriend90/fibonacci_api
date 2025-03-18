from fastapi import FastAPI
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect("fibonacci.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS fib_cache (n INTEGER PRIMARY KEY, result INTEGER)")
conn.commit()

# Fibonacci function with database caching
def calculate_fibonacci(n):
    cursor.execute("SELECT result FROM fib_cache WHERE n=?", (n,))
    result = cursor.fetchone()
    if result:
        return result[0]  # Return cached result

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
    cursor.execute("INSERT INTO fib_cache (n, result) VALUES (?, ?)", (n, result))
    conn.commit()
    return result

@app.get("/fibonacci/{n}")
def get_fibonacci(n: int):
    return {"n": n, "fibonacci": calculate_fibonacci(n)}
