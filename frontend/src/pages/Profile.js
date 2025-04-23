import React, { useState, useEffect } from 'react';
import { viewProfile, updateProfile } from '../services/axios';

function Profile() {
  const [profile, setProfile] = useState({ username: '', email: '' });
  const [editMode, setEditMode] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await viewProfile();
        setProfile(response.data);
      } catch (err) {
        setError('Failed to load profile.');
      }
    };
    fetchProfile();
  }, []);

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      await updateProfile(profile);
      setSuccess('Profile updated successfully!');
      setError('');
      setEditMode(false);
    } catch (err) {
      setError('Failed to update profile.');
      setSuccess('');
    }
  };

  return (
    <div className="profile-container">
      <h1>Profile</h1>
      {error && <p className="error-message">{error}</p>}
      {success && <p className="success-message">{success}</p>}
      {editMode ? (
        <form onSubmit={handleUpdate}>
          <div>
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={profile.username}
              onChange={(e) => setProfile({ ...profile, username: e.target.value })}
              required
            />
          </div>
          <div>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={profile.email}
              onChange={(e) => setProfile({ ...profile, email: e.target.value })}
              required
            />
          </div>
          <button type="submit">Save</button>
          <button type="button" onClick={() => setEditMode(false)}>Cancel</button>
        </form>
      ) : (
        <div>
          <p><strong>Username:</strong> {profile.username}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <button onClick={() => setEditMode(true)}>Edit Profile</button>
        </div>
      )}
    </div>
  );
}

export default Profile;