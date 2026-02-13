import axios from 'axios';

const serverBase =
  (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '');
const baseURL = `${serverBase}/api/v1`;

const instance = axios.create({ baseURL });

export default instance;
