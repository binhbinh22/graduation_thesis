import React, { useState, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (username === 'admin' && password === '123456') {
      window.location.href = 'http://127.0.0.1:8000/admin';
    } else {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });
        if (response.ok) {
          const data = await response.json();
          console.log('User ID:', data.id);
          console.log('Username:', data.username);
          login({ id: data.id, username: data.username, token: data.token }); // Lưu toàn bộ thông tin user
          navigate('/news');
        } else {
          const data = await response.json();
          alert(data.message);
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Đăng nhập</button>
      </form>
      <div style={{ marginTop: '0px', paddingLeft: '40px', paddingTop: '20px' }}> 
        Bạn chưa có tài khoản? 
        <Link to="/register" style={{ textDecoration: 'none' }}> Đăng ký</Link>
      </div>
    </div>
  );
};

export default Login;


// import React, { useState, useContext } from 'react';
// import { Link, useNavigate } from 'react-router-dom';
// import { AuthContext } from '../Contexts/AuthContext';

// const Login = () => {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const { login } = useContext(AuthContext);
//   const navigate = useNavigate();

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (username === 'admin' && password === '123456') {
//       window.location.href = 'http://127.0.0.1:8000/admin';
//     } else {
//       try {
//         const response = await fetch('http://127.0.0.1:8000/api/login/', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify({ username, password }),
//         });
//         if (response.ok) {
//           const data = await response.json();
//           console.log('User ID:', data.id);
//           console.log('Username:', data.username);
//           console.log('Password:', password); // Note: This is just for demonstration, avoid logging passwords in a real application
//           login(username);
//           navigate('/news');
//         } else {
//           const data = await response.json();
//           alert(data.message);
//         }
//       } catch (error) {
//         console.error('Error during login:', error);
//       }
//     }
//   };

//   return (
//     <div className="login-container">
//       <form onSubmit={handleSubmit}>
//         <input
//           type="text"
//           placeholder="Username"
//           value={username}
//           onChange={(e) => setUsername(e.target.value)}
//           required
//         />
//         <input
//           type="password"
//           placeholder="Password"
//           value={password}
//           onChange={(e) => setPassword(e.target.value)}
//           required
//         />
//         <button type="submit">Đăng nhập</button>
//       </form>
//       <div style={{marginTop: '0px' , paddingLeft: '40px',paddingTop: '20px'}}> Bạn chưa có tài khoản? 
//       <Link to="/register" style={{textDecoration: 'none'}}>     Đăng ký</Link></div>
//     </div>
//   );
// };

// export default Login;

// // import React, { useState, useContext } from 'react';
// // import { useNavigate } from 'react-router-dom';
// // import { AuthContext } from '../Contexts/AuthContext';

// // const Login = () => {
// //   const [username, setUsername] = useState('');
// //   const [password, setPassword] = useState('');
// //   const { login } = useContext(AuthContext);
// //   const navigate = useNavigate();

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     if (username === 'admin' && password === '123456') {
// //       window.location.href = 'http://127.0.0.1:8000/admin';
// //     } else {
// //       try {
// //         const response = await fetch('http://127.0.0.1:8000/api/login/', {
// //           method: 'POST',
// //           headers: {
// //             'Content-Type': 'application/json',
// //           },
// //           body: JSON.stringify({ username, password }),
// //         });
// //         if (response.ok) {
// //           login(username);
// //           navigate('/news');
// //         } else {
// //           const data = await response.json();
// //           alert(data.message);
// //         }
// //       } catch (error) {
// //         console.error('Error during login:', error);
// //       }
// //     }
// //   };

// //   return (
// //     <div className="login-container">
// //       <form onSubmit={handleSubmit}>
// //         <input
// //           type="text"
// //           placeholder="Username"
// //           value={username}
// //           onChange={(e) => setUsername(e.target.value)}
// //           required
// //         />
// //         <input
// //           type="password"
// //           placeholder="Password"
// //           value={password}
// //           onChange={(e) => setPassword(e.target.value)}
// //           required
// //         />
// //         <button type="submit">Đăng nhập</button>
// //       </form>
// //     </div>
// //   );
// // };

// // export default Login;



// // const ConfirmLogoutModal = ({ onConfirm, onCancel }) => {
// //   return (
// //     <div className="modal-overlay">
// //       <div className="modal-content">
// //         <h2>Đăng xuất</h2>
// //         <p>Bạn có muốn đăng xuất?</p>
// //         <div className="modal-buttons">
// //           <button onClick={onConfirm} className="confirm-btn">Có</button>
// //           <button onClick={onCancel} className="cancel-btn">Huỷ</button>
// //         </div>
// //       </div>
// //     </div>
// //   );
// // };

// // export default ConfirmLogoutModal;
