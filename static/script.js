async function fetchFibonacci() {
    const numberInput = document.getElementById("numberInput");
    const number = parseInt(numberInput.value);
    const resultElement = document.getElementById("result");

    // 🚨 Add input validation
    if (isNaN(number) || number < 0) {
        resultElement.innerHTML = "❌ Please enter a valid positive number.";
        return;
    }
    if (number > 10000) {  // Set a reasonable max limit
        resultElement.innerHTML = "❌ Number too large! Please enter a number ≤ 10,000.";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/fibonacci/${number}`);
        if (!response.ok) {
            throw new Error("Failed to fetch Fibonacci number.");
        }
        const data = await response.json();
        resultElement.innerHTML = `✅ Fibonacci(${data.n}) = ${data.fibonacci}`;
    } catch (error) {
        resultElement.innerHTML = "❌ Error fetching data. API may be down.";
        console.error(error);
    }
}
