import React from "react";
import { useNavigate } from "react-router-dom";
import ReactDOM from 'react-dom';

const h1Style = {
    textAlign: 'center',
    margin: 'auto',
    padding: '30px 0'
  };

  const h2Style = {
    textAlign: 'center',
    margin: 'auto',
    padding: '10px 0'
  };

  const formStyle = {
    textAlign: 'center',
    margin: 'auto',
    border: '3px solid green',
    padding: '50px 50px',
    width: '400px',
    minHeight: '100px',
    height: 'auto'
  }

  const ButtonStyle = {
  textAlign:"center",
  margin:"auto",
  display:"inline",
  marginLeft:"100px",
  width:"70px",
  height:"40px"
}

const IntroFormat = (props) => {
    return (
        <div>
            <h1 style={h1Style}>
                Welcome to Homie!
            </h1>

            <h2 style={h2Style}>
                Please Login!
            </h2>
            <form style={formStyle}>
                <label for="email">Your Email:</label><br />
                <input type='text' id="Useremail" name="Useremail" ref="Useremail" /><br />
                <label for="password">Your Password:</label><br />
                <input type='text' id="Userpassword" name="Userpassword" ref="Userpassword" /><br /> 
            </form>
            <div style={{"textAlign":"center","paddingTop":"30px"}}>
                <button onclick={login()} style={ButtonStyle}>
                    Login
                </button>
                <button onclick={Redirect_signup()} style={ButtonStyle}>
                    Signup
                </button>
            </div>
        </div>
    );
};

const Redirect_signup = () => {
    const navigate= useNavigate();
    navigate('/Signup');
}

function login() {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    var raw = JSON.stringify({
        "email": ReactDOM.findDOMNode(this.refs.Useremail).value.trim(),
        "password": ReactDOM.findDOMNode(this.refs.Userpassword).value.trim()
    });
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    const url = "http://34.134.110.35:8000/Users/"
    fetch(url, requestOptions).then(response => response.text())
}


export default IntroFormat;