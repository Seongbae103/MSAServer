export interface Article{
    artseq? : number
    title? : string
    content? : string
    created? : string
    modified? : string
    userid? : string
    username? : string
}

/** 
export interface ImageInput{
    item : string
    color: string
}
*/
/**
export interface Image {
    picture : any
}
 */
export interface InputImage{
    name: string
    lastModified: number
    lastModifiedDate: number
    type: string
    webkitRelativePath: string    
    size : number
}


export interface ImageState{
    data: InputImage
    status: 'successed' | 'loading' | 'failed'
}

export interface UploadFileResponse {
    success: boolean,
    message: string
}
export interface GetFileResponse {
    success: boolean,
    message: string
}

export interface ValidatorResponse {
    isValid: boolean,
    errorMessage: string
}

export const fileTypes = [
    'jpg',
    'png',
    'mp3',
    'mp4',
    'gif'

]
