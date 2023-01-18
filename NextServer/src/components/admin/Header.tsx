import React, { useEffect, useState } from 'react';
import styled from 'styled-components'
import Navbar from './Navbar';
import NavbarAuth from './NavbarAuth';
export default function Header(){
  const [token, setToken] = useState("")    //상태에 저장 (setitem을 하는 장소는api)
  useEffect(() => {                          // 열리면 바로 실행
    alert(`토큰 유지 여부 ${localStorage.getItem('key')}`)
    setToken(localStorage.getItem('session')||"")    // 로컬스토리지에 있는 session에서 가져옴
  }, [])
    return (
      <><header>
        {token === "" ? <Navbar/> : <NavbarAuth/>}
      </header>
      </>
    )
  }
const Span = styled.span`
    color: red;
    float: right;
    padding-right: 100px
`
const HR = styled.hr`
  border: 1px solid black;
  text-align: center;
`
