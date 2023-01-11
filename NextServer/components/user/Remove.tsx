export default function RemoveUser() {
    
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
            <h1>탈퇴</h1>
            <form action="/send-data-here" method="post">
                
                <label htmlFor="password">Password:</label>
                <input type="text" id="password" name="password" required minLength={4} maxLength={20}/>

                <button type="submit">Submit</button>
            </form>
        </>
    )
}
