export default function Login(){
    const validateFormWithJS = () => {
        //const name = document.querySelector('#name').value
        //const rollNumber = document.querySelector('#rollNumber').value
        const name = ""
        const rollNumber = ""
        if (!name) {
          alert('Please enter your name.')
          return false
        }
    
        if (rollNumber.length < 3) {
          alert('Roll Number should be at least 3 digits long.')
          return false
        }
      }
    

    return (<>
            <h1>로그인</h1>
            <form action="/send-data-here" method="post" onSubmit={validateFormWithJS} >
                <label htmlFor="user_email">User Email:</label>
                <input type="text" id="user_email" name="user_email" />

                <label htmlFor="password">Password:</label>
                <input type="text" id="password" name="password" />

                <button type="submit">Submit</button>
            </form>
        </>
    )
}