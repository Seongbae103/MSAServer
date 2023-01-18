import { createSlice, PayloadAction } from "@reduxjs/toolkit"
import { User } from '@/modules/types'
import { UserLoginInput } from "@/modules/types"
import { AppState } from "../store";
import { createSelector } from '@reduxjs/toolkit'; 
type UserState = {
    data: User[]
    status: 'idle' | 'loading' | 'failed'
    isLoggined: boolean
    error: any
    token: string

}


const initialState: UserState = {
    data: [],
    status: 'idle',
    isLoggined: false,
    error: null,
    token: '' //테스트시에만 ''내부에 입력
}

const userSlice = createSlice({
    name: 'userSlice',
    initialState,
    reducers: {
        joinRequest(state: UserState, action: PayloadAction<User>){
            alert(`2 joinRequest ${JSON.stringify(action.payload)}`)
            state.status = 'loading'
            state.error = null
        },
        joinSuccess(state: UserState, {payload}){
            state.status = 'idle'
            state.data = [...state.data, payload]
        },
        joinFailure(state: UserState, {payload}){
            state.status = 'failed'
            state.data = [...state.data, payload]
        },
        loginRequest(state: UserState, action: PayloadAction<UserLoginInput>){
            alert(` 1 ${JSON.stringify(action.payload)}`) ///로그인 정보 흐름1
            state.status = 'loading'
        },
        loginSuccess(state: UserState, {payload}){
            //alert(`&&&&&&&& loginSuccess >>>> payload is ${JSON.stringify(payload)}`)
            alert(`4 token >>>> payload is ${payload.token}`) ///로그인 정보 흐름4
            state.status = 'idle'
            state.data = [...state.data, payload]
            state.token = payload.token
            alert(`5 token >>>> state.token is ${state.token}`) ///로그인 정보 흐름5
        },
        loginFailure(state: UserState, {payload}){
            state.status = 'failed'
            state.data = [...state.data, payload]
        },
        logoutRequest(state: UserState, {payload}) {
            alert(`5 token >>> state.token in ${payload.token}`)
            state.status = 'loading';
            state.error = null;
        },
        logoutSuccess(state: UserState ){
            state.status = 'idle'
            window.location.href = '/'
        },
        logoutFailure(state: UserState, action: PayloadAction<{ error: any }>) {
            state.status = 'failed';
            state.error = action.payload;
        },

        // 회원정보
        setUserInfo(state: UserState) {
            state.status = 'idle';
            state
        }

    }
})

const {reducer, actions} = userSlice



// Actions
export const {joinRequest, joinSuccess, joinFailure,
    loginRequest, loginSuccess, loginFailure,
    logoutRequest, logoutSuccess, logoutFailure
} = userSlice.actions
export const userAction = actions

// Selectors
export const selectUserData = (state: AppState) => state.user.data;
export const selectUserStatus = (state: AppState) => state.user.status;
export const selectUserIsLoggined = (state: AppState) => state.user.isLoggined;
export const selectUserError = (state: AppState) => state.user.error;
export const userTokenSelector = (state: AppState) => state.user.token || initialState.token;
export const userSelector = createSelector(
    userTokenSelector,
    (token) => {
      return `My Token is ${token}.`;
    }
  );

// Reducer
export const userData = (state: AppState) => state.userSlice
export default reducer
        