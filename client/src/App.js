import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Home from './home';
import Login from './login';

function App() {

    const [ user, setUser ] = useState([]);
    const [ profile, setProfile ] = useState([]);
    useEffect(() => {
        const loggedInUser = localStorage.getItem("user");
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
    if (user) {
        return <Home></Home>;
    }
    return <Login></Login>

  }
export default App;