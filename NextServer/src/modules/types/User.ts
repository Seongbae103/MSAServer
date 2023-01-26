export interface User{
    userID? : string,
    email? : string,
    password? : string,
    birth? : string,
    address? : string,
    token? : string,
    created? : string,
    modified? : string
}
export interface UserLoginInput{
    email: string,
    password: string
}
export interface UserUpdate{
    userID?: string,
    phone?: string,
    password? : string,
    modified?: string
}
export interface LoginUser{ 
    userID?:string, password:string, email:string, 
    phone?:string, birth?:string, 
    token?: any
}

export interface UserInfo{
    userID?: string, password:string, email:string,
    phone:string, birth:string,
    token: any
}

export interface UserInfoState{
    data: UserInfo[]
    isloggined: boolean
}

export interface UserState{
    data: User[]
    status: 'idle' | 'loading' | 'failed'
    token?: null,
    isLoggined: boolean,
    error : null;
    loginedUser: null,
    check: boolean
}
