import '../styles/Login.css'
import { useDispatch } from 'react-redux';
import { useForm } from "react-hook-form";
import styled from 'styled-components'
import  Layout  from '../admin/Layout';
import  Header  from '../admin/Header';
import  Footer  from '../admin/Footer';

export default function LoginForm(){
    const dispatch = useDispatch()
    const { register, handleSubmit, formState: { errors } } = useForm();

    return (
        <Layout><Main>
        <h1>로그인</h1>
            
                </Main>
            </Layout>
 );
}
const Span = styled.span`
   color: red
`
const Main = styled.div`
width: 500px;
margin: 0 auto;
text-decoration:none
text-align: center;
`