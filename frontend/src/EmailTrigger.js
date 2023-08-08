import axios from 'axios';
import React from 'react';

function EmailTrigger() {
  const sendEmail = () => {
    axios.post('http://localhost:8080/licenses/trigger-emails/')
      .then((response) => {
        console.log(response.data)
        if (response.data.status === 'success') {
          alert('Email sent successfully!');
        } else {
          alert('An error occurred: ' + response.data.message);
        }
      })
      .catch((error) => {
        alert('A network error occurred: ' + error);
      });
  };

  return (
    <div>
      <button onClick={sendEmail}>Trigger Email</button>
    </div>
  );
}

export default EmailTrigger;