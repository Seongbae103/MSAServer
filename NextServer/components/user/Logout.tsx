import React from 'react';

export default function Logout(){

    return <button
        onClick = { e => {
            e.preventDefault()
            e.stopPropagation()

        }}> 로그아웃
    </button>}

