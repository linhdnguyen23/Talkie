import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Home from './home';
import Login from './login';
import { Navigate } from "react-router-dom";


function App() {

    const [ user, setUser ] = useState();
    const [ profile, setProfile ] = useState();
    const loggedInUser = localStorage.getItem("user");

    useEffect(() => {
        if (loggedInUser) {
            const foundUser = JSON.parse(loggedInUser);
            setUser(foundUser);
    }
    }, []);
    useEffect(
        () => {
            if (user) {
                axios
                    .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
                        headers: {
                            Authorization: `Bearer ${user.access_token}`,
                            Accept: 'application/json'
                        }
                    })
                    .then((res) => {
                        setProfile(res.data);
                    })
                    .catch((err) => console.log(err));
            }
        },
        [ user ]
    );
    if (loggedInUser) {
        return (<Navigate to="/home" replace={true} />)
    } else {
        return (<Navigate to="/login" replace={true} />)
    }

  }
export default App;