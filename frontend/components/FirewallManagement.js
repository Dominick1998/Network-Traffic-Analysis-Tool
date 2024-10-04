import React, { useState } from 'react';

const FirewallManagement = () => {
  const [ipAddress, setIpAddress] = useState('');
  const [port, setPort] = useState('');
  const [protocol, setProtocol] = useState('');
  const [action, setAction] = useState('block');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const handleFirewallAction = async () => {
    const firewallData = {
      action,
      ip_address: ipAddress,
      port: port ? parseInt(port, 10) : undefined,
      protocol,
    };

    try {
      const response = await fetch('/api/firewall', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(firewallData),
      });
      if (!response.ok) {
        throw new Error('Failed to apply firewall rule');
      }
      const data = await response.json();
      setMessage(data.message);
      setError(null);
    } catch (error) {
      setMessage(null);
      setError('Failed to apply firewall rule.');
    }
  };

  const handleDeleteFirewallRule = async () => {
    const firewallData = {
      ip_address: ipAddress,
      port: port ? parseInt(port, 10) : undefined,
      protocol,
    };

    try {
      const response = await fetch('/api/firewall', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(firewallData),
      });
      if (!response.ok) {
        throw new Error('Failed to delete firewall rule');
      }
      const data = await response.json();
      setMessage(data.message);
      setError(null);
    } catch (error) {
      setMessage(null);
      setError('Failed to delete firewall rule.');
    }
  };

  return (
    <div className="firewall-management">
      <h2>Firewall Management</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <input
          type="text"
          placeholder="IP Address"
          value={ipAddress}
          onChange={(e) => setIpAddress(e.target.value)}
        />
        <input
          type="text"
          placeholder="Port (Optional)"
          value={port}
          onChange={(e) => setPort(e.target.value)}
        />
        <input
          type="text"
          placeholder="Protocol (Optional)"
          value={protocol}
          onChange={(e) => setProtocol(e.target.value)}
        />
        <select value={action} onChange={(e) => setAction(e.target.value)}>
          <option value="block">Block</option>
          <option value="allow">Allow</option>
        </select>
        <button onClick={handleFirewallAction}>Apply Rule</button>
        <button onClick={handleDeleteFirewallRule}>Delete Rule</button>
      </div>
    </div>
  );
};

export default FirewallManagement;
