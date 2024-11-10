import React from 'react';
function Navbar() {

    return (
  
      <nav className="bg-pink-500 p-4">
  
        <div className="container mx-auto">
  
          <div className="flex justify-between items-center">
  
            <div className="text-white font-bold text-xl">Talkie</div>
  
            <div className="hidden md:flex space-x-4">
    
              <a href="#" className="text-white hover:text-gray-300">Login</a>
  
              <a href="#" className="text-white hover:text-gray-300">Sign up</a>
  
            </div>
  
          </div>
  
        </div>
  
      </nav>
  
    );
  
  }
  
export default Navbar;