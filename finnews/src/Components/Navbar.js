import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar">
      <ul className="navbar-list">
        <li className="navbar-item"><Link to="/">Trang chủ</Link></li>
        <li className="navbar-item"><Link to="/gold">Giá vàng</Link></li>
        <li className="navbar-item"><Link to="/stocks">Xăng dầu</Link></li>
        <li className="navbar-item"><Link to="/">Tài chính</Link></li>
        <li className="navbar-item"><Link to="/commodities">Nông sản</Link></li>
        <li className="navbar-item"><Link to="/">Thực phẩm</Link></li>

      </ul>
    </nav>
  );
}

export default Navbar;
