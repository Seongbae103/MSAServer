import '../styles/SignUp.css'

export default function FindEmail() {

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
            <h1>이메일 찾기</h1>
            <form action="/send-data-here">
                <label htmlFor="user_name">User Name:</label>
                <input type="text" id="user_name" name="user_name" required minLength={4} maxLength={20} />

                <label htmlFor="phone">Phone:</label>
                <input type="text" id="phone" name="phone" required minLength={4} maxLength={20} />

                <button type="submit">Submit</button>
            </form>
        </>
    )
}
