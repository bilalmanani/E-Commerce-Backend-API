import React, { useEffect, useState } from 'react';
import { User as UserIcon, Lock, CheckCircle2, AlertCircle } from 'lucide-react';
import api from '../api/axios';
import { User } from '../types';

export const UserProfile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  
  // Password state
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  
  const [profileMsg, setProfileMsg] = useState<string | null>(null);
  const [passwordMsg, setPasswordMsg] = useState<string | null>(null);
  const [passwordErr, setPasswordErr] = useState<string | null>(null);

  useEffect(() => {
    api.get<User>('/users/me')
      .then((res) => {
        setUser(res.data);
        setFirstName(res.data.first_name);
        setLastName(res.data.last_name);
        setEmail(res.data.email);
      })
      .catch(() => {});
  }, []);

  const handleUpdateProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    setProfileMsg(null);
    try {
      const res = await api.put<User>('/users/me', {
        first_name: firstName,
        last_name: lastName,
        email
      });
      setUser(res.data);
      setProfileMsg('Profile updated successfully!');
      setTimeout(() => setProfileMsg(null), 3000);
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not update profile');
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordMsg(null);
    setPasswordErr(null);
    try {
      await api.post('/users/me/change-password', {
        current_password: currentPassword,
        new_password: newPassword
      });
      setPasswordMsg('Password changed successfully!');
      setCurrentPassword('');
      setNewPassword('');
      setTimeout(() => setPasswordMsg(null), 3000);
    } catch (err: any) {
      setPasswordErr(err.response?.data?.message || 'Could not change password');
    }
  };

  if (!user) return null;

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-8">
      <h1 className="text-3xl font-black text-gray-900">User Account & Profile</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Profile Information Form */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-6">
          <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
            <UserIcon className="w-5 h-5 text-indigo-600" />
            <span>Profile Details</span>
          </h2>

          {profileMsg && (
            <div className="bg-emerald-50 text-emerald-800 text-xs p-3 rounded-lg flex items-center space-x-2 font-medium">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>{profileMsg}</span>
            </div>
          )}

          <form onSubmit={handleUpdateProfile} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">First Name</label>
              <input
                type="text"
                required
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Last Name</label>
              <input
                type="text"
                required
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Email Address</label>
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-indigo-600 text-white font-bold text-xs py-2.5 rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Update Profile Details
            </button>
          </form>
        </div>

        {/* Change Password Form */}
        <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm space-y-6">
          <h2 className="text-lg font-bold text-gray-900 flex items-center space-x-2">
            <Lock className="w-5 h-5 text-indigo-600" />
            <span>Change Password</span>
          </h2>

          {passwordMsg && (
            <div className="bg-emerald-50 text-emerald-800 text-xs p-3 rounded-lg flex items-center space-x-2 font-medium">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>{passwordMsg}</span>
            </div>
          )}

          {passwordErr && (
            <div className="bg-red-50 text-red-800 text-xs p-3 rounded-lg flex items-center space-x-2 font-medium">
              <AlertCircle className="w-4 h-4 text-red-600" />
              <span>{passwordErr}</span>
            </div>
          )}

          <form onSubmit={handleChangePassword} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Current Password</label>
              <input
                type="password"
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">New Password</label>
              <input
                type="password"
                required
                minLength={8}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="w-full p-2.5 bg-gray-50 border border-gray-300 rounded-lg text-sm"
              />
            </div>

            <button
              type="submit"
              className="w-full bg-gray-900 text-white font-bold text-xs py-2.5 rounded-lg hover:bg-gray-800 transition-colors"
            >
              Update Password
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
