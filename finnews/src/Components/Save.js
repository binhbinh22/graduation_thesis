import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../Contexts/AuthContext';
import { Link } from 'react-router-dom';

const Save = () => {
    const [news, setNews] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [newsPerPage] = useState(7);
    const { user } = useContext(AuthContext);


    useEffect(() => {
        const fetchNews = async () => {
            if (!user || !user.id) {
                console.error('User is not logged in or user.id is not available');
                return;
              }
            const url = `http://localhost:8000/api/get_save_news/${user.id}/`;
            console.log('Fetching read news from URL:', url);  
      
            try {
                const response = await fetch(url);
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

        fetchNews();
    }, [user]);

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
        <h2 style={{ marginBottom: '10px',marginTop: '1px'}} >Tin khuyến nghị</h2>
            {currentNews.map(item => (
                <Link to={`/news/${item.news}`} key={item.news} className="news-link">
                    <div className="News-item" style={{ display: 'flex', marginBottom: '20px' }}>
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
                </Link>
            ))}
            <ul className="pagination">
                <li className="page-item">
                    <button onClick={prevPage} className="page-link">Trang trước</button>
                </li>
                {Array.from({ length: Math.ceil(news.length / newsPerPage) }, (_, i) => (
                    <li key={i} className="page-item">
                        <button onClick={() => paginate(i + 1)} className="page-link">
                            {i + 1}
                        </button>
                    </li>
                ))}
                <li className="page-item">
                    <button onClick={nextPage} className="page-link">Trang tiếp theo</button>
                </li>
            </ul>
        </div>
    );
}

export default Save;

// import React, { useState, useEffect, useContext } from 'react';
// import { AuthContext } from '../Contexts/AuthContext';
// import { Link } from 'react-router-dom';

// const Save = () => {
//   const [saveNews, setSaveNews] = useState([]);
//   const { user } = useContext(AuthContext);

//   useEffect(() => {
//     const fetchReadNews = async () => {
//       if (!user || !user.id) {
//         console.error('User is not logged in or user.id is not available');
//         return;
//       }

//       const url = `http://localhost:8000/api/get_save_news/${user.id}/`;
//       console.log('Fetching read news from URL:', url);  // In ra URL

//       try {
//         const response = await fetch(url);
//         if (!response.ok) {
//           throw new Error('Failed to fetch read news');
//         }
//         const data = await response.json();
//         console.log('Fetched read news data:', data);  // In ra dữ liệu nhận được
//         setSaveNews(data);
//       } catch (error) {
//         console.error('Error fetching read news:', error);
//       }
//     };

//     if (user) {
//       console.log('Fetching read news for user:', user);
//       fetchReadNews();
//     }
//   }, [user]);

//   return (
//     <div>
//       <h2 style={{marginTop: '0px',marginLeft: '50px'}}>Tin tức đã lưu</h2>
//       <div className="read-news-container">
//         {saveNews.map((item) => (
//           <Link to={`/news/${item.id}`} key={item.id} className="news-link">
//           <div className="news-item" key={item.id} style={{width: '900px'}} >
//             <img src={item.link_img} alt="Hình ảnh bài báo" style={{ width: '150px', marginRight: '20px' }} />
//             <div className="news-item-content" style={{ flex: 1 }}>
//               <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.topic}</p>
//               <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'bold' }}>{item.title}</h2>
//               <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.time}</p>
//               <p style={{ margin: 0, fontSize: '1rem', color: 'black' }}>{item.content.split('\n')[0]}</p>
//               <p style={{ margin: 0, fontSize: '0.8rem', color: 'gray' }}>{item.author}</p>
//             </div>
//           </div>
//           </Link>
//         ))}
//       </div>
//     </div>
//   );
// };

// export default Save;
