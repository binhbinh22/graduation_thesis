import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <div className="footer-links">
            <p> Liên hệ: nguyenbinh.itvn02@gmail.com</p>
            {/* <a href="/contact">Contact</a> */}
            {/* <a href="/privacy">Privacy Policy</a>
            <a href="/terms">Terms of Service</a> */}
          </div>
        </div>
        <div className="footer-section">
          <div className="copyright">
            &copy; {new Date().getFullYear()} All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
