import React from 'react';

const InfoExtractModal = ({ isOpen, onClose, content }) => {
  if (!isOpen) return null;

  return (
    <div style={styles.modalOverlay}>
      <div style={styles.modalContent}>
        <h2>Thông tin quan trọng</h2>
        {content ? (
          <ul style={styles.list}>
            {content.split('\n').map((item, index) => (
              <li key={index} style={styles.listItem}>{item}</li>
            ))}
          </ul>
        ) : (
          <p style={styles.noContent}>Bài tin tức chưa được trích xuất</p>
        )}
        <button style={styles.button} onClick={onClose}>Đóng</button>
      </div>
    </div>
  );
};

const styles = {
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '8px',
    width: '500px',
    maxWidth: '90%',
    maxHeight: '80vh', // Giới hạn chiều cao modal
    overflowY: 'auto', // Thêm cuộn dọc
    boxShadow: '0 5px 15px rgba(0, 0, 0, 0.3)',
  },
  list: {
    listStyleType: 'none',
    padding: 0,
  },
  listItem: {
    marginBottom: '10px',
    padding: '10px',
    backgroundColor: '#f9f9f9',
    borderRadius: '4px',
  },
  noContent: {
    fontStyle: 'italic',
    color: 'gray',
  },
  button: {
    marginTop: '20px',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
};

export default InfoExtractModal;


// import React from 'react';

// const InfoExtractModal = ({ isOpen, onClose, content }) => {
//   if (!isOpen) return null;

//   return (
//     <div style={styles.modalOverlay}>
//       <div style={styles.modalContent}>
//         <h2>Thông tin quan trọng</h2>
//         {content ? (
//           <ul style={styles.list}>
//             {content.split('\n').map((item, index) => (
//               <li key={index} style={styles.listItem}>{item}</li>
//             ))}
//           </ul>
//         ) : (
//           <p style={styles.noContent}>Bài tin tức chưa được trích xuất</p>
//         )}
//         <button style={styles.button} onClick={onClose}>Đóng</button>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   modalOverlay: {
//     position: 'fixed',
//     top: 0,
//     left: 0,
//     right: 0,
//     bottom: 0,
//     backgroundColor: 'rgba(0, 0, 0, 0.5)',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//   },
//   modalContent: {
//     backgroundColor: 'white',
//     padding: '20px',
//     borderRadius: '8px',
//     width: '500px',
//     maxWidth: '90%',
//     boxShadow: '0 5px 15px rgba(0, 0, 0, 0.3)',
//   },
//   list: {
//     listStyleType: 'none',
//     padding: 0,
//   },
//   listItem: {
//     marginBottom: '10px',
//     padding: '10px',
//     backgroundColor: '#f9f9f9',
//     borderRadius: '4px',
//   },
//   noContent: {
//     fontStyle: 'italic',
//     color: 'gray',
//   },
//   button: {
//     marginTop: '20px',
//     padding: '10px 20px',
//     backgroundColor: '#007bff',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//   },
// };

// export default InfoExtractModal;

// import React from 'react';

// const InfoExtractModal = ({ isOpen, onClose, content }) => {
//   if (!isOpen) return null;

//   // Split the content by newlines to create an array of sentences
//   const contentArray = content.split('\n');

//   return (
//     <div style={styles.modalOverlay}>
//       <div style={styles.modalContent}>
//         <h2>Thông tin quan trọng</h2>
//         <ul style={styles.list}>
//           {contentArray.map((item, index) => (
//             <li key={index} style={styles.listItem}>{item}</li>
//           ))}
//         </ul>
//         <button style={styles.button} onClick={onClose}>Đóng</button>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   modalOverlay: {
//     position: 'fixed',
//     top: 0,
//     left: 0,
//     right: 0,
//     bottom: 0,
//     backgroundColor: 'rgba(0, 0, 0, 0.5)',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//   },
//   modalContent: {
//     backgroundColor: 'white',
//     padding: '20px',
//     borderRadius: '8px',
//     width: '500px',
//     maxWidth: '90%',
//     boxShadow: '0 5px 15px rgba(0, 0, 0, 0.3)',
//   },
//   list: {
//     listStyleType: 'none',
//     padding: 0,
//   },
//   listItem: {
//     marginBottom: '10px',
//     padding: '10px',
//     backgroundColor: '#f9f9f9',
//     borderRadius: '4px',
//   },
//   button: {
//     marginTop: '20px',
//     padding: '10px 20px',
//     backgroundColor: '#007bff',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//   },
// };

// export default InfoExtractModal;

// import React from 'react';

// const InfoExtractModal = ({ isOpen, onClose, content }) => {
//   if (!isOpen) return null;

//   return (
//     <div style={styles.modalOverlay}>
//       <div style={styles.modalContent}>
//         <h2>Thông tin quan trọng</h2>
//         <div>{content}</div>
//         <button style={styles.button} onClick={onClose}>Đóng</button>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   modalOverlay: {
//     position: 'fixed',
//     top: 0,
//     left: 0,
//     right: 0,
//     bottom: 0,
//     backgroundColor: 'rgba(0, 0, 0, 0.5)',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//   },
//   modalContent: {
//     backgroundColor: 'white',
//     padding: '20px',
//     borderRadius: '8px',
//     width: '500px',
//     maxWidth: '90%',
//   },
//   button: {
//     marginTop: '20px',
//     padding: '10px 20px',
//     backgroundColor: '#007bff',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//   },
// };

// export default InfoExtractModal;
