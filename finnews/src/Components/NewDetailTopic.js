import React, { useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';

const NewDetailTopic = () => {
    const { topicId } = useParams(); // Lấy topicId từ URL
    const [news, setNews] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [newsPerPage] = useState(7);
    const [topicName, setTopicName] = useState(''); // Thêm biến trạng thái cho tên chủ đề

    useEffect(() => {
        const fetchNews = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/topics/${topicId}/news/`);
                if (!response.ok) {
                    throw new Error('Failed to fetch news');
                }
                const data = await response.json();
                const sortedNews = data.sort((a, b) => b.id - a.id);
                setNews(sortedNews);
                if (sortedNews.length > 0) {
                    setTopicName(sortedNews[0].topic); // Giả sử tất cả tin tức có cùng một chủ đề
                }
            } catch (error) {
                console.error('Error fetching news:', error);
            }
        };

        fetchNews();
    }, [topicId]);

    // Tính index của tin tức đầu tiên trên trang hiện tại
    const indexOfLastNews = currentPage * newsPerPage;
    const indexOfFirstNews = indexOfLastNews - newsPerPage;
    const currentNews = news.slice(indexOfFirstNews, indexOfLastNews);

    // Logic cho việc chuyển trang
    const paginate = (pageNumber) => setCurrentPage(pageNumber);
    const nextPage = () => setCurrentPage(currentPage + 1);
    const prevPage = () => setCurrentPage(currentPage - 1);

    return (
        <div style={{width: '900px', paddingLeft: '50px'}}>
            <h2 style={{ marginBottom: '20px', marginTop: '1px' }}>Tin tức {topicName}</h2> {/* Cập nhật tiêu đề động */}

            {currentNews.map(item => (
                <Link to={`/news/${item.id}`} key={item.id} className="news-link">
                    <div className="News-item" style={{ display: 'flex', marginBottom: '20px' }}>
                        <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
                        <div className="news-item-content" style={{ flex: 1 }}>
                            <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
                            <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
                            <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
                            <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
                            <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
                        </div>
                    </div>
                </Link>
            ))}
            <ul className="pagination">
                <li className="page-item">
                    <button onClick={prevPage} className="page-link" disabled={currentPage === 1}>
                        Trang trước
                    </button>
                </li>
                {Array.from({ length: Math.ceil(news.length / newsPerPage) }, (_, i) => (
                    <li key={i} className="page-item">
                        <button onClick={() => paginate(i + 1)} className="page-link">
                            {i + 1}
                        </button>
                    </li>
                ))}
                <li className="page-item">
                    <button onClick={nextPage} className="page-link" disabled={currentPage === Math.ceil(news.length / newsPerPage)}>
                        Trang tiếp theo
                    </button>
                </li>
            </ul>
        </div>
    );
}

export default NewDetailTopic;

// import React, { useState, useEffect } from 'react';
// import { Link, useParams } from 'react-router-dom';

// const NewDetailTopic = () => {
//     const { topicId } = useParams(); // Lấy topicId từ URL
//     const [news, setNews] = useState([]);
//     const [topicName, setTopicName] = useState(''); // Thêm biến trạng thái cho tên chủ đề
//     const [currentPage, setCurrentPage] = useState(1);
//     const [newsPerPage] = useState(7);

//     useEffect(() => {
//         const fetchNews = async () => {
//             try {
//                 const response = await fetch(`http://127.0.0.1:8000/api/topics/${topicId}/news/`);
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch news');
//                 }
//                 const data = await response.json();
//                 const sortedNews = data.news.sort((a, b) => b.id - a.id); // Giả sử API trả về một mảng news
//                 setNews(sortedNews);
//                 setTopicName(data.topic_name); // Giả sử API trả về tên chủ đề
//             } catch (error) {
//                 console.error('Error fetching news:', error);
//             }
//         };

//         fetchNews();
//     }, [topicId]);

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
//             <h2 style={{ marginBottom: '20px', marginTop: '1px' }}>Tin tức {topicName}</h2> {/* Cập nhật tiêu đề động */}

//             {currentNews.map(item => (
//                 <Link to={`/news/${item.id}`} key={item.id} className="news-link">
//                     <div className="News-item" style={{ display: 'flex', marginBottom: '20px' }}>
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
//                     <button onClick={prevPage} className="page-link" disabled={currentPage === 1}>
//                         Trang trước
//                     </button>
//                 </li>
//                 {Array.from({ length: Math.ceil(news.length / newsPerPage) }, (_, i) => (
//                     <li key={i} className="page-item">
//                         <button onClick={() => paginate(i + 1)} className="page-link">
//                             {i + 1}
//                         </button>
//                     </li>
//                 ))}
//                 <li className="page-item">
//                     <button onClick={nextPage} className="page-link" disabled={currentPage === Math.ceil(news.length / newsPerPage)}>
//                         Trang tiếp theo
//                     </button>
//                 </li>
//             </ul>
//         </div>
//     );
// }

// export default NewDetailTopic;

// import React, { useState, useEffect } from 'react';
// import { Link, useParams } from 'react-router-dom';

// const NewDetailTopic = () => {
//     const { topicId } = useParams(); // Lấy topicId từ URL
//     const [news, setNews] = useState([]);
//     const [currentPage, setCurrentPage] = useState(1);
//     const [newsPerPage] = useState(7);
//     const [topicName, setTopicName] = useState(''); // Thêm biến trạng thái cho tên chủ đề

//     useEffect(() => {
//         const fetchNews = async () => {
//             try {
//                 const response = await fetch(`http://127.0.0.1:8000/api/topics/${topicId}/news/`);
//                 if (!response.ok) {
//                     throw new Error('Failed to fetch news');
//                 }
//                 const data = await response.json();
//                 const sortedNews = data.sort((a, b) => b.id - a.id);
//                 setNews(sortedNews);
//                 setTopicName(data.topic); 
//             } catch (error) {
//                 console.error('Error fetching news:', error);
//             }
//         };

//         fetchNews();
//     }, [topicId]);

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
//             <h2 style={{ marginBottom: '20px', marginTop: '1px' }}>Tin tức {topicName}</h2>

//             {currentNews.map(item => (
//                 <Link to={`/news/${item.id}`} key={item.id} className="news-link">
//                     <div className="News-item" style={{ display: 'flex', marginBottom: '20px' }}>
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
//                     <button onClick={prevPage} className="page-link" disabled={currentPage === 1}>
//                         Trang trước
//                     </button>
//                 </li>
//                 {Array.from({ length: Math.ceil(news.length / newsPerPage) }, (_, i) => (
//                     <li key={i} className="page-item">
//                         <button onClick={() => paginate(i + 1)} className="page-link">
//                             {i + 1}
//                         </button>
//                     </li>
//                 ))}
//                 <li className="page-item">
//                     <button onClick={nextPage} className="page-link" disabled={currentPage === Math.ceil(news.length / newsPerPage)}>
//                         Trang tiếp theo
//                     </button>
//                 </li>
//             </ul>
//         </div>
//     );
// }

// export default NewDetailTopic;


// // import React, { useState, useEffect } from 'react';
// // import { Link } from 'react-router-dom';

// // const NewDetailTopic = () => {
// //     const [news, setNews] = useState([]);
// //     const [currentPage, setCurrentPage] = useState(1);
// //     const [newsPerPage] = useState(7);

// //     useEffect(() => {
// //         const fetchNews = async () => {
// //             try {
// //                 const response = await fetch('http://127.0.0.1:8000/api/topics/${topicId}/news/');
// //                 if (!response.ok) {
// //                     throw new Error('Failed to fetch news');
// //                 }
// //                 const data = await response.json();
// //                 const sortedNews = data.sort((a, b) => b.id - a.id);
// //                 setNews(sortedNews);
// //             } catch (error) {
// //                 console.error('Error fetching news:', error);
// //             }
// //         };

// //         fetchNews();
// //     }, []);

// //     // Tính index của tin tức đầu tiên trên trang hiện tại
// //     const indexOfLastNews = currentPage * newsPerPage;
// //     const indexOfFirstNews = indexOfLastNews - newsPerPage;
// //     const currentNews = news.slice(indexOfFirstNews, indexOfLastNews);

// //     // Logic cho việc chuyển trang
// //     const paginate = (pageNumber) => setCurrentPage(pageNumber);
// //     const nextPage = () => setCurrentPage(currentPage + 1);
// //     const prevPage = () => setCurrentPage(currentPage - 1);

// //     return (
// //         <div style={{width: '900px', paddingLeft: '50px'}}>
// //                 <h2 style={{ marginBottom: '20px',marginTop: '1px'}} >Tin tức giá vàng</h2>

// //             {currentNews.map(item => (
// //                 <Link to={`/news/${item.id}`} key={item.id} className="news-link">
// //                     <div className="News-item" style={{ display: 'flex', marginBottom: '20px' }}>
// //                         <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
// //                         <div className="news-item-content" style={{ flex: 1 }}>
// //                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
// //                             <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
// //                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
// //                             <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
// //                             <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
// //                         </div>
// //                     </div>
// //                 </Link>
// //             ))}
// //             <ul className="pagination">
// //                 <li className="page-item">
// //                     <button onClick={prevPage} className="page-link">Trang trước</button>
// //                 </li>
// //                 {Array.from({ length: Math.ceil(news.length / newsPerPage) }, (_, i) => (
// //                     <li key={i} className="page-item">
// //                         <button onClick={() => paginate(i + 1)} className="page-link">
// //                             {i + 1}
// //                         </button>
// //                     </li>
// //                 ))}
// //                 <li className="page-item">
// //                     <button onClick={nextPage} className="page-link">Trang tiếp theo</button>
// //                 </li>
// //             </ul>
// //         </div>
// //     );
// // }

// // export default NewDetailTopic;
