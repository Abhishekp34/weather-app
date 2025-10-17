import React, { useState } from 'react';
import api from './Services/api';

function App() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchWeather = async () => {
    setLoading(true);
    setError('');
    setForecast(null);
    try {
      const res = await api.get(`/weather?city=${city}`);
      setWeather(res.data);
    } catch (err) {
      setWeather(null);
      setError(err.response?.data?.error || 'Could not fetch weather.');
    }
    setLoading(false);
  };

  const fetchForecast = async () => {
    setLoading(true);
    setError('');
    setWeather(null);
    try {
      const res = await api.get(`/forecast?city=${city}`);
      setForecast(res.data['7_day_forecast'] || []);
    } catch (err) {
      setForecast(null);
      setError(err.response?.data?.error || 'Could not fetch forecast.');
    }
    setLoading(false);
  };

  return (
    <div style={{ maxWidth: '600px', margin: '30px auto', padding: '20px', background: '#fafafa', borderRadius: '8px' }}>
      <h2>Weather Microservice</h2>
      <input
        value={city}
        onChange={e => setCity(e.target.value)}
        placeholder="Enter city"
        style={{padding: '8px', fontSize: '16px'}}
      />
      <button onClick={fetchWeather} style={{margin: '0 10px'}}>Current Weather</button>
      <button onClick={fetchForecast}>7 Day Forecast</button>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {weather && (
        <div style={{margin: '20px 0', padding: '12px', border: '1px solid #ddd', borderRadius: '6px', background: '#fff'}}>
          <h3>{weather.city}</h3>
          <p>Description: {weather.description}</p>
          <p>Temperature: {weather.temperature}°C</p>
          <p>Humidity: {weather.humidity}%</p>
        </div>
      )}

      {forecast && (
        <div style={{marginTop: '20px'}}>
          <h3>7 Day Forecast</h3>
          {forecast.length === 0 && <p>No data.</p>}
          {forecast.map((day, idx) => (
            <div key={day.date || idx} style={{padding: '10px', border: '1px solid #eee', borderRadius: '5px', marginBottom: '8px', background: '#f7f7f7'}}>
              <strong>{day.date}</strong>
              <div>{day.weather_description}</div>
              <div>Min: {day.temperature_min}°C, Max: {day.temperature_max}°C, Humidity: {day.humidity}%</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
