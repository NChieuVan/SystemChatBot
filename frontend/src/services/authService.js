// authService.js: Wrapper for login/register/logout using backend API
// Usage: import { login, register, logout, getToken, authHeader } from './authService';

const API_BASE = typeof import.meta !== 'undefined' && import.meta.env && import.meta.env.VITE_API_URL
  ? import.meta.env.VITE_API_URL
  : '';

function buildUrl(path) {
  if (!API_BASE) return path;
  return `${API_BASE.replace(/\/$/, '')}${path}`;
}

export async function login(email, password) {
  const url = buildUrl('/api/auth/login');
  const body = new URLSearchParams();
  body.append('email', email);
  body.append('password', password);

  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: body.toString()
  });

  if (!res.ok) {
    let errDetail = res.statusText;
    try {
      const err = await res.json();
      errDetail = err.detail || err.error || JSON.stringify(err);
    } catch (_) {}
    throw new Error(errDetail || `HTTP ${res.status}`);
  }

  const data = await res.json();
  if (data.access_token) {
    localStorage.setItem('token', data.access_token);
  }
  return data;
}

export async function register(email, password, name) {
  const url = buildUrl('/api/auth/register');
  const body = new URLSearchParams();
  body.append('email', email);
  body.append('password', password);
  if (name) body.append('name', name);

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString()
  });

  if (!res.ok) {
    let errDetail = res.statusText;
    try {
      const err = await res.json();
      errDetail = err.detail || err.error || JSON.stringify(err);
    } catch (_) {}
    throw new Error(errDetail || `HTTP ${res.status}`);
  }

  return res.json();
}

export function logout() {
  localStorage.removeItem('token');
}

export function getToken() {
  return localStorage.getItem('token');
}

export function authHeader() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

export default {
  login,
  register,
  logout,
  getToken,
  authHeader
};
