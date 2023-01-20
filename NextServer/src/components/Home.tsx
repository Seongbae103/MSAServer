import axios from "axios";
import {useState, useEffect} from "react"
import Pagination from "./admin/Pagination";



export default function Home(){

   const [currentPage, setCurrentPage] = useState(1);
   const lastPage = 3;
   const [list, setList] = useState([])
   const [count, setCount] = useState(0)

    useEffect(()=>{
        axios
        .get('http://localhost:8000/users/page/1')
        .then(res => {
            const count = res.data.count
            const items = res.data.pager.items
            setCount(count)
            setList(items)
        })
        .catch(err => {console.log(err)})
    }, [])

  return (
    <>
    <h2>회원목록 총{count}명</h2>
        <table className='user-list'>
            <thead>
                <tr>
                <th>ID</th><th>이메일</th><th>비번</th><th>이름</th><th>전화번호</th>
                <th>생년월일</th><th>주소</th><th>직업</th><th>관심사항</th>
                </tr>
            </thead>
            <tbody>
            {list && list.map(({userid, email, password, username, phone, birth, address, job, interests})=>(
                <tr key={userid}>
                    <td>{userid}</td><td>{email}</td><td>{password}</td><td>{username}</td>
                    <td>{phone}</td><td>{birth}</td><td>{address}</td>
                    <td>{job}</td><td>{interests}</td>
                </tr>
            ))}
            </tbody>
        </table>
        <div className="page-container">
      <h1>React TypeScript Pagination</h1>
      <Pagination
        currentPage={currentPage}
        lastPage={lastPage}
        maxLength={7}
        setCurrentPage={setCurrentPage}
      />
    </div>
    </>
    
  );
}