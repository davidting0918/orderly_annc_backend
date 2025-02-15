import { useEffect, useState } from "react";

function App() {
  // State to store fetched data
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = "http://localhost:8000/users/info?num=100"; // API Endpoint
        const apiKey = "a21e517c10cf09a245aff962a7c1e6ef"; // API Key
        const apiSecret = "3ee460f0e320971de84035266762ecba1bf8782f6b7891415093dcda20b3f79d"; // API Secret

        const response = await fetch(apiUrl, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "X-API-KEY": apiKey,
            "X-API-SECRET": apiSecret
          }
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        setUsers(data.data); // Assuming API returns { "users": [...] }
        setLoading(false); // Stop loading

      } catch (error) {
        console.error("Error fetching data:", error);
        setError("Failed to fetch user data");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>User Information</h1>

      {/* Show Loading Message */}
      {loading && <p>Loading data...</p>}

      {/* Show Error Message */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Display Fetched Users */}
      {!loading && !error && (
        <ul>
          {users.map((user, index) => (
            <li key={index}>
              <strong>{user.name}</strong> - {user.user_id}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
