

import React, { useState, useEffect, useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { AuthContext } from '../Contexts/AuthContext';

const News = () => {
    const [news, setNews] = useState([]);
    const [recommendedNews, setRecommendedNews] = useState([]);
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/guest/news/');
                if (!response.ok) {
                    throw new Error('Failed to fetch news');
                }
                const data = await response.json();
                const sortedNews = data.sort((a, b) => b.id - a.id);
                setNews(sortedNews);
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        };

        const fetchRecommendedNews = async () => {
            if (user) {
                if (!user || !user.id) {
                    console.error('User is not logged in or user.id is not available');
                    return;
                  }
                const url = `http://127.0.0.1:8000/api/recommended-news/${user.id}/`;
                console.log('Fetching read news from URL:', url);  
                
                try {
                    const response = await fetch(url);
                    if (!response.ok) {
                        throw new Error('Failed to fetch recommended news');
                    }
                    const data = await response.json();
                    const sortedNews = data.sort((a, b) => b.id - a.id);
                    setRecommendedNews(sortedNews);
                } catch (error) {
                    console.error('Error fetching recommended news:', error);
                }
            }
        };

        fetchNews();
        fetchRecommendedNews();
    }, [user]);

    const handleNewsClick = async (newsId) => {
        try {
          const payload = {
            user: user.id,
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
      


    const renderUserInterestedNews = () => {
        if (recommendedNews.length === 0) return null;

        const firstTagNews = recommendedNews.slice(0, 1);
        const secondTagNews = recommendedNews.slice(1, 4);
        const thirdTagNews = recommendedNews.slice(4, 5);

        return (
            <div style={{ position: 'relative' }}>
                <div className="user-interested-news">
                    <div className="column">
                        {firstTagNews.map(item => (
                            <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                                <div className="news-item1" style={{ padding: '0px' }}>
                                    <p className="news-topic">{item.topic}</p>
                                    <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '400px', marginRight: '20px' }} />
                                    <h2 className="news-title">{item.title}</h2>
                                    <p className="news-content">{item.content.split('\n')[0]}</p>
                                    <p className="news-time">{item.time}</p>
                                    <p className="news-author">{item.author}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="column">
                        {secondTagNews.map(item => (
                            <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                                <div className="news-item" style={{ display: 'flex', marginBottom: '1px' }}>
                                    <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
                                    <div className="news-item-content" style={{ flex: 1 }}>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                                        <h2 style={{ margin: 0, fontSize: '1rem', fontWeight: 'bold' }}>{item.title}</h2>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="column">
                        {thirdTagNews.map(item => (
                            <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                                <div className="news-item1" style={{ padding: '0px' }}>
                                    <p className="news-topic">{item.topic}</p>
                                    <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '400px', marginRight: '20px' }} />
                                    <h2 className="news-title">{item.title}</h2>
                                    <p className="news-content">{item.content.split('\n')[0]}</p>
                                    <p className="news-time">{item.time}</p>
                                    <p className="news-author">{item.author}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
                <button className="view-more-btn"><Link to="/recommended_news" style={{ textDecoration: 'none', color: 'white' }}>Xem các chủ đề quan tâm</Link></button>
            </div>
        );
    };

    return (
        <div>
            <div className="interested-news-section">
                <h2 style={{ marginBottom: '10px', marginTop: '1px' }}>Tin khuyến nghị</h2>
                {renderUserInterestedNews()}
            </div>
            <hr />
            <div className="general-news-section" style={{ width: '900px', paddingLeft: '50px' }}>
                <h2>Tin tức chung</h2>
                {news.map(item => (
                    <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                        <div className="news-item" >
                            <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
                            <div className="news-item-content" style={{ flex: 1 }}>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                                <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                                <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default News;

