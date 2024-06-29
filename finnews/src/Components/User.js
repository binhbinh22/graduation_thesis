import React, { useState, useEffect, useContext } from 'react';
import ReadNews from './ReadNews';
import SaveNews from './SaveNews'; 
import SelectTag from './SelectTags'
import { AuthContext } from '../Contexts/AuthContext';

const User = () => {
  const [selectedSection, setSelectedSection] = useState('profile');
  const { user } = useContext(AuthContext);

  if (!user) {
    return <div>Loading...</div>; // Hoặc thông báo lỗi tùy thuộc vào tình huống của bạn
  }

  const renderSection = () => {
    switch (selectedSection) {
      case 'profile':
        return <Profile user={user} />;
      case 'saved':
        return <SaveNews />;
      case 'read':
        return <ReadNews />;
      case 'interests':
        return <SelectTag />;
      default:
        return <Profile user={user} />;
    }
  };

  return (
    <div className="user-container">
      <div className="sidebar">
        <button onClick={() => setSelectedSection('profile')}>Thông tin cá nhân</button>
        <button onClick={() => setSelectedSection('saved')}>Tin tức yêu thích</button>
        <button onClick={() => setSelectedSection('read')}>Lịch sử đọc tin</button>
        <button onClick={() => setSelectedSection('interests')}>Các chủ đề quan tâm</button>
      </div>
      <div className="content">
        {renderSection()}
      </div>
    </div>
  );
};

const Profile = ({ user }) => {
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    password: '',
  });
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/users/${user.id}/`, {
      headers: {
        'Authorization': `Bearer ${user.token}`, 
      },
    })
    .then(response => response.json())
    .then(data => {
      setProfileData({
        username: data.username,
        email: data.email,
        password: '',
      });
    })
    .catch(error => console.error('Error fetching user data:', error));
  }, [user.id, user.token]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setProfileData({ ...profileData, [name]: value });
  };

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleSaveClick = () => {
    fetch(`http://127.0.0.1:8000/api/users/${user.id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${user.token}`,
      },
      body: JSON.stringify(profileData),
    })
    .then(response => response.json())
    .then(data => {
      setProfileData({
        username: data.username,
        email: data.email,
        password: '',
      });
      setIsEditing(false);
    })
    .catch(error => console.error('Error saving user data:', error));
  };

  return (
    <div className="profile">
      <h2>Thông tin cá nhân</h2>
      {isEditing ? (
        <div className="profile-edit">
          <label>
            Tên người dùng:
            <input 
              type="text" 
              name="username" 
              value={profileData.username} 
              onChange={handleInputChange} 
            />
          </label>
          <label>
            Email:
            <input 
              type="email" 
              name="email" 
              value={profileData.email} 
              onChange={handleInputChange} 
            />
          </label>
          <label>
            Mật khẩu:
            <input 
              type="password" 
              name="password" 
              value={profileData.password} 
              onChange={handleInputChange} 
            />
          </label>
          <button onClick={handleSaveClick}>Lưu</button>
        </div>
      ) : (
        <div className="profile-view">
          <p><strong>Tên người dùng:</strong> {profileData.username}</p>
          <p><strong>Email:</strong> {profileData.email}</p>
          <button onClick={handleEditClick}>Chỉnh sửa</button>
        </div>
      )}
    </div>
  );
};

const InterestedTopics = () => (
  <div>
    <h2>Các chủ đề quan tâm</h2>
    {/* Thêm danh sách chủ đề quan tâm */}
  </div>
);

export default User;



// import React, { useState, useEffect, useContext } from 'react';
// import ReadNews from './ReadNews';
// import SaveNews from './SaveNews'; 
// import SelectTag from './SelectTags'
// import { AuthContext } from '../Contexts/AuthContext';

// const User = () => {
//     const [selectedSection, setSelectedSection] = useState('profile');
//     const { user } = useContext(AuthContext);

//     if (!user) {
//         return <div>Loading...</div>; // Hoặc thông báo lỗi tùy thuộc vào tình huống của bạn
//     }

//     const renderSection = () => {
//         switch (selectedSection) {
//             case 'profile':
//                 return <Profile user={user} />;
//             case 'saved':
//                 return <SaveNews />;
//             case 'read':
//                 return <ReadNews />;
//             case 'interests':
//                 return <SelectTag />;
//             default:
//                 return <Profile user={user} />;
//         }
//     };

//     return (
//         <div className="user-container">
//             <div className="sidebar">
//                 <button onClick={() => setSelectedSection('profile')}>Thông tin cá nhân</button>
//                 <button onClick={() => setSelectedSection('saved')}>Tin tức đã lưu</button>
//                 <button onClick={() => setSelectedSection('read')}>Tin tức đã đọc</button>
//                 <button onClick={() => setSelectedSection('interests')}>Các chủ đề quan tâm</button>
//             </div>
//             <div className="content">
//                 {renderSection()}
//             </div>
//         </div>
//     );
// };

// const Profile = ({ user }) => {
//     const [profileData, setProfileData] = useState({
//         username: '',
//         email: '',
//         password: '',
//     });
//     const [isEditing, setIsEditing] = useState(false);

//     useEffect(() => {
//         fetch(`http://127.0.0.1:8000/api/users/${user.id}/`, {
//             headers: {
//                 'Authorization': `Bearer ${user.token}`, // Assuming you are using token-based authentication
//             },
//         })
//         .then(response => response.json())
//         .then(data => {
//             setProfileData({
//                 username: data.username,
//                 email: data.email,
//                 password: '',
//             });
//         })
//         .catch(error => console.error('Error fetching user data:', error));
//     }, [user.id, user.token]);

//     const handleInputChange = (e) => {
//         const { name, value } = e.target;
//         setProfileData({ ...profileData, [name]: value });
//     };

//     const handleEditClick = () => {
//         setIsEditing(true);
//     };

//     const handleSaveClick = () => {
//         fetch(`http://127.0.0.1:8000/api/users/${user.id}/`, {
//             method: 'PUT',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': `Bearer ${user.token}`,
//             },
//             body: JSON.stringify(profileData),
//         })
//         .then(response => response.json())
//         .then(data => {
//             setProfileData({
//                 username: data.username,
//                 email: data.email,
//                 password: '',
//             });
//             setIsEditing(false);
//         })
//         alert('Chỉnh sửa thông tin thành công')
//         .catch(error => console.error('Error saving user data:', error));
//     };

//     return (
//         <div className="profile">
//             <h2>Thông tin cá nhân</h2>
//             {isEditing ? (
//                 <div className="profile-edit">
//                     <label>
//                         Tên người dùng:
//                         <input 
//                             type="text" 
//                             name="username" 
//                             value={profileData.username} 
//                             onChange={handleInputChange} 
//                         />
//                     </label>
//                     <label>
//                         Email:
//                         <input 
//                             type="email" 
//                             name="email" 
//                             value={profileData.email} 
//                             onChange={handleInputChange} 
//                         />
//                     </label>
//                     <label>
//                         Mật khẩu:
//                         <input 
//                             type="password" 
//                             name="password" 
//                             value={profileData.password} 
//                             onChange={handleInputChange} 
//                         />
//                     </label>
//                     <button onClick={handleSaveClick}>Lưu</button>
//                 </div>
//             ) : (
//                 <div className="profile-view">
//                     <p><strong>Tên người dùng:</strong> {profileData.username}</p>
//                     <p><strong>Email:</strong> {profileData.email}</p>
//                     <button onClick={handleEditClick}>Chỉnh sửa</button>
//                 </div>
//             )}
//         </div>
//     );
// };



// export default User;




