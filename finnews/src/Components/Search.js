import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Search.css';

const Search = () => {
  const [searchOptions, setSearchOptions] = useState([]);
  const [selectedKeywordId, setSelectedKeywordId] = useState('');
  const [selectedKeywordName, setSelectedKeywordName] = useState('');
  const [selectedRelation, setSelectedRelation] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showAdvancedSearch, setShowAdvancedSearch] = useState(false);
  const [showAdvancedSearch1, setShowAdvancedSearch1] = useState(false);

  const [relations, setRelations] = useState([]);
  const [reasons, setReasons] = useState([]);
  const [sentiments, setSentiments] = useState([]);
  const [selectedReasonId, setSelectedReasonId] = useState('');
  const [selectedSentiment, setSelectedSentiment] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const fetchSearchOptions = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/tags/');
        if (!response.ok) {
          throw new Error('Failed to fetch search options');
        }
        const data = await response.json();
        setSearchOptions(data);
      } catch (error) {
        console.error('Error fetching search options:', error);
      }
    };

    const fetchReasons = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/reason/');
        if (!response.ok) {
          throw new Error('Failed to fetch reasons');
        }
        const data = await response.json();
        setReasons(data);
      } catch (error) {
        console.error('Error fetching reasons:', error);
      }
    };

    fetchSearchOptions();
    fetchReasons();
  }, []);

  const highlightText = (text, keyword) => {
    if (!keyword) return text;
    const parts = text.split(new RegExp(`(${keyword})`, 'gi'));
    return parts.map((part, index) =>
      part.toLowerCase() === keyword.toLowerCase() ? (
        <span key={index} className="highlight1">{part}</span>
      ) : (
        part
      )
    );
  };

  const handleKeywordClick = async (keywordId, keywordName) => {
    setSelectedKeywordId(keywordId);
    setSelectedKeywordName(keywordName);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/relations/${keywordId}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch relations');
      }
      const data = await response.json();
      setRelations(data);
      setSelectedRelation(''); // Reset selected relation when changing keyword
      setSearchResults([]); // Reset search results when changing keyword
    } catch (error) {
      console.error('Error fetching relations:', error);
    }
  };

  const handleRelationClick = async (relation) => {
    setSelectedRelation(relation);
    setSearchResults([]); // Reset search results
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/news_tags/${selectedKeywordId}/${relation}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch search results');
      }
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error searching news:', error);
    }
  };

  const handleReasonClick = async (reasonId) => {
    setSelectedReasonId(reasonId);
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/sentiments/${reasonId}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch sentiments');
      }
      const data = await response.json();
      setSentiments(data);
      setSelectedSentiment(''); // Reset selected sentiment when changing reason
      setSearchResults([]); // Reset search results when changing reason
    } catch (error) {
      console.error('Error fetching sentiments:', error);
    }
  };

  const handleSentimentClick = async (sentiment) => {
    setSelectedSentiment(sentiment);
    setSearchResults([]); // Reset search results
    try {
      const response = await fetch(`http://127.0.0.1:8000/api/news_reason/${selectedReasonId}/${sentiment}/`);
      if (!response.ok) {
        throw new Error('Failed to fetch search results');
      }
      const data = await response.json();
      setSearchResults(data);
    } catch (error) {
      console.error('Error searching news:', error);
    }
  };

  const handleNewsClick = async (newsId) => {
    try {
      const payload = { news: newsId };
      const response = await fetch('http://localhost:8000/api/read_news/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Failed to save read history');
      }

      navigate(`/news/${newsId}`);
    } catch (error) {
      console.error('Error saving read history:', error);
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();

    try {
      let url = `http://127.0.0.1:8000/api/search_news/?query=${encodeURIComponent(selectedKeywordName)}`;

      if (showAdvancedSearch && selectedKeywordId && selectedRelation) {
        url = `http://127.0.0.1:8000/api/news_tags/${selectedKeywordId}/${selectedRelation}/`;
      } else if (showAdvancedSearch && selectedKeywordId) {
        url = `http://127.0.0.1:8000/api/news_tag/${selectedKeywordId}/`;
      }

      const response = await fetch(url);
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
      {/* <div className="advanced-search">
        <button
          className="test"
          style={{ marginLeft: '40px', marginTop: '0px', backgroundColor: '#669ee7', color: 'white', padding: '10px' }}
          onClick={() => setShowAdvancedSearch(!showAdvancedSearch)}
        >
          {showAdvancedSearch ? 'Tìm kiếm từ khoá' : 'Tìm kiếm theo Tag'}
        </button>

        {showAdvancedSearch && (
          <div className="keyword-list">
            <p>Tác động:</p>
            {relations.map((relation) => (
              <button
                key={relation}
                className="keyword-button"
                onClick={() => handleRelationClick(relation)}
              >
                {relation}
              </button>
            ))}
          </div>
        )}

        {showAdvancedSearch && (
          <div className="keyword-list">
            <p>Chủ thể:</p>
            {searchOptions.map((option) => (
              <button
                key={option.id}
                className="keyword-button"
                onClick={() => handleKeywordClick(option.id, option.name)}
              >
                {option.name}
              </button>
            ))}
          </div>
        )}
      </div> */}
      <div className="advanced-search">
      <h4 style={{paddingLeft: '40px',marginTop: '0px',color: 'black' ,color:'!important'}}> Tìm kiếm nâng cao </h4>
        <button
          className="test"
          style={{ marginLeft: '40px', marginTop: '0px', backgroundColor: '#669ee7', color: 'white', padding: '10px', width:'132px',marginBottom: '10px' }}
          onClick={() => setShowAdvancedSearch1(!showAdvancedSearch1)}
        >
          {showAdvancedSearch1 ? 'Tìm kiếm từ khoá' : 'Tìm kiếm theo Nguyên nhân'}
        </button>

        {showAdvancedSearch1 && (
          <div className="keyword-list">
            <p>Tác động:</p>
            {sentiments.map((sentiment) => (
              <button
                key={sentiment}
                className="keyword-button"
                onClick={() => handleSentimentClick(sentiment)}
              >
                {sentiment}
              </button>
            ))}
          </div>
        )}

        {showAdvancedSearch1 && (
          <div className="keyword-list">
            <p>Nguyên nhân:</p>
            {reasons.map((reason) => (
              <button
                key={reason.id}
                className="keyword-button"
                onClick={() => handleReasonClick(reason.id)}
              >
                {reason.name}
              </button>
            ))}
          </div>
        )}
        <button
          className="test"
          style={{ marginLeft: '40px', marginTop: '0px', backgroundColor: '#669ee7', color: 'white', padding: '10px',marginBottom: '10px' }}
          onClick={() => setShowAdvancedSearch(!showAdvancedSearch)}
        >
          {showAdvancedSearch ? 'Tìm kiếm từ khoá' : 'Tìm kiếm theo Tag'}
        </button>

        {showAdvancedSearch && (
          <div className="keyword-list">
            <p>Tác động:</p>
            {relations.map((relation) => (
              <button
                key={relation}
                className="keyword-button"
                onClick={() => handleRelationClick(relation)}
              >
                {relation}
              </button>
            ))}
          </div>
        )}

        {showAdvancedSearch && (
          <div className="keyword-list">
            <p>Chủ thể:</p>
            {searchOptions.map((option) => (
              <button
                key={option.id}
                className="keyword-button"
                onClick={() => handleKeywordClick(option.id, option.name)}
              >
                {option.name}
              </button>
            ))}
          </div>
        )}
      </div>

      <div className="search-results-container">
        <form onSubmit={handleSearch} className="search-input">
          <input
            type="text"
            placeholder="Nhập thông tin tìm kiếm"
            value={selectedKeywordName}
            onChange={(e) => setSelectedKeywordName(e.target.value)}
          />
          <button type="submit">Tìm kiếm</button>
        </form>

        <div className="search-results">
          {searchResults.length === 0 ? (
            <p>Không có kết quả tìm kiếm nào.</p>
          ) : (
            searchResults.map((item) => (
              <Link to={`/news/${item.id}`} key={item.id} className="news-link">
                <div className="news-item">
                  <img src={item.link_img} alt="Hình ảnh bài báo" />
                  <div className="news-item-content">
                    <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                    <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>
                      {highlightText(item.title, selectedKeywordName)}
                    </h2>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                    <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>
                      {highlightText(item.content ? item.content.split('\n')[0] : '', selectedKeywordName)}
                    </p>
                    <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
                  </div>
                </div>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default Search;


