import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Search = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    navigate(`/search?query=${searchTerm}`);
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Nhập thông tin tìm kiếm"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <button type="submit">Tìm kiếm</button>
      </form>
    </div>
  );
};

export default Search;

// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// const Search = ({ onSearch }) => {
//   const [searchTerm, setSearchTerm] = useState('');
//   const navigate = useNavigate();

//   const handleSearch = (e) => {
//     e.preventDefault();
//     onSearch(searchTerm);
//     navigate('/search?q=' + searchTerm);
//   };

//   return (
//     <div className="search-container">
//     <form onSubmit={handleSearch} className="search-form">
//       <input
//         type="text"
//         placeholder="Nhập từ khoá tìm kiếm"
//         value={searchTerm}
//         onChange={(e) => setSearchTerm(e.target.value)}
//       />
//       <button type="submit">Tìm kiếm</button>
//     </form>
//     </div>
//   );
// };

// export default Search;



