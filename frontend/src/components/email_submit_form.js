import React from 'react';

import axios from 'axios';
import EmailSubmitSuccess from './email_submit_success';

const NEW_EMAIL_URL = '/api/new';

class EmailSubmitForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
    };
  }

  handleFormInput = (event) => {
    this.setState({
      [event.target.name]: event.target.value,
    });
  }

  handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
      email: this.state.email,
    };
    const response = await axios.post(NEW_EMAIL_URL, data);
    this.setState({
      new_email: response.data.email,
    });
  }

  render = () => (
    <>
      <div className="row">
        <div className="offset-by-two eight columns">
          <form method="POST" id="new-email-form"
            className="input-then-button-layout"
          >
            <input
              type="submit"
              value="↩"
              onClick={this.handleSubmit}
            />
            <span className="submit-span">
              <input
                type="email"
                name="email"
                className="email-input"
                id="new-email-input"
                placeholder="you@domain.com"
                value={this.state.email}
                onChange={this.handleFormInput}
              />
            </span>
          </form>
        </div>
      </div>
      <div className="row">
        <div className="offset-by-two eight columns">
          {
            this.state.new_email
            && <EmailSubmitSuccess email={this.state.new_email} />
          }
        </div>
      </div>
    </>
  )
}

export default EmailSubmitForm;
