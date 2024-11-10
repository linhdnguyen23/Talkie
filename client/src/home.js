import React, { useState, useEffect } from 'react';
import axios from 'axios';

import { googleLogout } from '@react-oauth/google';

const Home = (props) => {
  const [ user, setUser ] = useState();
  const [ profile, setProfile ] = useState();

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

  // log out function to log the user out of google and set the profile array to null
  const logOut = () => {
      googleLogout();
      setProfile(null);
  };

  const onButtonClick = () => {

};

  return (
    <div className="mainContainer">
      <div className={'titleContainer'}>
        <div>Welcome!</div>
      </div>
      <div>This is the home page.</div>
      <div className={'buttonContainer'}>
        <input
          className={'inputButton'}
          type="button"
          onClick={onButtonClick}
          value={user ? 'Log out' : 'Log in'}
        />
        {profile ? <div>Your email address is {profile.email}</div> : <div />}
        {profile ? <div><img src={profile.picture}/></div> : <div />}
      </div>
    </div>
  )
}

export default Home