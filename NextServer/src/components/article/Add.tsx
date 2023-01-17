import { SubmitHandler, useForm} from "react-hook-form"
import { Article } from "@/modules/types"
import { useRef } from "react"
import { useDispatch } from "react-redux"
import { writeRequest } from "@/modules/slices"
import styled from 'styled-components';

export default function AddArticle() { 
    const dispatch = useDispatch()
    const { register, handleSubmit, watch, formState: { errors }  } = useForm<Article>()
    const onSubmit: SubmitHandler<Article> = data => {
      alert(`1 - 리액트에 입력된 회원정보 : ${JSON.stringify(data)}`)
      dispatch(writeRequest(data))
    };
    return (<>
        
        <form onSubmit={handleSubmit(onSubmit)}>
          <Sheet >
            <thead>
              <Row>
                <Cell colSpan={2}><h6>게시판 글쓰기</h6></Cell>
              </Row>
            </thead>
            <tbody>
              <Row>
                <Cell>
                <label htmlFor="title">제 목</label></Cell>
                <Cell><Input
            {...register("title", { 
              required: true,
              maxLength: 30,
            })}
            type="text"  id="title" name="title" 
            placeholder="제목"
            required minLength= {10} maxLength={20}/> <br/>
            
            {errors.title && <p>{errors.title.message}</p>} </Cell></Row>
            <Row><Cell>
          <label htmlFor="user_id">글쓴이</label></Cell>
          <Cell><Input 
          {...register("user_id", { 
            required: true,
            maxLength: 30,
          })} //...register가 있어야 위의 alert창에서 값을 받을 수 있다
            type="text" 
            placeholder="글쓴이 id"
            id="user_id" name="user_id" required /> 
                </Cell>
              </Row>
             
              <Row>
                <Cell>
                <label htmlFor="content">글내용</label></Cell><Cell>
          <Input 
          {...register("content", { 
            required: true,
            maxLength: 30,
          })}
          type="text" id="content" name="content" 
          placeholder="글내용"
          required /> </Cell>
              </Row>
              
              
              <Row>
                <Cell colSpan={2}><button type="submit" >전송</button></Cell>
              </Row>
              
            </tbody>
          </Sheet>

          
          </form> 
        </>)

    }

const Sheet = styled.table`
border: 1px solid black
width: 70%

`
const Row = styled.tr`
border: 1px solid black
`
const Cell = styled.td`
border: 1px solid black,

`
const Input = styled.input`
width: 100%
`