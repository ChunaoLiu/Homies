import logo from './logo.svg';
import './App.css';
import axios from "axios";
import React, {Component} from "react";
import { NavLink, Routes, Route } from 'react-router-dom';
import About from './static/About';
import IntroFormat from './static/introFormat';

const Home = () => (
  <div className='home'>
    <h1>Welcome to my portfolio website</h1>
    <p> Feel free to browse around and learn more about me.</p>
  </div>
);

const Intro = () => (
  <div className='intro'>
    <introFormat/>
  </div>
);

const Contact = () => (
  <div className='contact'>
    <h1>Contact Me</h1>
    <p>You can reach me via email: <strong>hello@example.com</strong></p>
  </div>
);

const Main = () => (
  <Routes>
    <Route exact path='/' element={<IntroFormat/>}></Route>
    <Route exact path='/about' element={<About/>}></Route>
    <Route exact path='/contact' element={<Contact/>}></Route>
    <Route exact path='/intro' element={<introFormat/>}></Route>
  </Routes>
);

const Navigation = () => (
  <nav>
    <ul>
      <li><NavLink to='/'>Home</NavLink></li>
      <li><NavLink to='/about'>About</NavLink></li>
      <li><NavLink to='/contact'>Contact</NavLink></li>
    </ul>
  </nav>
);

function App() {
  return (
    <div className="App">
      <Main/>
      <header>
      </header>
      <introFormat/>
      <h1> Shit </h1>
    </div>
  );
}

export default App;
