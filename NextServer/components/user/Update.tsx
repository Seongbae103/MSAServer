export default function UserUpdate() {
    
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
            <h1>회원정보 갱신</h1>
            <form action="/send-data-here" method="put" >
                <label htmlFor="user_email">User Email:</label>
                <div id="user_email"></div>

                <label htmlFor="password">Password:</label>
                <div id="password"></div>
               
                <label htmlFor="user_name">User Name:</label>
                <div id="user_name"></div>

                <label htmlFor="phone">Phone:</label>
                <input type="text" id="phone" name="phone" />

                <label htmlFor="birth">Birth:</label>
                <div id="birth"></div>

                <label htmlFor="address">Address:</label>
                <input type="text" id="address" name="address" />

                <label htmlFor="job">Job:</label>
                <input type="text" id="job" name="job" />

                <label htmlFor="user_interests">User Interests:</label>
                <input type="text" id="user_interests" name="user_interests" />

                <button type="submit">Submit</button>
            </form>
        </>
    )
}
