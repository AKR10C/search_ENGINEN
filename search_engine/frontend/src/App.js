import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [maxPrice, setMaxPrice] = useState("");
  const [minRating, setMinRating] = useState("");
  const [sort, setSort] = useState("");
  const [searched, setSearched] = useState(false);
  const [darkMode, setDarkMode] = useState(true); // 🌙 toggle

  const handleSearch = async () => {
  if (!query.trim()) {
    alert("Please enter a search query");
    return;
  }

  setLoading(true);
  setSearched(true);

  try {
    let fullQuery = query;

    if (maxPrice) fullQuery += ` under ${maxPrice}`;
    if (minRating) fullQuery += ` rating above ${minRating}`;
    if (sort) fullQuery += ` ${sort}`;

    console.log("Query sent:", fullQuery);   // ✅ ADD THIS

    const response = await fetch(
      `https://search-enginen.onrender.com/search?q=${fullQuery}`
    );

    const data = await response.json();

    console.log("API DATA:", data);          // ✅ ADD THIS

    setResults(data.result || []);
  } catch (error) {
    console.error("ERROR:", error);          // ✅ ADD THIS
  }

  setLoading(false);
};

    setLoading(true);
    setSearched(true);

    try {
      let fullQuery = query;

      if (maxPrice) fullQuery += ` under ${maxPrice}`;
      if (minRating) fullQuery += ` rating above ${minRating}`;
      if (sort) fullQuery += ` ${sort}`;

      const response = await fetch(
        `https://search-enginen.onrender.com/search?q=${fullQuery}`,
      );

      const data = await response.json();
      setResults(data.result || []);
    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  // 🎨 theme styles
  const theme = {
    background: darkMode ? "#121212" : "#f5f7fa",
    text: darkMode ? "#ffffff" : "#000000",
    card: darkMode ? "#1e1e1e" : "#ffffff",
    input: darkMode ? "#2c2c2c" : "#ffffff",
  };

  return (
    <div
      style={{
        fontFamily: "Arial, sans-serif",
        backgroundColor: theme.background,
        color: theme.text,
        minHeight: "100vh",
        padding: "40px",
      }}
    >
      {/* 🌙 Toggle Button */}
      <div style={{ textAlign: "right" }}>
        <button
          onClick={() => setDarkMode(!darkMode)}
          style={{
            padding: "8px 15px",
            borderRadius: "8px",
            border: "none",
            cursor: "pointer",
          }}
        >
          {darkMode ? "☀ Light" : "🌙 Dark"}
        </button>
      </div>

      <h1 style={{ textAlign: "center" }}>🔍 Product Search</h1>

      {/* 🔍 Search Bar */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: "20px",
        }}
      >
        <input
          type="text"
          placeholder="Search products..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          style={{
            padding: "12px",
            width: "400px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: theme.input,
            color: theme.text,
            marginRight: "10px",
          }}
        />

        <button
          onClick={handleSearch}
          style={{
            padding: "12px 20px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: "#007bff",
            color: "white",
            cursor: "pointer",
          }}
        >
          Search
        </button>
      </div>

      {/* 🎛 Filters */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          marginTop: "20px",
          gap: "10px",
        }}
      >
        <input
          type="number"
          placeholder="Max Price"
          value={maxPrice}
          onChange={(e) => setMaxPrice(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: theme.input,
            color: theme.text,
          }}
        />

        <input
          type="number"
          placeholder="Min Rating"
          value={minRating}
          onChange={(e) => setMinRating(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "8px",
            border: "1px solid #ccc",
            backgroundColor: theme.input,
            color: theme.text,
          }}
        />

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          style={{
            padding: "10px",
            borderRadius: "8px",
            backgroundColor: theme.input,
            color: theme.text,
          }}
        >
          <option value="">Sort</option>
          <option value="low price">Low Price</option>
          <option value="high price">High Price</option>
          <option value="high rating">High Rating</option>
        </select>
      </div>

      {/* ⏳ Loading */}
      {loading && (
        <p style={{ textAlign: "center", marginTop: "20px" }}>Loading...</p>
      )}

      {/* ❌ No results */}
      {searched && !loading && results.length === 0 && (
        <p>No results found</p>
      )}

      {/* 📦 Results */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(250px, 1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        {results.map((item) => (
          <div
            key={item.id}
            style={{
              backgroundColor: theme.card,
              padding: "20px",
              borderRadius: "12px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
              textAlign: "center",
            }}
          >
            <h3>{item.name}</h3>
            <p style={{ fontWeight: "bold" }}>₹{item.price}</p>
            <p>⭐ {item.rating}</p>
          </div>
        ))}
      </div>
    </div>
  );

export default App;
