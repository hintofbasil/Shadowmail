import React from 'react';

import axios from 'axios';
import DeleteFormResponse from './delete_form_response';

const REQUEST_DELETE_URL = '/api/request_delete';

class RequestDeleteForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: '',
    };
  }

  componentDidMount = () => {
    const url = new URL(document.URL);
    const email = url.searchParams.get('email');
    this.setState({
      email,
    });
  }

  handleInput = (event) => {
    this.setState({
      email: event.target.value,
    });
  }

  handleSubmit = async (event) => {
    event.preventDefault();
    const data = {
      email: this.state.email,
    };
    try {
      const response = await axios.post(REQUEST_DELETE_URL, data);
      this.setState({
        status: response.data.status,
        reason: 'Confirmation email sent',
      });
    } catch (error) {
      const { response } = error;
      this.setState({
        status: response.data.status || 'ERROR',
        reason: response.data.reason || 'An unexpected error occured',
      });
    }
  }

  render = () => (
    <>
      <div className="row">
        <div className="offset-by-two eight columns">
          <form method="POST" id="click-me-form">
            <input
              type="email"
              name="email"
              id="click-me-text-input"
              placeholder="you@domain.com"
              value={this.state.email}
              onChange={this.handleInput}
            />
            <br />
            <input
              type="submit"
              id="click-me-button"
              value="Send request"
              onClick={this.handleSubmit}
            />
          </form>
        </div>
      </div>
      {this.state.status
        && <DeleteFormResponse
          status={this.state.status}
          reason={this.state.reason}
        />
      }
    </>
  )
}

export default RequestDeleteForm;
