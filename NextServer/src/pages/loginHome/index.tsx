import { NextPage } from "next"
import { useEffect, useState } from "react"
import { LoginHome } from "@/components/user"
interface Props{ article: string }
const LoginHomePage: NextPage<Props> = ({docs}: any) => {
    const [loginUser, setLoginUser] = useState("")
    useEffect(()=>{
        setLoginUser(JSON.stringify(localStorage.getItem("loginUser")))
    }
    )
    return (<><div>로그인 정보 : {loginUser} </div></>)
}
export default LoginHomePage