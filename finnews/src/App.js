import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Switch } from 'react-router-dom';
import Navbar from './Components/Navbar';
import News from './Components/News';
import Gold from './Components/Gold';
import Stock from './Components/Stock';
import Commodities from './Components/Commodities';
import Header from './Components/Header';
import AdminPage from './Admin/AdminPage';
import Search from './Components/Search';
import NewsDetail from './Components/NewsDetail';
import './App.css';
import Register from './Components/Register';
import Login from './Components/Login';
import { AuthProvider } from './Contexts/AuthContext';
import SearchResults from './Components/SearchResults';
import SelectTags from './Components/SelectTags'; 
function App() {
  return (
    <AuthProvider>
    <Router>
      <div className="container">
        <Header />
        <Navbar />
        <div className="news-container">
          <Routes>
            <Route path="/" element={<News />} />
            <Route path="/commodities" element={<Commodities />} />
            <Route path="/stocks" element={<Stock />} />
            <Route path="/gold" element={<Gold />} />
            <Route path="/news/:id" element={<NewsDetail />} />
            <Route path="/admin/*" element={<AdminPage />} />
            <Route path="/search" element={<Search />} />
            <Route path="*" element={<Navigate to="/" />} />
            <Route path="/register" element={<Register/>} />
            <Route path="/login" element={<Login/>} />
            <Route path="/select-tags" element={<SelectTags />} />
            <Route path="/search" element={<SearchResults />} />
          </Routes>
        </div>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;




// import React from 'react';
// import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import Navbar from './Components/Navbar';
// import News from './Components/News';
// import Header from './Components/Header';
// import NewsItem from './Components/NewsItem';
// import AdminPage from './Admin/AdminPage'; // Import trang Admin
// import Search from './Components/Search'; // Import Search component

// import './App.css';

// function App() {
//   return (
//     <Router>
//       <div className="container">
//         <Header />
//         <Navbar />
//         <div className="news-container">
//           <Routes>
//             <Route path="/" element={<News />} />
//             <Route path="/newsitem/:id" element={<NewsItem />} />
//             <Route path="/news" element={<Navigate to="/" />} />
//             <Route path="/admin/*" element={<AdminPage />} /> {/* Điều hướng đến trang Admin */}
//             <Route path="/search" element={<Search />} /> {/* Add Search route */}

//           </Routes>
//         </div>
//       </div>
//     </Router>
//   );
// }

// export default App;
