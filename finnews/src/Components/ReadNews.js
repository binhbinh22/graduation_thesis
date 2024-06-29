import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../Contexts/AuthContext';

const ReadNews = () => {
  const [readNews, setReadNews] = useState([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    const fetchReadNews = async () => {
      if (!user || !user.id) {
        console.error('User is not logged in or user.id is not available');
        return;
      }

      const url = `http://localhost:8000/api/get_read_news/${user.id}/`;
      console.log('Fetching read news from URL:', url);  // In ra URL

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch read news');
        }
        const data = await response.json();
        console.log('Fetched read news data:', data);  // In ra dữ liệu nhận được
        const sortedNews = data.sort((a, b) => b.id - a.id);
        setReadNews(sortedNews);
      } catch (error) {
        console.error('Error fetching read news:', error);
      }
    };

    if (user) {
      console.log('Fetching read news for user:', user);
      fetchReadNews();
    }
  }, [user]);

  return (
    <div>
      <h2 style={{marginTop: '0px'}}>Lịch sử đọc tin</h2>
      <div className="read-news-container">
        {readNews.map((item) => (
          <div className="news-item" key={item.id} style={{width: '900px'}} >
            <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
            <div className="news-item-content" style={{ flex: 1 }}>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
              <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
              <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
              <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReadNews;


