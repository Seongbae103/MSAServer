import axios, { AxiosResponse } from 'axios'
import { currentTime } from '@/components/admin/utils'
import { Article } from '@/modules/types'
import { author } from '../controllers'


export const article = {
    async write(payload: Article){
            try{
                const response : AxiosResponse<any, Article[]> =
                await axios.post(`http://localhost:8000/articles/write`, payload, {headers: {
                    "Content-Type" : "application/json",
                    Authorization: "JWT fefege...",
                }})
                if(response.data === "success"){
                    alert('4 결과: API 내부 join 성공'+ JSON.stringify(response.data))
                }else{
                    alert(' 결과: ${response.data.msg}')
                }
                
                return response
            }catch(err){
                console.log(` ${currentTime} : articleSaga 내부에서 join 실패 `)
            }
        },
       async update(payload:Article){
        try{
            const response : AxiosResponse<any, Article[]> =
            await author.post('http://localhost:8000/articles/update', payload)
            alert(`4 서버에서 리턴받은 값: ${JSON.stringify(response.data)}`)
            localStorage.setItem("title", JSON.stringify(response.data.title))
            localStorage.setItem("content", JSON.stringify(response.data.content))
        }catch(err){
            return err;
        }
    },
    
}