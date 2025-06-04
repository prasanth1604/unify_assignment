import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function App() {
  const [classes, setClasses] = useState([]);
  const [clientEmail, setClientEmail] = useState("");
  const [clientName, setClientName] = useState("");
  const [selectedClassId, setSelectedClassId] = useState("");
  const [myClasses, setMyClasses] = useState([]);
  const [checkEmail, setCheckEmail] = useState("");

  // Fetch all available classes
  useEffect(() => {
    axios.get(`${API_BASE}/classes/`)
      .then(res => setClasses(res.data))
      .catch(err => console.error("Error fetching classes:", err));
  }, []);

  const handleRegister = () => {
  if (!selectedClassId || !clientName || !clientEmail) {
    alert("Please fill in all details.");
    return;
  }

  axios.post(`${API_BASE}/book/`, {
    class_id: selectedClassId,
    client_name: clientName,
    client_email: clientEmail
  })
  .then(res => {
    alert(res.data.message);

    // Update class slots locally
    setClasses(prevClasses => 
      prevClasses.map(cls => {
        if (cls.id === parseInt(selectedClassId)) {
          return { ...cls, total_slots: cls.total_slots - 1 };
        }
        return cls;
      })
    );
  })
  .catch(err => {
    alert(err.response?.data?.message || "Registration failed");
  });
};


  const fetchMyClasses = () => {
    if (!checkEmail) {
      alert("Please enter your email to fetch registered classes.");
      return;
    }

    axios.get(`${API_BASE}/bookings/${checkEmail}/`)
      .then(res => {
        setMyClasses(res.data);
      })
      .catch(err => {
        alert(err.response?.data?.message || "Could not fetch classes.");
        setMyClasses([]);
      });
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>🏋️‍♀️ Fitness Classes</h1>
      <h2>Available Classes</h2>
      <ul>
        {classes.map(fitClass => (
          <li key={fitClass.id}>
            <div> CLASS ID :{fitClass.id}</div>
            <div>{fitClass.name}</div> 
            with {fitClass.Instructor} at {new Date(fitClass.time).toLocaleString()} — Slots: {fitClass.total_slots}
          </li>
        ))}
      </ul>

      <h2>Register for a Class</h2>
      <label>
        Name: <input value={clientName} onChange={e => setClientName(e.target.value)} />
      </label><br />
      <label>
        Email: <input value={clientEmail} onChange={e => setClientEmail(e.target.value)} />
      </label><br />
      <label>
        Class ID: <input value={selectedClassId} onChange={e => setSelectedClassId(e.target.value)} />
      </label><br />
      <button onClick={handleRegister}>Register</button>

      <h2>My Registered Classes</h2>
      <label>
        Email: <input value={checkEmail} onChange={e => setCheckEmail(e.target.value)} />
      </label><br />
      <button onClick={fetchMyClasses}>Show My Classes</button>
      <ul>
        {myClasses.map((cname, idx) => (
          <>
          <li key={cname.id}>{cname.name}</li>
            with {cname.Instructor} at {new Date(cname.time).toLocaleString()} 
          </>
        ))}
      </ul>
    </div>
  );
}

export default App;
