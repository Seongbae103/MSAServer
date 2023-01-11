export default function FindPassword() {

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
            <h1>비밀번호 찾기</h1>
            <form action="/send-data-here">
                <label htmlFor="user_email">User Email:</label>
                <input type="text" id="user_email" name="user_email"/>

                <button type="submit">Submit</button>
            </form>
        </>
    )
}

