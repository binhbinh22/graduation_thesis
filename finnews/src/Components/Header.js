import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';
import Search from './Search';

function Header() {
  const { user, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleSearch = (searchTerm) => {
    // This function can be used to perform any action on search
    console.log('Search term:', searchTerm);
  };

  return (
    <div className="header">
      <h1 className="header-title">FinNews</h1>
      <div className="header-search">
        <Search onSearch={handleSearch} /> {/* Đưa component Search vào Header */}
      </div>
      <div className="header-buttons">
        {user ? (
          <>
            <span className="header-user">Hello {user}</span>
            <button onClick={handleLogout} className="header-logout-btn">Đăng xuất</button>
            <Link to="/recommended-news" className="header-recommended-btn">Tin Khuyến Nghị</Link> {/* Thêm nút "Tin Khuyến Nghị" */}

          </>
        ) : (
          <>
            <Link to="/register" className="header-register-btn">Đăng ký</Link>
            <Link to="/login" className="header-login-btn">Đăng nhập</Link>
          </>
        )}
      </div>
    </div>
  );
}

export default Header;
