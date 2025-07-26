import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import DataTable from './DataTable';
import ChartComponent from './ChartComponent';

function App() {
  const [prompt, setPrompt] = useState('');
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [tableData, setTableData] = useState(null);
  const responseAreaRef = useRef(null);

  useEffect(() => {
    if (responseAreaRef.current) {
      responseAreaRef.current.scrollTop = responseAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    const userMessage = { sender: 'user', type: 'text', data: prompt };
    setMessages(prev => [...prev, userMessage]);
    setLoading(true);
    setPrompt('');

    try {
      const res = await axios.post('http://127.0.0.1:5000/process-prompt', {
        prompt: userMessage.data,
      });
      
      // The backend now returns an array of response objects
      const botResponses = res.data.map(response => ({ ...response, sender: 'bot' }));

      // If a table is part of the response, find it and save its data for future charts
      const newTableData = botResponses.find(msg => msg.type === 'table');
      if (newTableData) {
        setTableData(newTableData.data);
      }
      
      setMessages(prev => [...prev, ...botResponses]);

    } catch (error) {
      const errorMessage = { sender: 'bot', type: 'error', data: error.response?.data?.error || 'An unexpected error occurred.' };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="response-area" ref={responseAreaRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}-message`}>
            {msg.type === 'text' && <p>{msg.data}</p>}
            {msg.type === 'insights' && (
              <div className="insights">
                <h3>Automated Insights</h3>
                <p>{msg.data}</p>
              </div>
            )}
            {msg.type === 'table' && <DataTable data={msg.data} />}
            {msg.type === 'chart' && <ChartComponent spec={msg.spec} data={tableData} />}
            {msg.type === 'answer' && <p className="answer">{msg.data}</p>}
            {msg.type === 'error' && <p className="error">Error: {msg.data}</p>}
          </div>
        ))}
         {loading && <div className="message bot-message"><p>Processing...</p></div>}
      </div>
      <form onSubmit={handleSubmit} className="prompt-form">
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Load a file, ask a question, or request a chart"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          Submit
        </button>
      </form>
    </div>
  );
}

export default App;