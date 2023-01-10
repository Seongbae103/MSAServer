import React, { useCallback, useState } from 'react';


import { useDispatch } from 'react-redux';

import styled from 'styled-components'
export default function UserRemove() 
  const [pwd, setPwd] = useState('')

  const dispatch = useDispatch()

const Main = styled.div`
width: 500px;
margin: 0 auto;
text-decoration:none
text-align: center;
`