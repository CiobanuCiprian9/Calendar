import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Calendar from './app/calendarPage/calendar/calendarPage';
import AuthPage from './app/authPage/authPage';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import {Temporal} from "@js-temporal/polyfill";
if(!window.Temporal){
  window.Temporal=Temporal;
}
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/auth" element={<AuthPage />} />
      <Route path="/calendar" element={<Calendar />} />
      <Route path="/" element={<AuthPage />} />
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
