import React, { useState } from 'react';

import { useNavigate } from 'react-router-dom'
import { googleLogout } from '@react-oauth/google';

const Home = (props) => {
  const { loggedIn, email } = props
  const navigate = useNavigate()
  const [ profile, setProfile ] = useState([]);


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
          value={loggedIn ? 'Log out' : 'Log in'}
        />
        {loggedIn ? <div>Your email address is {email}</div> : <div />}
      </div>
    </div>
  )
}

export default Home