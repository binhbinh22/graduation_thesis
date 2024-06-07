import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Search = () => {
  const [searchOptions, setSearchOptions] = useState([]);
  const [selectedKeywordId, setSelectedKeywordId] = useState(null);
  const [selectedKeywordName, setSelectedKeywordName] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSearchOptions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/searchs/');
        if (!response.ok) {
          throw new Error('Failed to fetch search options');
        }
        const data = await response.json();
        setSearchOptions(data);
      } catch (error) {
        console.error('Error fetching search options:', error);
      }
    };

    fetchSearchOptions();
  }, []);

  const handleKeywordClick = (keywordId, keywordName) => {
    setSelectedKeywordId(keywordId);
    setSelectedKeywordName(keywordName);
  };

  const handleNewsClick = async (newsId) => {
    try {
      const payload = {
        // user: user.id,
        news: newsId,
      };
  
      const response = await fetch('http://localhost:8000/api/read_news/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });
      console.log('Payload to be sent:', JSON.stringify(payload));

  
      if (!response.ok) {
        throw new Error('Failed to save read history');
      }
  
      // Nếu mọi thứ đều ok, chuyển hướng đến trang chi tiết tin tức
      navigate(`/news/${newsId}`);
    } catch (error) {
      console.error('Error saving read history:', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/news_search/${selectedKeywordId}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch search results');
      }
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error searching news:', error);
    }
  };

  return (
    <div className="search-container">
      <form onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Nhập thông tin tìm kiếm"
          value={selectedKeywordName}
          onChange={(e) => setSelectedKeywordName(e.target.value)}
        />
        <button type="submit">Tìm kiếm</button>
      </form>

      <div className="keyword-list">
        {searchOptions.map((option) => (
          <button
            key={option.id}
            className={selectedKeywordId === option.id ? 'keyword-button selected' : 'keyword-button'}
            onClick={() => handleKeywordClick(option.id, option.name)}
          >
            {option.name}
          </button>
        ))}
      </div>

      <div className="search-results">
        {searchResults.map((item) => (
          <Link to={`/news/${item.id}`} key={item.id} className="news-link">
          {/* <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}> */}
            <div className="news-item" style = {{ width:'800px'}}>
              <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
              <div className="news-item-content" style={{ flex: 1 }}>
                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content ? item.content.split('\n')[0] : ''}</p>
                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
              </div>
            </div>
            
          {/* </div> */}
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Search;












// import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

// const Search = () => {
//   const [searchTerm, setSearchTerm] = useState('');
//   const navigate = useNavigate();

//   const handleSearch = (e) => {
//     e.preventDefault();
//     navigate(`/search?query=${searchTerm}`);
//   };

//   return (
//     <div className="search-container">
//       <form onSubmit={handleSearch}>
//         <input
//           type="text"
//           placeholder="Nhập thông tin tìm kiếm"
//           value={searchTerm}
//           onChange={(e) => setSearchTerm(e.target.value)}
//         />
//         <button type="submit">Tìm kiếm</button>
//       </form>
//     </div>
//   );
// };

// export default Search;





