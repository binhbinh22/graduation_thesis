import React from 'react';
import './ConfirmLogoutModal.css'; 

const ConfirmLogoutModal = ({ onConfirm, onCancel }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Đăng xuất</h2>
        <p>Bạn có muốn đăng xuất?</p>
        <div className="modal-buttons">
          <button onClick={onConfirm} className="confirm-btn">Có</button>
          <button onClick={onCancel} className="cancel-btn">Huỷ</button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmLogoutModal;
