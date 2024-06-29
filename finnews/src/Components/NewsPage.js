import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const NewsPage = () => {
    const [news, setNews] = useState([]);
    const [highlightedNews, setHighlightedNews] = useState([]);
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

        const fetchHighlightedNews = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/guest/news/featured/');
                if (!response.ok) {
                    throw new Error('Failed to fetch highlighted news');
                }
                const data = await response.json();
                setHighlightedNews(data);
            } catch (error) {
                console.error('Error fetching highlighted news:', error);
            }
        };

        fetchNews();
        fetchHighlightedNews();
    }, []);

    const handleNewsClick = (newsId) => {
        navigate(`/news/${newsId}`);
    };

    const renderHighlightedNews = () => {
        if (highlightedNews.length === 0) return null;
    
        const firstTopicNews = highlightedNews.filter(news => news.topic === 'Xăng dầu').slice(0, 1);
        const secondTopicNews = highlightedNews.filter(news => news.topic === 'Nông sản').slice(0, 3);
        const thirdTopicNews = highlightedNews.filter(news => news.topic === 'Tài chính').slice(0, 1);
    
        return (
            <div style={{ position: 'relative' }}>
                <div className="user-interested-news">
                    <div className="column">
                        {firstTopicNews.map(item => (
                            <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                                <div className="news-item1" style={{ padding: '0px' }}>
                                    <p className="news-topic">{item.topic}</p>
                                    <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '400px', marginRight: '20px' }} />
                                    <h2 className="news-title">{item.title}</h2>
                                    <p className="news-content">{item.info_extrac.split('\n')[0]}</p>
                                    <p className="news-time">{item.time}</p>
                                    <p className="news-author">{item.author}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="column">
                        {secondTopicNews.map(item => (
                            <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                                <div className="news-item" style={{ display: 'flex', marginBottom: '1px' }}>
                                    <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
                                    <div className="news-item-content" style={{ flex: 1 }}>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                                        <h2 style={{ margin: 0, fontSize: '1rem', fontWeight: 'bold' }}>{item.title}</h2>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'black' }}>{item.info_extrac.split('\n')[0]}</p>
                                        <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <div className="column">
                        {thirdTopicNews.map(item => (
                            <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                                <div className="news-item1" style={{ padding: '0px',paddingBottom: '60px' }}>
                                    <p className="news-topic">{item.topic}</p>
                                    <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '400px', marginRight: '20px',height: '276px' }} />
                                    <h2 className="news-title">{item.title}</h2>
                                    <p className="news-content">{item.info_extrac.split('\n')[0]}</p>
                                    <p className="news-time">{item.time}</p>
                                    <p className="news-author">{item.author}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
                <div>
                <button className="view-more-btn">
                    <Link to="/highligh" style={{ textDecoration: 'none', color: 'white' }}>
                        Xem thêm các tin tức nổi bật
                    </Link>
                </button>
                </div>
            </div>
        );
    };
    

    return (
        <div>
            <div className="interested-news-section">
                <h2 style={{ marginBottom: '10px', marginTop: '1px',marginLeft: '50px' }}>Tin nổi bật</h2>
                {renderHighlightedNews()}
            </div>
            <hr />
            <div className="general-news-section" style={{ width: '900px', paddingLeft: '50px' }}>
                <h2>Tin tức chung</h2>
                {news.map(item => (
                    <div key={item.id} className="news-link" onClick={() => handleNewsClick(item.id)}>
                        <div className="news-item">
                            <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
                            <div className="news-item-content" style={{ flex: 1 }}>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                                <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                                <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
                                <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
                                <hr style={{marginTop: '10px'}}/>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default NewsPage;

// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';

// const NewsPage = () => {
//     const [news, setNews] = useState([]);
//     const [currentPage, setCurrentPage] = useState(1);
//     const [newsPerPage] = useState(10);

//     useEffect(() => {
//         const fetchNews = async () => {
//             try {
//                 const response = await fetch('http://127.0.0.1:8000/api/guest/news/');
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch news');
//                 }
//                 const data = await response.json();
//                 const sortedNews = data.sort((a, b) => b.id - a.id);
//                 setNews(sortedNews);
//             } catch (error) {
//                 console.error('Error fetching news:', error);
//             }
//         };

//         fetchNews();
//     }, []);

//     const indexOfLastNews = currentPage * newsPerPage;
//     const indexOfFirstNews = indexOfLastNews - newsPerPage;
//     const currentNews = news.slice(indexOfFirstNews, indexOfLastNews);

//     const totalPages = Math.ceil(news.length / newsPerPage);

//     const paginate = (pageNumber) => setCurrentPage(pageNumber);
//     const nextPage = () => setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));
//     const prevPage = () => setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));

//     const renderPageNumbers = () => {
//         const pageNumbers = [];
//         const maxPageNumbersToShow = 5;
//         const startPage = Math.max(1, currentPage - Math.floor(maxPageNumbersToShow / 2));
//         const endPage = Math.min(totalPages, startPage + maxPageNumbersToShow - 1);

//         if (startPage > 1) {
//             pageNumbers.push(
//                 <button key={1} onClick={() => paginate(1)} className={`pagination-button ${currentPage === 1 ? 'active' : ''}`}>
//                     1
//                 </button>
//             );
//             if (startPage > 2) {
//                 pageNumbers.push(<span key="ellipsis1" className="ellipsis">...</span>);
//             }
//         }

//         for (let i = startPage; i <= endPage; i++) {
//             pageNumbers.push(
//                 <button key={i} onClick={() => paginate(i)} className={`pagination-button ${currentPage === i ? 'active' : ''}`}>
//                     {i}
//                 </button>
//             );
//         }

//         if (endPage < totalPages) {
//             if (endPage < totalPages - 1) {
//                 pageNumbers.push(<span key="ellipsis2" className="ellipsis">...</span>);
//             }
//             pageNumbers.push(
//                 <button key={totalPages} onClick={() => paginate(totalPages)} className={`pagination-button ${currentPage === totalPages ? 'active' : ''}`}>
//                     {totalPages}
//                 </button>
//             );
//         }

//         return pageNumbers;
//     };

//     return (
//         <div style={{width: '900px', paddingLeft: '50px'}}>
//             <h2  style={{ marginBottom: '20px',marginTop: '1px'}}>Trang chủ</h2>

//             {currentNews.map(item => (
//                 <Link to={`/news/${item.id}`} key={item.id} className="news-link">
//                 <div className="News-item" style={{ display: 'flex', marginBottom: '20px' }}>
//                         <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
//                         <div className="news-item-content" style={{ flex: 1 }}>
//                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
//                             <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
//                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
//                             <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
//                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
//                         </div>
//                     </div>
//                 </Link>
//             ))}

//             <div className="pagination-container">
//                 <button onClick={prevPage} className="pagination-button" disabled={currentPage === 1}>
//                     Trang trước
//                 </button>
//                 {renderPageNumbers()}
//                 <button onClick={nextPage} className="pagination-button" disabled={currentPage === totalPages}>
//                     Trang tiếp theo
//                 </button>
//             </div>
//         </div>
//     );
// };

// export default NewsPage;




// import React, { useState, useEffect } from 'react';
// import { Link } from 'react-router-dom';

// const NewsPage = () => {
//     const [news, setNews] = useState([]);
//     const [currentPage, setCurrentPage] = useState(1);
//     const [newsPerPage] = useState(10);

//     useEffect(() => {
//         const fetchNews = async () => {
//             try {
//                 const response = await fetch('http://127.0.0.1:8000/api/guest/news/');
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch news');
//                 }
//                 const data = await response.json();
//                 setNews(data);
//             } catch (error) {
//                 console.error('Error fetching news:', error);
//             }
//         };

//         fetchNews();
//     }, []);

//     // Tính index của tin tức đầu tiên trên trang hiện tại
//     const indexOfLastNews = currentPage * newsPerPage;
//     const indexOfFirstNews = indexOfLastNews - newsPerPage;
//     const currentNews = news.slice(indexOfFirstNews, indexOfLastNews);

//     // Logic cho việc chuyển trang
//     const paginate = (pageNumber) => setCurrentPage(pageNumber);
//     const nextPage = () => setCurrentPage(currentPage + 1);
//     const prevPage = () => setCurrentPage(currentPage - 1);

//     return (
//         <div style={{width: '900px', paddingLeft: '50px'}}>
//                 <h2 style={{ marginBottom: '20px',marginTop: '1px'}} >Trang chủ</h2>

//             {currentNews.map(item => (
//                 <Link to={`/news/${item.id}`} key={item.id} className="news-link">
//                     <div className="News-item" style={{ display: 'flex', marginBottom: '20px', marginTop: '10px' }}>
//                         <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
//                         <div className="news-item-content" style={{ flex: 1 }}>
//                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
//                             <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
//                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
//                             <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
//                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
//                         </div>
//                     </div>
//                 </Link>
//             ))}
//             <ul className="pagination">
//                 <li className="page-item">
//                     <button onClick={prevPage} className="page-link">Trang trước</button>
//                 </li>
//                 {Array.from({ length: Math.ceil(news.length / newsPerPage) }, (_, i) => (
//                     <li key={i} className="page-item">
//                         <button onClick={() => paginate(i + 1)} className="page-link">
//                             {i + 1}
//                         </button>
//                     </li>
//                 ))}
//                 <li className="page-item">
//                     <button onClick={nextPage} className="page-link">Trang tiếp theo</button>
//                 </li>
//             </ul>
//         </div>
//     );
// }

// export default NewsPage;