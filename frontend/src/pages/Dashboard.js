// Dashboard.js
import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../utils/AuthContext';
import axios from '../services/axios';

function Dashboard() {
  const { isLoggedIn } = useContext(AuthContext);
  const [items, setItems] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [records, setRecords] = useState([]);
  const [newRecord, setNewRecord] = useState({ datetime: '', comment: '' });
  const [newItem, setNewItem] = useState({ name: '', description: '' });

  useEffect(() => {
    if (isLoggedIn) {
      fetchItems();
    }
  }, [isLoggedIn]);

  const fetchItems = async () => {
    try {
      const response = await axios.get('/items/');
      setItems(response.data.items);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
  };

  const fetchRecords = async (itemId) => {
    try {
      const response = await axios.get(`/items/${itemId}/records/`);
      setRecords(response.data.records);
    } catch (error) {
      console.error('Error fetching records:', error);
    }
  };

  const handleSelectItem = (item) => {
    setSelectedItem(item);
    fetchRecords(item.id);
  };

  const handleAddItem = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/items/', newItem);
      setItems([...items, { id: response.data.id, ...newItem }]);
      setNewItem({ name: '', description: '' });
    } catch (error) {
      console.error('Error adding item:', error);
    }
  };

  // Update the datetime format to match the backend's expected format
  const handleAddRecord = async (e) => {
    e.preventDefault();
    try {
      // Format datetime to include seconds
      const formattedRecord = {
        ...newRecord,
        datetime: new Date(newRecord.datetime).toISOString().slice(0, 19),
      };

      const response = await axios.post(`/items/${selectedItem.id}/records/`, formattedRecord);
      setRecords([...records, { id: response.data.id, ...formattedRecord }]);
      setNewRecord({ datetime: '', comment: '' });
    } catch (error) {
      console.error('Error adding record:', error);
    }
  };

  const handleDeleteItem = async (id) => {
    try {
      await axios.delete(`/items/${id}/`);
      setItems(items.filter((item) => item.id !== id));
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <h2>Your Tracking Items</h2>
      <form onSubmit={handleAddItem}>
        <input
          type="text"
          placeholder="Name"
          value={newItem.name}
          onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Description"
          value={newItem.description}
          onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
        />
        <button type="submit">Add Item</button>
      </form>
      <ul>
        {items.map((item) => (
          <li key={item.id} onClick={() => handleSelectItem(item)}>
            <strong>{item.name}</strong>: {item.description}
            <button onClick={() => handleDeleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {selectedItem && (
        <div>
          <h2>Records for {selectedItem.name}</h2>
          <form onSubmit={handleAddRecord}>
            <input
              type="datetime-local"
              value={newRecord.datetime}
              onChange={(e) => setNewRecord({ ...newRecord, datetime: e.target.value })}
              required
            />
            <input
              type="text"
              placeholder="Comment"
              value={newRecord.comment}
              onChange={(e) => setNewRecord({ ...newRecord, comment: e.target.value })}
            />
            <button type="submit">Add Record</button>
          </form>
          <ul>
            {records.map((record) => (
              <li key={record.id}>
                <strong>{new Date(record.datetime).toLocaleString()}</strong>: {record.comment}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Dashboard;