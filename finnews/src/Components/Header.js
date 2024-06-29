import React, { useContext, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';
import ConfirmLogoutModal from './ConfirmLogoutModal'; 
import defaultAvatar from './icons/circle-user-round.png';
function Header() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setShowModal(false);
  };

  const handleAvatarClick = () => {
    setShowDropdown(!showDropdown);
  };

  const avatarSrc = user?.avatar ? user.avatar : defaultAvatar;

  return (
    <div className="header">
      <h1 className="header-title">FinNews</h1>

      <div className="header-buttons">
        <Link to="/search" className="header-register-btn">Tìm kiếm</Link>
        {user ? (
          <div className="header-avatar-container">
            <img
              src={avatarSrc}
              // alt="Avatar"
              className="header-avatar"
              onClick={handleAvatarClick}
            />
            {showDropdown && (
              <div className="header-dropdown">
                <Link to="/user">Xem thông tin</Link>
                <hr />
                <button onClick={() => setShowModal(true)}>Đăng xuất</button>
              </div>
            )}
          </div>
        ) : (
          <Link to="/login" className="header-login-btn">Đăng nhập</Link>
        )}
      </div>
      {showModal && (
        <ConfirmLogoutModal
          onConfirm={handleLogout}
          onCancel={() => setShowModal(false)}
        />
      )}
    </div>
  );
}

export default Header;




// import React, { useContext, useState } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { AuthContext } from '../Contexts/AuthContext';
// import ConfirmLogoutModal from './ConfirmLogoutModal'; 

// function Header() {
//   const { user, logout } = useContext(AuthContext);
//   const navigate = useNavigate();
//   const [showDropdown, setShowDropdown] = useState(false);
//   const [showModal, setShowModal] = useState(false);

//   const handleLogout = () => {
//     logout();
//     navigate('/');
//     setShowModal(false);
//   };

//   const handleAvatarClick = () => {
//     setShowDropdown(!showDropdown);
//   };


//   return (
//     <div className="header">
//       <h1 className="header-title">FinNews</h1>

//       <div className="header-buttons">
//         {user ? ( 
//           <div>  
//           <div className="header-register-btn">  
//           <Link to="/search" >Tìm kiếm</Link>  
//           </div>   
//           <div className="header-login-btn">
//             <img
//               src={user.avatar}  // Giả sử bạn có đường dẫn avatar trong user object
//               alt="Avatar"
//               className="header-avatar"
//               onClick={handleAvatarClick}
//             />
//             {showDropdown && (
//               <div className="header-dropdown">
//                 <Link to="/user" style={{paddingRight: '0px', width: '140px'}}>Xem thông tin</Link>
//                 <hr style={{paddingTop: '0px', paddingBottom: '0px'}} />
//                 <button onClick={() => setShowModal(true)} style={{paddingRight: '0px', width: '150px'}}>Đăng xuất</button>
//               </div>
//             )}
//           </div>
//           </div>
//         ) : (
//           <>
//             <Link to="/search" className="header-register-btn">Tìm kiếm</Link>
//             <Link to="/login" className="header-login-btn">Đăng nhập</Link>
//           </>
//         )}
//       </div>
//       {showModal && (
//         <ConfirmLogoutModal
//           onConfirm={handleLogout}
//           onCancel={() => setShowModal(false)}
//         />
//       )}
//     </div>
//   );
// }

// export default Header;


