import React, { useState, useEffect } from 'react';

const FirewallManagement = () => {
  const [rules, setRules] = useState([]);
  const [newRule, setNewRule] = useState('');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRules = async () => {
      try {
        const response = await fetch('/api/firewall/rules');
        if (!response.ok) {
          throw new Error('Failed to fetch firewall rules');
        }
        const data = await response.json();
        setRules(data.rules);
      } catch (error) {
        setError('Failed to load firewall rules.');
      }
    };

    fetchRules();
  }, []);

  const handleAddRule = async () => {
    try {
      const response = await fetch('/api/firewall/rules', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule: newRule }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to add firewall rule');
      }
      setMessage(data.message);
      setRules([...rules, newRule]);
      setNewRule('');
    } catch (error) {
      setError(error.message);
    }
  };

  const handleDeleteRule = async (rule) => {
    try {
      const response = await fetch('/api/firewall/rules', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rule }),
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete firewall rule');
      }
      setMessage(data.message);
      setRules(rules.filter(r => r !== rule));
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className="firewall-management">
      <h2>Firewall Management</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <input
        type="text"
        placeholder="Enter new firewall rule"
        value={newRule}
        onChange={(e) => setNewRule(e.target.value)}
      />
      <button onClick={handleAddRule}>Add Rule</button>

      <h3>Existing Firewall Rules</h3>
      {rules.length > 0 ? (
        <ul>
          {rules.map((rule, index) => (
            <li key={index}>
              {rule} <button onClick={() => handleDeleteRule(rule)}>Delete</button>
            </li>
          ))}
        </ul>
      ) : (
        <p>No firewall rules available.</p>
      )}
    </div>
  );
};

export default FirewallManagement;
