import React, { useContext, useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';

function Navbar() {
  const { user } = useContext(AuthContext);
  const [topics, setTopics] = useState([]);

  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/topics/');
        if (!response.ok) {
          throw new Error('Failed to fetch topics');
        }
        const data = await response.json();
        setTopics(data);
      } catch (error) {
        console.error('Error fetching topics:', error);
      }
    };

    fetchTopics();
  }, []);

  return (
    <nav className="navbar">
      <hr />
      <ul className="navbar-list">
        <li className="navbar-item">
          <Link to={user ? "/news" : "/"} style = {{textDecoration:'none'}}>Trang chủ</Link>
        </li>
        {/* <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
        <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
        <li className="navbar-item"><Link to="/finance">Tài chính</Link></li>
        <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li> */}
        {user && (
          <li className="navbar-item"><Link to="/save" style = {{textDecoration:'none'}}>Tin yêu thích</Link></li>
        )}
        
            {topics.map(topic => (
              <li key={topic.id} className="navbar-item">
                <Link to={`/topics/${topic.id}/news`} style = {{textDecoration:'none'}}>{topic.name}</Link>
              </li>
            ))}
       
      </ul>
      <hr />
    </nav>
  );
}

export default Navbar;

// import React, { useContext } from 'react';
// import { Link } from 'react-router-dom';
// import { AuthContext } from '../Contexts/AuthContext';

// function Navbar() {
//   const { user } = useContext(AuthContext); 
//   return (
//     <nav className="navbar">
//       <hr />
//       <ul className="navbar-list">
//         <li className="navbar-item">
//           <Link to={user ? "/news" : "/"}>Trang chủ</Link>
//         </li>
//         <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
//         <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
//         <li className="navbar-item"><Link to="/finance">Tài chính</Link></li>
//         <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li>
//         {user && (
//           <li className="navbar-item"><Link to="/save">Tin yêu thích</Link></li>
//         )}
//       </ul>
//       <hr />
//     </nav>
//   );
// }

// export default Navbar;


// // import React, { useContext } from 'react';
// // import { Link } from 'react-router-dom';
// // import { AuthContext } from '../Contexts/AuthContext'; // Import AuthContext

// // function Navbar() {
// //   const { user } = useContext(AuthContext); // Lấy user từ AuthContext

// //   return (
// //     <nav className="navbar">
// //             <hr />

// //       <ul className="navbar-list">
// //         <li className="navbar-item">
// //           <Link to={user ? "/news" : "/"}>Trang chủ</Link>
// //         </li>

// //         <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
// //         <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
// //         <li className="navbar-item"><Link to="/finance">Tài chính</Link></li>
// //         <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li>
        
// //         <li className="navbar-item"><Link to="/save">Tin tức đã lưu</Link></li>
// //       </ul>
// //       <hr />

// //     </nav>
// //   );
// // }

// // export default Navbar;



// // import React from 'react';
// // import { Link } from 'react-router-dom';

// // function Navbar() {
// //   return (
// //     <nav className="navbar">
// //       <ul className="navbar-list">
// //         <li className="navbar-item"><Link to="/news">Trang chủ</Link></li>
// //         <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
// //         <li className="navbar-item"><Link to="/petro">Xăng dầu</Link></li>
// //         <li className="navbar-item"><Link to="/finance/">Tài chính</Link></li>
// //         <li className="navbar-item"><Link to="/nongsan">Nông sản-Thực phẩm</Link></li>

// //       </ul>
// //     </nav>
// //   );
// // }

// // export default Navbar;
