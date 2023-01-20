import { PayloadAction } from "@reduxjs/toolkit"
import { call, delay, put, takeLatest } from "redux-saga/effects"
import { writeRequest, writeSuccess, writeFailure} from '@/modules/slices';
import { Article } from '@/modules/types';
// import { user } from '@/modules/controllers';
import { article } from '@/modules/apis/articleAPI';
// api 

export function* watchWrite(){
    yield takeLatest(writeRequest, (action: {payload: Article}) => {
        try{
            alert(' 결과: ${response.data.msg}')
            const response: any = article.write(action.payload)
            put(writeSuccess(response.payload))
            window.location.href = '/article/write'
        }catch(error){
            alert(' 결과: ${response.data.msg}')
            put(writeFailure(error))
        }
    })
}
