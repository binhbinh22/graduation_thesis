import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext'; // Import AuthContext

function Navbar() {
  const { user } = useContext(AuthContext); // Lấy user từ AuthContext

  return (
    <nav className="navbar">
      <hr />
      <ul className="navbar-list">
        <li className="navbar-item">
          <Link to={user ? "/news" : "/"}>Trang chủ</Link>
        </li>
        <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
        <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
        <li className="navbar-item"><Link to="/finance">Tài chính</Link></li>
        <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li>
        {user && (
          <li className="navbar-item"><Link to="/save">Tin yêu thích</Link></li>
        )}
      </ul>
      <hr />
    </nav>
  );
}

export default Navbar;


// import React, { useContext } from 'react';
// import { Link } from 'react-router-dom';
// import { AuthContext } from '../Contexts/AuthContext'; // Import AuthContext

// function Navbar() {
//   const { user } = useContext(AuthContext); // Lấy user từ AuthContext

//   return (
//     <nav className="navbar">
//             <hr />

//       <ul className="navbar-list">
//         <li className="navbar-item">
//           <Link to={user ? "/news" : "/"}>Trang chủ</Link>
//         </li>

//         <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
//         <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
//         <li className="navbar-item"><Link to="/finance">Tài chính</Link></li>
//         <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li>
        
//         <li className="navbar-item"><Link to="/save">Tin tức đã lưu</Link></li>
//       </ul>
//       <hr />

//     </nav>
//   );
// }

// export default Navbar;



// import React from 'react';
// import { Link } from 'react-router-dom';

// function Navbar() {
//   return (
//     <nav className="navbar">
//       <ul className="navbar-list">
//         <li className="navbar-item"><Link to="/news">Trang chủ</Link></li>
//         <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
//         <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
//         <li className="navbar-item"><Link to="/finance/">Tài chính</Link></li>
//         <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li>

//       </ul>
//     </nav>
//   );
// }

// export default Navbar;
